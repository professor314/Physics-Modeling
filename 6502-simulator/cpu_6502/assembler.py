"""Two-pass assembler for 6502 assembly language.

Supports all 13 addressing mode syntaxes, labels, and common directives.
Case-insensitive mnemonics, hexadecimal literals with $ prefix.

Syntax examples:
    loop:       LDA #$42        ; immediate
                STA $00         ; zero page
                STA $0200       ; absolute
                LDA $10,X       ; zero page,X
                LDA $4000,X    ; absolute,X
                LDA $4000,Y    ; absolute,Y
                LDA ($40,X)    ; indexed indirect
                LDA ($40),Y    ; indirect indexed
                JMP ($FFFC)    ; indirect
                BNE loop       ; relative (label)
                ASL A          ; accumulator
                RTS            ; implied

Directives:
    .org $8000      — set origin address
    .byte $FF       — emit raw byte(s), comma-separated
    .word $FFFC     — emit 16-bit word (little-endian)
"""

from __future__ import annotations

import re
from cpu_6502.opcodes import AddressingMode, OPCODE_TABLE, OpcodeInfo, OPERAND_SIZES


# ---------------------------------------------------------------------------
# Build reverse lookup: (mnemonic, addressing_mode) -> opcode byte
# ---------------------------------------------------------------------------

_MNEMONIC_MODE_TO_OPCODE: dict[tuple[str, AddressingMode], int] = {}
for _opcode, _info in OPCODE_TABLE.items():
    _MNEMONIC_MODE_TO_OPCODE[(_info.mnemonic, _info.mode)] = _opcode


# ---------------------------------------------------------------------------
# Addressing mode detection patterns
# ---------------------------------------------------------------------------

# Order matters: check more specific patterns first
_ADDR_MODE_PATTERNS: list[tuple[str, AddressingMode]] = [
    # Indexed indirect: ($nn,X)
    (r'^\(\$([0-9A-Fa-f]{1,2})\s*,\s*X\)$', AddressingMode.INDEXED_INDIRECT),
    # Indirect indexed: ($nn),Y
    (r'^\(\$([0-9A-Fa-f]{1,2})\)\s*,\s*Y$', AddressingMode.INDIRECT_INDEXED),
    # Indirect: ($nnnn)
    (r'^\(\$([0-9A-Fa-f]{3,4})\)$', AddressingMode.INDIRECT),
    # Immediate: #$nn or #nn
    (r'^#\$([0-9A-Fa-f]{1,2})$', AddressingMode.IMMEDIATE),
    (r'^#(\d+)$', AddressingMode.IMMEDIATE),
    # Zero page,X: $nn,X
    (r'^\$([0-9A-Fa-f]{1,2})\s*,\s*X$', AddressingMode.ZERO_PAGE_X),
    # Zero page,Y: $nn,Y
    (r'^\$([0-9A-Fa-f]{1,2})\s*,\s*Y$', AddressingMode.ZERO_PAGE_Y),
    # Absolute,X: $nnnn,X
    (r'^\$([0-9A-Fa-f]{3,4})\s*,\s*X$', AddressingMode.ABSOLUTE_X),
    # Absolute,Y: $nnnn,Y
    (r'^\$([0-9A-Fa-f]{3,4})\s*,\s*Y$', AddressingMode.ABSOLUTE_Y),
    # Zero page: $nn (1-2 hex digits)
    (r'^\$([0-9A-Fa-f]{1,2})$', AddressingMode.ZERO_PAGE),
    # Absolute: $nnnn (3-4 hex digits)
    (r'^\$([0-9A-Fa-f]{3,4})$', AddressingMode.ABSOLUTE),
    # Accumulator: A
    (r'^A$', AddressingMode.ACCUMULATOR),
]

# Branch instructions use relative addressing
_BRANCH_MNEMONICS = {'BCC', 'BCS', 'BEQ', 'BMI', 'BNE', 'BPL', 'BVC', 'BVS'}


class AssemblerError(Exception):
    """Raised when assembly fails."""

    def __init__(self, message: str, line_num: int = 0):
        self.line_num = line_num
        super().__init__(f"Line {line_num}: {message}" if line_num else message)


class Assembler:
    """Two-pass 6502 assembler.

    Pass 1: Scan for labels and record their addresses.
    Pass 2: Emit machine code bytes, resolving label references.
    """

    def __init__(self) -> None:
        self.symbols: dict[str, int] = {}
        self.origin: int = 0

    def assemble(self, source: str) -> bytes:
        """Assemble 6502 source code to machine code bytes.

        Args:
            source: Assembly source code string.

        Returns:
            Assembled machine code as bytes.

        Raises:
            AssemblerError: If the source contains syntax errors or
                undefined labels.
        """
        lines = source.split('\n')
        self.symbols = {}

        # Parse lines into structured form
        parsed = self._parse_lines(lines)

        # Pass 1: determine addresses and collect labels
        self._pass1(parsed)

        # Pass 2: emit bytes
        return self._pass2(parsed)

    def _parse_lines(self, lines: list[str]) -> list[dict]:
        """Parse raw source lines into structured records."""
        parsed = []
        for i, line in enumerate(lines, 1):
            # Strip comments
            if ';' in line:
                line = line[:line.index(';')]
            line = line.strip()
            if not line:
                continue

            record: dict = {'line_num': i, 'label': None, 'mnemonic': None,
                           'operand_str': None, 'directive': None, 'dir_args': None}

            # Check for label
            if ':' in line:
                parts = line.split(':', 1)
                record['label'] = parts[0].strip()
                line = parts[1].strip()
                if not line:
                    parsed.append(record)
                    continue

            # Check for directive
            if line.startswith('.'):
                parts = line.split(None, 1)
                record['directive'] = parts[0].lower()
                record['dir_args'] = parts[1].strip() if len(parts) > 1 else ''
                parsed.append(record)
                continue

            # Must be an instruction
            parts = line.split(None, 1)
            record['mnemonic'] = parts[0].upper()
            record['operand_str'] = parts[1].strip() if len(parts) > 1 else None
            parsed.append(record)

        return parsed

    def _pass1(self, parsed: list[dict]) -> None:
        """Pass 1: Assign addresses to all labels."""
        pc = 0
        origin_set = False

        for record in parsed:
            # Handle .org before recording label at this position
            if record['directive'] == '.org':
                pc = self._parse_value(record['dir_args'], record['line_num'])
                if not origin_set:
                    self.origin = pc
                    origin_set = True

            if record['label']:
                self.symbols[record['label']] = pc

            if record['directive']:
                if record['directive'] == '.org':
                    pass  # already handled
                elif record['directive'] == '.byte':
                    values = self._parse_byte_args(record['dir_args'], record['line_num'])
                    pc += len(values)
                elif record['directive'] == '.word':
                    values = self._parse_word_args(record['dir_args'], record['line_num'])
                    pc += len(values) * 2
            elif record['mnemonic']:
                size = self._instruction_size(record['mnemonic'], record['operand_str'],
                                             record['line_num'])
                pc += size

    def _pass2(self, parsed: list[dict]) -> bytes:
        """Pass 2: Emit machine code bytes."""
        output = bytearray()
        pc = self.origin
        current_origin = self.origin

        for record in parsed:
            if record['directive'] == '.org':
                new_origin = self._parse_value(record['dir_args'], record['line_num'])
                # If there's a gap, fill with zeros
                if new_origin > pc:
                    output.extend(b'\x00' * (new_origin - pc))
                pc = new_origin
                if not output:
                    current_origin = new_origin
                    self.origin = new_origin
                continue

            if record['directive'] == '.byte':
                values = self._parse_byte_args(record['dir_args'], record['line_num'])
                output.extend(values)
                pc += len(values)
                continue

            if record['directive'] == '.word':
                values = self._parse_word_args(record['dir_args'], record['line_num'])
                for v in values:
                    output.append(v & 0xFF)
                    output.append((v >> 8) & 0xFF)
                    pc += 2
                continue

            if record['directive']:
                continue

            if not record['mnemonic']:
                continue

            # Encode instruction
            mnemonic = record['mnemonic']
            operand_str = record['operand_str']

            mode, value = self._resolve_operand(mnemonic, operand_str, pc, record['line_num'])
            opcode = self._find_opcode(mnemonic, mode, record['line_num'])

            output.append(opcode)
            pc += 1

            operand_size = OPERAND_SIZES[mode]
            if operand_size == 1:
                if mode == AddressingMode.RELATIVE:
                    # Convert absolute target to relative offset
                    offset = value - (pc + 1)
                    if offset < -128 or offset > 127:
                        raise AssemblerError(
                            f"Branch target out of range: offset {offset}", record['line_num']
                        )
                    output.append(offset & 0xFF)
                else:
                    output.append(value & 0xFF)
                pc += 1
            elif operand_size == 2:
                output.append(value & 0xFF)
                output.append((value >> 8) & 0xFF)
                pc += 2

        return bytes(output)

    def _resolve_operand(self, mnemonic: str, operand_str: str | None,
                         pc: int, line_num: int) -> tuple[AddressingMode, int]:
        """Resolve operand string to addressing mode and numeric value."""
        if operand_str is None or operand_str == '':
            # Implied mode
            return AddressingMode.IMPLIED, 0

        # Check if operand_str is 'A' for accumulator mode
        if operand_str.upper() == 'A' and mnemonic in ('ASL', 'LSR', 'ROL', 'ROR'):
            return AddressingMode.ACCUMULATOR, 0

        # Branch instructions: operand is a label or value
        if mnemonic in _BRANCH_MNEMONICS:
            value = self._resolve_label_or_value(operand_str, line_num)
            return AddressingMode.RELATIVE, value

        # Try each addressing mode pattern
        for pattern, mode in _ADDR_MODE_PATTERNS:
            m = re.match(pattern, operand_str, re.IGNORECASE)
            if m:
                value_str = m.group(1) if m.lastindex else ''
                if pattern.startswith(r'^#(\d'):
                    value = int(value_str)
                elif value_str:
                    value = int(value_str, 16)
                else:
                    value = 0
                return mode, value

        # Check for label references (absolute or zero page)
        # Label with ,X or ,Y
        label_xy = re.match(r'^(\w+)\s*,\s*([XY])$', operand_str, re.IGNORECASE)
        if label_xy:
            label = label_xy.group(1)
            index_reg = label_xy.group(2).upper()
            value = self._resolve_label_or_value(label, line_num)
            if value <= 0xFF:
                mode = AddressingMode.ZERO_PAGE_X if index_reg == 'X' else AddressingMode.ZERO_PAGE_Y
            else:
                mode = AddressingMode.ABSOLUTE_X if index_reg == 'X' else AddressingMode.ABSOLUTE_Y
            return mode, value

        # Indirect with label: (label)
        indirect_label = re.match(r'^\((\w+)\)$', operand_str)
        if indirect_label:
            value = self._resolve_label_or_value(indirect_label.group(1), line_num)
            return AddressingMode.INDIRECT, value

        # Plain label — absolute or zero page
        value = self._resolve_label_or_value(operand_str, line_num)
        if value <= 0xFF and (mnemonic, AddressingMode.ZERO_PAGE) in _MNEMONIC_MODE_TO_OPCODE:
            return AddressingMode.ZERO_PAGE, value
        return AddressingMode.ABSOLUTE, value

    def _resolve_label_or_value(self, s: str, line_num: int) -> int:
        """Resolve a string that's either a hex value ($xx), decimal, or label name."""
        s = s.strip()
        if s.startswith('$'):
            return int(s[1:], 16)
        if s.isdigit():
            return int(s)
        if s in self.symbols:
            return self.symbols[s]
        raise AssemblerError(f"Undefined symbol: '{s}'", line_num)

    def _find_opcode(self, mnemonic: str, mode: AddressingMode, line_num: int) -> int:
        """Find the opcode byte for a mnemonic + addressing mode combination."""
        key = (mnemonic, mode)
        if key in _MNEMONIC_MODE_TO_OPCODE:
            return _MNEMONIC_MODE_TO_OPCODE[key]
        raise AssemblerError(
            f"Invalid addressing mode {mode.value} for {mnemonic}", line_num
        )

    def _instruction_size(self, mnemonic: str, operand_str: str | None, line_num: int) -> int:
        """Determine instruction size in bytes (for pass 1)."""
        if operand_str is None or operand_str == '':
            return 1  # Implied

        if operand_str.upper() == 'A' and mnemonic in ('ASL', 'LSR', 'ROL', 'ROR'):
            return 1  # Accumulator

        if mnemonic in _BRANCH_MNEMONICS:
            return 2  # Relative

        # Try patterns to determine size
        for pattern, mode in _ADDR_MODE_PATTERNS:
            m = re.match(pattern, operand_str, re.IGNORECASE)
            if m:
                return 1 + OPERAND_SIZES[mode]

        # Label references — check if it could be zero page
        label_xy = re.match(r'^(\w+)\s*,\s*[XY]$', operand_str, re.IGNORECASE)
        if label_xy:
            label = label_xy.group(1)
            if label in self.symbols and self.symbols[label] <= 0xFF:
                return 2  # zero page + index
            return 3  # assume absolute + index

        indirect_label = re.match(r'^\((\w+)\)$', operand_str)
        if indirect_label:
            return 3  # indirect (JMP)

        # Plain label — check if in symbol table from earlier in pass 1
        s = operand_str.strip()
        if s.startswith('$'):
            hex_val = s[1:].split(',')[0]
            if len(hex_val) <= 2:
                return 2
            return 3

        # For forward references, assume absolute (3 bytes)
        if s in self.symbols and self.symbols[s] <= 0xFF:
            if (mnemonic, AddressingMode.ZERO_PAGE) in _MNEMONIC_MODE_TO_OPCODE:
                return 2
        return 3

    def _parse_value(self, s: str, line_num: int) -> int:
        """Parse a numeric value from directive argument."""
        s = s.strip()
        if s.startswith('$'):
            return int(s[1:], 16)
        if s.startswith('0x') or s.startswith('0X'):
            return int(s, 16)
        return int(s)

    def _parse_byte_args(self, args_str: str, line_num: int) -> list[int]:
        """Parse .byte directive arguments (comma-separated values)."""
        parts = [p.strip() for p in args_str.split(',')]
        result = []
        for p in parts:
            if not p:
                continue
            if p.startswith('"') or p.startswith("'"):
                # String literal
                text = p[1:-1]
                result.extend(ord(c) for c in text)
            else:
                result.append(self._parse_value(p, line_num) & 0xFF)
        return result

    def _parse_word_args(self, args_str: str, line_num: int) -> list[int]:
        """Parse .word directive arguments (comma-separated 16-bit values)."""
        parts = [p.strip() for p in args_str.split(',')]
        result = []
        for p in parts:
            if not p:
                continue
            result.append(self._parse_value(p, line_num) & 0xFFFF)
        return result
