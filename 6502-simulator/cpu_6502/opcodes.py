"""6502 opcode table and instruction decoder.

Contains the complete table of all 151 documented MOS 6502 opcodes,
organized by instruction mnemonic. Each entry maps an opcode byte to its
mnemonic, addressing mode, cycle count, and instruction length in bytes.

Reference: http://www.6502.org/tutorials/6502opcodes.html
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from cpu_6502.memory import Memory


# ---------------------------------------------------------------------------
# Addressing modes
# ---------------------------------------------------------------------------

class AddressingMode(Enum):
    """All 13 addressing modes of the MOS 6502."""

    IMPLIED = "imp"          # No operand (e.g. CLC, RTS)
    ACCUMULATOR = "acc"      # Operates on A register (e.g. ASL A)
    IMMEDIATE = "imm"        # 1-byte literal (e.g. LDA #$44)
    ZERO_PAGE = "zpg"        # 1-byte address in page zero (e.g. LDA $44)
    ZERO_PAGE_X = "zpx"      # Zero page + X (e.g. LDA $44,X)
    ZERO_PAGE_Y = "zpy"      # Zero page + Y (e.g. LDX $44,Y)
    ABSOLUTE = "abs"         # 2-byte address (e.g. LDA $4400)
    ABSOLUTE_X = "abx"       # Absolute + X (e.g. LDA $4400,X)
    ABSOLUTE_Y = "aby"       # Absolute + Y (e.g. LDA $4400,Y)
    INDIRECT = "ind"         # 2-byte pointer, JMP only (e.g. JMP ($FFFC))
    INDEXED_INDIRECT = "izx" # (Indirect,X) — (zp,X) (e.g. LDA ($44,X))
    INDIRECT_INDEXED = "izy" # (Indirect),Y — (zp),Y (e.g. LDA ($44),Y)
    RELATIVE = "rel"         # Signed 1-byte branch offset (e.g. BNE label)


# ---------------------------------------------------------------------------
# Opcode info
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class OpcodeInfo:
    """Metadata for a single 6502 opcode.

    Attributes:
        mnemonic: Three-letter instruction name (e.g. "LDA").
        mode: Addressing mode used by this opcode variant.
        cycles: Base cycle count (page-crossing penalties added at runtime).
        bytes: Total instruction length including opcode byte (1, 2, or 3).
    """

    mnemonic: str
    mode: AddressingMode
    cycles: int
    bytes: int


# ---------------------------------------------------------------------------
# Operand sizes per addressing mode
# ---------------------------------------------------------------------------

OPERAND_SIZES: dict[AddressingMode, int] = {
    AddressingMode.IMPLIED: 0,
    AddressingMode.ACCUMULATOR: 0,
    AddressingMode.IMMEDIATE: 1,
    AddressingMode.ZERO_PAGE: 1,
    AddressingMode.ZERO_PAGE_X: 1,
    AddressingMode.ZERO_PAGE_Y: 1,
    AddressingMode.RELATIVE: 1,
    AddressingMode.ABSOLUTE: 2,
    AddressingMode.ABSOLUTE_X: 2,
    AddressingMode.ABSOLUTE_Y: 2,
    AddressingMode.INDIRECT: 2,
    AddressingMode.INDEXED_INDIRECT: 1,
    AddressingMode.INDIRECT_INDEXED: 1,
}


# ---------------------------------------------------------------------------
# Complete opcode table — all 151 documented 6502 opcodes
# ---------------------------------------------------------------------------

# Shorthand aliases for readability
_IMP = AddressingMode.IMPLIED
_ACC = AddressingMode.ACCUMULATOR
_IMM = AddressingMode.IMMEDIATE
_ZPG = AddressingMode.ZERO_PAGE
_ZPX = AddressingMode.ZERO_PAGE_X
_ZPY = AddressingMode.ZERO_PAGE_Y
_ABS = AddressingMode.ABSOLUTE
_ABX = AddressingMode.ABSOLUTE_X
_ABY = AddressingMode.ABSOLUTE_Y
_IND = AddressingMode.INDIRECT
_IZX = AddressingMode.INDEXED_INDIRECT
_IZY = AddressingMode.INDIRECT_INDEXED
_REL = AddressingMode.RELATIVE

OPCODE_TABLE: dict[int, OpcodeInfo] = {
    # ===========================================================================
    # Load / Store Operations
    # ===========================================================================

    # LDA — Load Accumulator
    0xA9: OpcodeInfo("LDA", _IMM, 2, 2),
    0xA5: OpcodeInfo("LDA", _ZPG, 3, 2),
    0xB5: OpcodeInfo("LDA", _ZPX, 4, 2),
    0xAD: OpcodeInfo("LDA", _ABS, 4, 3),
    0xBD: OpcodeInfo("LDA", _ABX, 4, 3),  # +1 if page crossed
    0xB9: OpcodeInfo("LDA", _ABY, 4, 3),  # +1 if page crossed
    0xA1: OpcodeInfo("LDA", _IZX, 6, 2),
    0xB1: OpcodeInfo("LDA", _IZY, 5, 2),  # +1 if page crossed

    # LDX — Load X Register
    0xA2: OpcodeInfo("LDX", _IMM, 2, 2),
    0xA6: OpcodeInfo("LDX", _ZPG, 3, 2),
    0xB6: OpcodeInfo("LDX", _ZPY, 4, 2),
    0xAE: OpcodeInfo("LDX", _ABS, 4, 3),
    0xBE: OpcodeInfo("LDX", _ABY, 4, 3),  # +1 if page crossed

    # LDY — Load Y Register
    0xA0: OpcodeInfo("LDY", _IMM, 2, 2),
    0xA4: OpcodeInfo("LDY", _ZPG, 3, 2),
    0xB4: OpcodeInfo("LDY", _ZPX, 4, 2),
    0xAC: OpcodeInfo("LDY", _ABS, 4, 3),
    0xBC: OpcodeInfo("LDY", _ABX, 4, 3),  # +1 if page crossed

    # STA — Store Accumulator
    0x85: OpcodeInfo("STA", _ZPG, 3, 2),
    0x95: OpcodeInfo("STA", _ZPX, 4, 2),
    0x8D: OpcodeInfo("STA", _ABS, 4, 3),
    0x9D: OpcodeInfo("STA", _ABX, 5, 3),
    0x99: OpcodeInfo("STA", _ABY, 5, 3),
    0x81: OpcodeInfo("STA", _IZX, 6, 2),
    0x91: OpcodeInfo("STA", _IZY, 6, 2),

    # STX — Store X Register
    0x86: OpcodeInfo("STX", _ZPG, 3, 2),
    0x96: OpcodeInfo("STX", _ZPY, 4, 2),
    0x8E: OpcodeInfo("STX", _ABS, 4, 3),

    # STY — Store Y Register
    0x84: OpcodeInfo("STY", _ZPG, 3, 2),
    0x94: OpcodeInfo("STY", _ZPX, 4, 2),
    0x8C: OpcodeInfo("STY", _ABS, 4, 3),

    # ===========================================================================
    # Register Transfers
    # ===========================================================================

    # TAX — Transfer A to X
    0xAA: OpcodeInfo("TAX", _IMP, 2, 1),
    # TAY — Transfer A to Y
    0xA8: OpcodeInfo("TAY", _IMP, 2, 1),
    # TXA — Transfer X to A
    0x8A: OpcodeInfo("TXA", _IMP, 2, 1),
    # TYA — Transfer Y to A
    0x98: OpcodeInfo("TYA", _IMP, 2, 1),

    # ===========================================================================
    # Stack Operations
    # ===========================================================================

    # TSX — Transfer Stack Pointer to X
    0xBA: OpcodeInfo("TSX", _IMP, 2, 1),
    # TXS — Transfer X to Stack Pointer
    0x9A: OpcodeInfo("TXS", _IMP, 2, 1),
    # PHA — Push Accumulator
    0x48: OpcodeInfo("PHA", _IMP, 3, 1),
    # PHP — Push Processor Status
    0x08: OpcodeInfo("PHP", _IMP, 3, 1),
    # PLA — Pull Accumulator
    0x68: OpcodeInfo("PLA", _IMP, 4, 1),
    # PLP — Pull Processor Status
    0x28: OpcodeInfo("PLP", _IMP, 4, 1),

    # ===========================================================================
    # Logical Operations
    # ===========================================================================

    # AND — Logical AND
    0x29: OpcodeInfo("AND", _IMM, 2, 2),
    0x25: OpcodeInfo("AND", _ZPG, 3, 2),
    0x35: OpcodeInfo("AND", _ZPX, 4, 2),
    0x2D: OpcodeInfo("AND", _ABS, 4, 3),
    0x3D: OpcodeInfo("AND", _ABX, 4, 3),  # +1 if page crossed
    0x39: OpcodeInfo("AND", _ABY, 4, 3),  # +1 if page crossed
    0x21: OpcodeInfo("AND", _IZX, 6, 2),
    0x31: OpcodeInfo("AND", _IZY, 5, 2),  # +1 if page crossed

    # EOR — Exclusive OR
    0x49: OpcodeInfo("EOR", _IMM, 2, 2),
    0x45: OpcodeInfo("EOR", _ZPG, 3, 2),
    0x55: OpcodeInfo("EOR", _ZPX, 4, 2),
    0x4D: OpcodeInfo("EOR", _ABS, 4, 3),
    0x5D: OpcodeInfo("EOR", _ABX, 4, 3),  # +1 if page crossed
    0x59: OpcodeInfo("EOR", _ABY, 4, 3),  # +1 if page crossed
    0x41: OpcodeInfo("EOR", _IZX, 6, 2),
    0x51: OpcodeInfo("EOR", _IZY, 5, 2),  # +1 if page crossed

    # ORA — Logical Inclusive OR
    0x09: OpcodeInfo("ORA", _IMM, 2, 2),
    0x05: OpcodeInfo("ORA", _ZPG, 3, 2),
    0x15: OpcodeInfo("ORA", _ZPX, 4, 2),
    0x0D: OpcodeInfo("ORA", _ABS, 4, 3),
    0x1D: OpcodeInfo("ORA", _ABX, 4, 3),  # +1 if page crossed
    0x19: OpcodeInfo("ORA", _ABY, 4, 3),  # +1 if page crossed
    0x01: OpcodeInfo("ORA", _IZX, 6, 2),
    0x11: OpcodeInfo("ORA", _IZY, 5, 2),  # +1 if page crossed

    # BIT — Bit Test
    0x24: OpcodeInfo("BIT", _ZPG, 3, 2),
    0x2C: OpcodeInfo("BIT", _ABS, 4, 3),

    # ===========================================================================
    # Arithmetic Operations
    # ===========================================================================

    # ADC — Add with Carry
    0x69: OpcodeInfo("ADC", _IMM, 2, 2),
    0x65: OpcodeInfo("ADC", _ZPG, 3, 2),
    0x75: OpcodeInfo("ADC", _ZPX, 4, 2),
    0x6D: OpcodeInfo("ADC", _ABS, 4, 3),
    0x7D: OpcodeInfo("ADC", _ABX, 4, 3),  # +1 if page crossed
    0x79: OpcodeInfo("ADC", _ABY, 4, 3),  # +1 if page crossed
    0x61: OpcodeInfo("ADC", _IZX, 6, 2),
    0x71: OpcodeInfo("ADC", _IZY, 5, 2),  # +1 if page crossed

    # SBC — Subtract with Carry
    0xE9: OpcodeInfo("SBC", _IMM, 2, 2),
    0xE5: OpcodeInfo("SBC", _ZPG, 3, 2),
    0xF5: OpcodeInfo("SBC", _ZPX, 4, 2),
    0xED: OpcodeInfo("SBC", _ABS, 4, 3),
    0xFD: OpcodeInfo("SBC", _ABX, 4, 3),  # +1 if page crossed
    0xF9: OpcodeInfo("SBC", _ABY, 4, 3),  # +1 if page crossed
    0xE1: OpcodeInfo("SBC", _IZX, 6, 2),
    0xF1: OpcodeInfo("SBC", _IZY, 5, 2),  # +1 if page crossed

    # CMP — Compare Accumulator
    0xC9: OpcodeInfo("CMP", _IMM, 2, 2),
    0xC5: OpcodeInfo("CMP", _ZPG, 3, 2),
    0xD5: OpcodeInfo("CMP", _ZPX, 4, 2),
    0xCD: OpcodeInfo("CMP", _ABS, 4, 3),
    0xDD: OpcodeInfo("CMP", _ABX, 4, 3),  # +1 if page crossed
    0xD9: OpcodeInfo("CMP", _ABY, 4, 3),  # +1 if page crossed
    0xC1: OpcodeInfo("CMP", _IZX, 6, 2),
    0xD1: OpcodeInfo("CMP", _IZY, 5, 2),  # +1 if page crossed

    # CPX — Compare X Register
    0xE0: OpcodeInfo("CPX", _IMM, 2, 2),
    0xE4: OpcodeInfo("CPX", _ZPG, 3, 2),
    0xEC: OpcodeInfo("CPX", _ABS, 4, 3),

    # CPY — Compare Y Register
    0xC0: OpcodeInfo("CPY", _IMM, 2, 2),
    0xC4: OpcodeInfo("CPY", _ZPG, 3, 2),
    0xCC: OpcodeInfo("CPY", _ABS, 4, 3),

    # ===========================================================================
    # Increments & Decrements
    # ===========================================================================

    # INC — Increment Memory
    0xE6: OpcodeInfo("INC", _ZPG, 5, 2),
    0xF6: OpcodeInfo("INC", _ZPX, 6, 2),
    0xEE: OpcodeInfo("INC", _ABS, 6, 3),
    0xFE: OpcodeInfo("INC", _ABX, 7, 3),

    # INX — Increment X
    0xE8: OpcodeInfo("INX", _IMP, 2, 1),
    # INY — Increment Y
    0xC8: OpcodeInfo("INY", _IMP, 2, 1),

    # DEC — Decrement Memory
    0xC6: OpcodeInfo("DEC", _ZPG, 5, 2),
    0xD6: OpcodeInfo("DEC", _ZPX, 6, 2),
    0xCE: OpcodeInfo("DEC", _ABS, 6, 3),
    0xDE: OpcodeInfo("DEC", _ABX, 7, 3),

    # DEX — Decrement X
    0xCA: OpcodeInfo("DEX", _IMP, 2, 1),
    # DEY — Decrement Y
    0x88: OpcodeInfo("DEY", _IMP, 2, 1),

    # ===========================================================================
    # Shifts & Rotates
    # ===========================================================================

    # ASL — Arithmetic Shift Left
    0x0A: OpcodeInfo("ASL", _ACC, 2, 1),
    0x06: OpcodeInfo("ASL", _ZPG, 5, 2),
    0x16: OpcodeInfo("ASL", _ZPX, 6, 2),
    0x0E: OpcodeInfo("ASL", _ABS, 6, 3),
    0x1E: OpcodeInfo("ASL", _ABX, 7, 3),

    # LSR — Logical Shift Right
    0x4A: OpcodeInfo("LSR", _ACC, 2, 1),
    0x46: OpcodeInfo("LSR", _ZPG, 5, 2),
    0x56: OpcodeInfo("LSR", _ZPX, 6, 2),
    0x4E: OpcodeInfo("LSR", _ABS, 6, 3),
    0x5E: OpcodeInfo("LSR", _ABX, 7, 3),

    # ROL — Rotate Left
    0x2A: OpcodeInfo("ROL", _ACC, 2, 1),
    0x26: OpcodeInfo("ROL", _ZPG, 5, 2),
    0x36: OpcodeInfo("ROL", _ZPX, 6, 2),
    0x2E: OpcodeInfo("ROL", _ABS, 6, 3),
    0x3E: OpcodeInfo("ROL", _ABX, 7, 3),

    # ROR — Rotate Right
    0x6A: OpcodeInfo("ROR", _ACC, 2, 1),
    0x66: OpcodeInfo("ROR", _ZPG, 5, 2),
    0x76: OpcodeInfo("ROR", _ZPX, 6, 2),
    0x6E: OpcodeInfo("ROR", _ABS, 6, 3),
    0x7E: OpcodeInfo("ROR", _ABX, 7, 3),

    # ===========================================================================
    # Jumps & Calls
    # ===========================================================================

    # JMP — Jump
    0x4C: OpcodeInfo("JMP", _ABS, 3, 3),
    0x6C: OpcodeInfo("JMP", _IND, 5, 3),

    # JSR — Jump to Subroutine
    0x20: OpcodeInfo("JSR", _ABS, 6, 3),

    # RTS — Return from Subroutine
    0x60: OpcodeInfo("RTS", _IMP, 6, 1),

    # ===========================================================================
    # Branches (all are 2 bytes: opcode + signed offset)
    # ===========================================================================

    # BCC — Branch if Carry Clear
    0x90: OpcodeInfo("BCC", _REL, 2, 2),  # +1 if taken, +2 if page crossed
    # BCS — Branch if Carry Set
    0xB0: OpcodeInfo("BCS", _REL, 2, 2),
    # BEQ — Branch if Equal (Zero set)
    0xF0: OpcodeInfo("BEQ", _REL, 2, 2),
    # BMI — Branch if Minus (Negative set)
    0x30: OpcodeInfo("BMI", _REL, 2, 2),
    # BNE — Branch if Not Equal (Zero clear)
    0xD0: OpcodeInfo("BNE", _REL, 2, 2),
    # BPL — Branch if Positive (Negative clear)
    0x10: OpcodeInfo("BPL", _REL, 2, 2),
    # BVC — Branch if Overflow Clear
    0x50: OpcodeInfo("BVC", _REL, 2, 2),
    # BVS — Branch if Overflow Set
    0x70: OpcodeInfo("BVS", _REL, 2, 2),

    # ===========================================================================
    # Status Flag Changes
    # ===========================================================================

    # CLC — Clear Carry
    0x18: OpcodeInfo("CLC", _IMP, 2, 1),
    # CLD — Clear Decimal
    0xD8: OpcodeInfo("CLD", _IMP, 2, 1),
    # CLI — Clear Interrupt Disable
    0x58: OpcodeInfo("CLI", _IMP, 2, 1),
    # CLV — Clear Overflow
    0xB8: OpcodeInfo("CLV", _IMP, 2, 1),
    # SEC — Set Carry
    0x38: OpcodeInfo("SEC", _IMP, 2, 1),
    # SED — Set Decimal
    0xF8: OpcodeInfo("SED", _IMP, 2, 1),
    # SEI — Set Interrupt Disable
    0x78: OpcodeInfo("SEI", _IMP, 2, 1),

    # ===========================================================================
    # System Functions
    # ===========================================================================

    # BRK — Force Interrupt
    0x00: OpcodeInfo("BRK", _IMP, 7, 1),
    # NOP — No Operation
    0xEA: OpcodeInfo("NOP", _IMP, 2, 1),
    # RTI — Return from Interrupt
    0x40: OpcodeInfo("RTI", _IMP, 6, 1),
}


# ---------------------------------------------------------------------------
# Decoder function
# ---------------------------------------------------------------------------

def decode(memory: Memory, pc: int) -> tuple[OpcodeInfo, int]:
    """Decode the instruction at the given program counter.

    Reads the opcode byte, looks up its metadata, then reads the operand
    bytes (0, 1, or 2 depending on the addressing mode).

    Args:
        memory: The memory bus to read from.
        pc: Address of the opcode byte.

    Returns:
        A tuple of (OpcodeInfo, operand) where operand is:
        - 0 for implied/accumulator modes
        - 8-bit value for immediate/zero-page/relative modes
        - 16-bit value for absolute/indirect modes

    Raises:
        ValueError: If the opcode byte is not in the table (illegal opcode).
    """
    opcode_byte = memory.read(pc)

    if opcode_byte not in OPCODE_TABLE:
        raise ValueError(
            f"Illegal opcode: ${opcode_byte:02X} at address ${pc:04X}"
        )

    info = OPCODE_TABLE[opcode_byte]
    operand_size = OPERAND_SIZES[info.mode]

    operand: int = 0
    if operand_size == 1:
        operand = memory.read((pc + 1) & 0xFFFF)
    elif operand_size == 2:
        operand = memory.read_word((pc + 1) & 0xFFFF)

    return info, operand
