"""6502 disassembler.

Converts machine code bytes back into human-readable assembly language.
Produces output in the format: "$8000: A9 42    LDA #$42"
"""

from __future__ import annotations

from cpu_6502.memory import Memory
from cpu_6502.opcodes import AddressingMode, OPCODE_TABLE, OPERAND_SIZES


def disassemble(memory: Memory, start: int, count: int = 16) -> list[str]:
    """Disassemble `count` instructions starting at `start`.

    Args:
        memory: Memory instance to read from.
        start: Starting address for disassembly.
        count: Number of instructions to disassemble.

    Returns:
        List of formatted disassembly strings, e.g.:
        ["$8000: A9 42    LDA #$42", "$8002: 8D 00 60 STA $6000"]
    """
    lines: list[str] = []
    pc = start & 0xFFFF

    for _ in range(count):
        addr = pc
        opcode_byte = memory.read(pc)
        pc = (pc + 1) & 0xFFFF

        if opcode_byte not in OPCODE_TABLE:
            # Unknown opcode — show as raw byte
            lines.append(f"${addr:04X}: {opcode_byte:02X}       ???")
            continue

        info = OPCODE_TABLE[opcode_byte]
        operand_size = OPERAND_SIZES[info.mode]

        # Read operand bytes
        raw_bytes = [opcode_byte]
        operand = 0
        if operand_size == 1:
            operand = memory.read(pc)
            raw_bytes.append(operand)
            pc = (pc + 1) & 0xFFFF
        elif operand_size == 2:
            lo = memory.read(pc)
            hi = memory.read((pc + 1) & 0xFFFF)
            operand = (hi << 8) | lo
            raw_bytes.extend([lo, hi])
            pc = (pc + 2) & 0xFFFF

        # Format hex bytes column (up to 3 bytes, padded to 8 chars)
        hex_str = ' '.join(f'{b:02X}' for b in raw_bytes)
        hex_col = f"{hex_str:<8}"

        # Format operand based on addressing mode
        operand_str = _format_operand(info.mode, operand, pc)

        lines.append(f"${addr:04X}: {hex_col} {info.mnemonic} {operand_str}".rstrip())

    return lines


def disassemble_one(memory: Memory, pc: int) -> tuple[str, int]:
    """Disassemble a single instruction at pc.

    Args:
        memory: Memory instance.
        pc: Address of the instruction.

    Returns:
        Tuple of (formatted string, next_pc).
    """
    lines = disassemble(memory, pc, count=1)
    opcode_byte = memory.read(pc)
    if opcode_byte in OPCODE_TABLE:
        size = OPCODE_TABLE[opcode_byte].bytes
    else:
        size = 1
    return lines[0] if lines else f"${pc:04X}: ??? ", (pc + size) & 0xFFFF


def _format_operand(mode: AddressingMode, operand: int, next_pc: int) -> str:
    """Format the operand portion of a disassembled instruction."""
    if mode == AddressingMode.IMPLIED:
        return ""
    elif mode == AddressingMode.ACCUMULATOR:
        return "A"
    elif mode == AddressingMode.IMMEDIATE:
        return f"#${operand:02X}"
    elif mode == AddressingMode.ZERO_PAGE:
        return f"${operand:02X}"
    elif mode == AddressingMode.ZERO_PAGE_X:
        return f"${operand:02X},X"
    elif mode == AddressingMode.ZERO_PAGE_Y:
        return f"${operand:02X},Y"
    elif mode == AddressingMode.ABSOLUTE:
        return f"${operand:04X}"
    elif mode == AddressingMode.ABSOLUTE_X:
        return f"${operand:04X},X"
    elif mode == AddressingMode.ABSOLUTE_Y:
        return f"${operand:04X},Y"
    elif mode == AddressingMode.INDIRECT:
        return f"(${operand:04X})"
    elif mode == AddressingMode.INDEXED_INDIRECT:
        return f"(${operand:02X},X)"
    elif mode == AddressingMode.INDIRECT_INDEXED:
        return f"(${operand:02X}),Y"
    elif mode == AddressingMode.RELATIVE:
        # Show target address
        offset = operand if operand < 128 else operand - 256
        target = (next_pc + offset) & 0xFFFF
        return f"${target:04X}"
    return ""
