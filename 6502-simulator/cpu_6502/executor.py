"""Instruction execution engine for the 6502 CPU.

Implements all 56 official 6502 instructions across all addressing modes,
including BCD arithmetic for ADC/SBC when the Decimal flag is set.

The `step()` method is added to CPU6502 via monkey-patching at import time,
so importing this module augments the CPU class with execution capability.
"""

from __future__ import annotations

from cpu_6502.cpu import CPU6502
from cpu_6502.opcodes import AddressingMode, OPCODE_TABLE, OpcodeInfo


# ---------------------------------------------------------------------------
# Address resolution
# ---------------------------------------------------------------------------

def resolve_address(cpu: CPU6502, mode: AddressingMode, operand: int) -> tuple[int, bool]:
    """Resolve the effective address for a given addressing mode.

    Args:
        cpu: The CPU instance (for registers and memory access).
        mode: The addressing mode of the instruction.
        operand: The raw operand bytes fetched after the opcode.

    Returns:
        A tuple of (effective_address, page_crossed).
        For IMMEDIATE mode, the address is meaningless — callers read
        the operand value directly. For ACCUMULATOR/IMPLIED, returns (0, False).
    """
    state = cpu.state
    page_crossed = False

    if mode == AddressingMode.IMMEDIATE:
        # Operand IS the value; we return a sentinel that callers handle
        return operand, False

    elif mode == AddressingMode.ZERO_PAGE:
        return operand & 0xFF, False

    elif mode == AddressingMode.ZERO_PAGE_X:
        return (operand + state.x) & 0xFF, False

    elif mode == AddressingMode.ZERO_PAGE_Y:
        return (operand + state.y) & 0xFF, False

    elif mode == AddressingMode.ABSOLUTE:
        return operand & 0xFFFF, False

    elif mode == AddressingMode.ABSOLUTE_X:
        addr = (operand + state.x) & 0xFFFF
        page_crossed = (operand & 0xFF00) != (addr & 0xFF00)
        return addr, page_crossed

    elif mode == AddressingMode.ABSOLUTE_Y:
        addr = (operand + state.y) & 0xFFFF
        page_crossed = (operand & 0xFF00) != (addr & 0xFF00)
        return addr, page_crossed

    elif mode == AddressingMode.INDIRECT:
        # JMP (indirect) with the page-boundary bug
        return cpu.memory.read_word_bug(operand), False

    elif mode == AddressingMode.INDEXED_INDIRECT:
        # (zp,X): pointer at (operand + X) in zero page
        ptr = (operand + state.x) & 0xFF
        lo = cpu.memory.read(ptr)
        hi = cpu.memory.read((ptr + 1) & 0xFF)
        return (hi << 8) | lo, False

    elif mode == AddressingMode.INDIRECT_INDEXED:
        # (zp),Y: pointer at operand in zero page, then + Y
        lo = cpu.memory.read(operand & 0xFF)
        hi = cpu.memory.read((operand + 1) & 0xFF)
        base = (hi << 8) | lo
        addr = (base + state.y) & 0xFFFF
        page_crossed = (base & 0xFF00) != (addr & 0xFF00)
        return addr, page_crossed

    elif mode == AddressingMode.RELATIVE:
        # Offset is signed byte; relative to PC after fetching operand
        return operand, False

    # IMPLIED or ACCUMULATOR
    return 0, False


def read_operand(cpu: CPU6502, mode: AddressingMode, addr: int, operand: int) -> int:
    """Read the effective operand value.

    For IMMEDIATE mode, the value is the operand itself.
    For ACCUMULATOR, the value is the A register.
    For memory modes, reads from the effective address.
    """
    if mode == AddressingMode.IMMEDIATE:
        return operand & 0xFF
    elif mode == AddressingMode.ACCUMULATOR:
        return cpu.state.a
    else:
        return cpu.memory.read(addr)


# ---------------------------------------------------------------------------
# Instruction implementations
# ---------------------------------------------------------------------------

def _adc(cpu: CPU6502, value: int) -> None:
    """Add with Carry (binary and BCD modes)."""
    state = cpu.state
    a = state.a

    if state.d:
        # BCD mode
        lo = (a & 0x0F) + (value & 0x0F) + int(state.c)
        if lo > 9:
            lo += 6
        hi = (a >> 4) + (value >> 4) + (1 if lo > 0x0F else 0)
        lo &= 0x0F

        # Overflow detection uses binary interpretation
        bin_result = a + value + int(state.c)
        state.v = bool(~(a ^ value) & (a ^ (hi << 4)) & 0x80)

        if hi > 9:
            hi += 6
        state.c = hi > 0x0F
        hi &= 0x0F

        result = (hi << 4) | lo
        state.a = result & 0xFF
        state.n = bool(result & 0x80)
        state.z = (bin_result & 0xFF) == 0
    else:
        # Binary mode
        result = a + value + int(state.c)
        state.c = result > 0xFF
        result &= 0xFF
        state.v = bool(~(a ^ value) & (a ^ result) & 0x80)
        state.a = result
        state.update_nz(result)


def _sbc(cpu: CPU6502, value: int) -> None:
    """Subtract with Carry (binary and BCD modes)."""
    state = cpu.state
    a = state.a

    if state.d:
        # BCD mode
        lo = (a & 0x0F) - (value & 0x0F) - (0 if state.c else 1)
        if lo < 0:
            lo = ((lo - 6) & 0x0F) | 0x10  # borrow from high nibble
        hi = (a >> 4) - (value >> 4) - (1 if lo & 0x10 else 0)
        lo &= 0x0F
        if hi < 0:
            hi = (hi - 6) & 0x0F
            carry = False
        else:
            carry = True
            hi &= 0x0F

        result = (hi << 4) | lo
        # Flags are based on binary result for N and Z on NMOS 6502
        bin_result = a - value - (0 if state.c else 1)
        state.c = bin_result >= 0
        state.v = bool((a ^ value) & (a ^ (bin_result & 0xFF)) & 0x80)
        state.a = result & 0xFF
        state.n = bool(bin_result & 0x80)
        state.z = (bin_result & 0xFF) == 0
    else:
        # Binary mode — SBC is ADC with complement
        result = a + (value ^ 0xFF) + int(state.c)
        state.c = result > 0xFF
        result &= 0xFF
        state.v = bool((a ^ result) & ((value ^ 0xFF) ^ result) & 0x80)
        state.a = result
        state.update_nz(result)


def _compare(cpu: CPU6502, reg_value: int, operand_value: int) -> None:
    """CMP/CPX/CPY — compare register with memory."""
    result = reg_value - operand_value
    cpu.state.c = reg_value >= operand_value
    cpu.state.update_nz(result & 0xFF)


def _branch(cpu: CPU6502, condition: bool, offset: int) -> int:
    """Execute a branch instruction. Returns extra cycles consumed."""
    if not condition:
        return 0
    # Offset is signed byte
    if offset & 0x80:
        offset -= 256
    old_pc = cpu.state.pc
    cpu.state.pc = (cpu.state.pc + offset) & 0xFFFF
    # +1 for branch taken, +1 more if page crossed
    extra = 1
    if (old_pc & 0xFF00) != (cpu.state.pc & 0xFF00):
        extra += 1
    return extra


# ---------------------------------------------------------------------------
# Main execution step
# ---------------------------------------------------------------------------

def _step(cpu: CPU6502) -> int:
    """Execute one instruction and return cycles consumed.

    This method is attached to CPU6502 as `step()`.

    Returns:
        Number of clock cycles consumed by the instruction.

    Raises:
        ValueError: If an illegal opcode is encountered.
    """
    if cpu.halted:
        return 0

    state = cpu.state
    opcode_byte = cpu.fetch_byte()

    if opcode_byte not in OPCODE_TABLE:
        raise ValueError(f"Illegal opcode: ${opcode_byte:02X} at ${(state.pc - 1) & 0xFFFF:04X}")

    info = OPCODE_TABLE[opcode_byte]
    cycles = info.cycles
    extra_cycles = 0

    # Fetch operand bytes
    operand = 0
    if info.bytes == 2:
        operand = cpu.fetch_byte()
    elif info.bytes == 3:
        operand = cpu.fetch_word()

    # Resolve address
    addr, page_crossed = resolve_address(cpu, info.mode, operand)

    mnemonic = info.mnemonic

    # --- Load / Store ---
    if mnemonic == "LDA":
        val = read_operand(cpu, info.mode, addr, operand)
        state.a = val
        state.update_nz(val)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "LDX":
        val = read_operand(cpu, info.mode, addr, operand)
        state.x = val
        state.update_nz(val)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "LDY":
        val = read_operand(cpu, info.mode, addr, operand)
        state.y = val
        state.update_nz(val)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "STA":
        cpu.memory.write(addr, state.a)

    elif mnemonic == "STX":
        cpu.memory.write(addr, state.x)

    elif mnemonic == "STY":
        cpu.memory.write(addr, state.y)

    # --- Register Transfers ---
    elif mnemonic == "TAX":
        state.x = state.a
        state.update_nz(state.x)

    elif mnemonic == "TAY":
        state.y = state.a
        state.update_nz(state.y)

    elif mnemonic == "TXA":
        state.a = state.x
        state.update_nz(state.a)

    elif mnemonic == "TYA":
        state.a = state.y
        state.update_nz(state.a)

    elif mnemonic == "TSX":
        state.x = state.sp
        state.update_nz(state.x)

    elif mnemonic == "TXS":
        state.sp = state.x

    # --- Stack ---
    elif mnemonic == "PHA":
        cpu.push(state.a)

    elif mnemonic == "PHP":
        # PHP pushes status with B flag set
        cpu.push(state.status | 0x10)

    elif mnemonic == "PLA":
        state.a = cpu.pull()
        state.update_nz(state.a)

    elif mnemonic == "PLP":
        state.status = cpu.pull()

    # --- Logic ---
    elif mnemonic == "AND":
        val = read_operand(cpu, info.mode, addr, operand)
        state.a &= val
        state.update_nz(state.a)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "EOR":
        val = read_operand(cpu, info.mode, addr, operand)
        state.a ^= val
        state.update_nz(state.a)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "ORA":
        val = read_operand(cpu, info.mode, addr, operand)
        state.a |= val
        state.update_nz(state.a)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "BIT":
        val = cpu.memory.read(addr)
        state.z = (state.a & val) == 0
        state.n = bool(val & 0x80)
        state.v = bool(val & 0x40)

    # --- Arithmetic ---
    elif mnemonic == "ADC":
        val = read_operand(cpu, info.mode, addr, operand)
        _adc(cpu, val)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "SBC":
        val = read_operand(cpu, info.mode, addr, operand)
        _sbc(cpu, val)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "CMP":
        val = read_operand(cpu, info.mode, addr, operand)
        _compare(cpu, state.a, val)
        if page_crossed:
            extra_cycles += 1

    elif mnemonic == "CPX":
        val = read_operand(cpu, info.mode, addr, operand)
        _compare(cpu, state.x, val)

    elif mnemonic == "CPY":
        val = read_operand(cpu, info.mode, addr, operand)
        _compare(cpu, state.y, val)

    # --- Increment / Decrement ---
    elif mnemonic == "INC":
        val = (cpu.memory.read(addr) + 1) & 0xFF
        cpu.memory.write(addr, val)
        state.update_nz(val)

    elif mnemonic == "DEC":
        val = (cpu.memory.read(addr) - 1) & 0xFF
        cpu.memory.write(addr, val)
        state.update_nz(val)

    elif mnemonic == "INX":
        state.x = (state.x + 1) & 0xFF
        state.update_nz(state.x)

    elif mnemonic == "INY":
        state.y = (state.y + 1) & 0xFF
        state.update_nz(state.y)

    elif mnemonic == "DEX":
        state.x = (state.x - 1) & 0xFF
        state.update_nz(state.x)

    elif mnemonic == "DEY":
        state.y = (state.y - 1) & 0xFF
        state.update_nz(state.y)

    # --- Shifts ---
    elif mnemonic == "ASL":
        if info.mode == AddressingMode.ACCUMULATOR:
            state.c = bool(state.a & 0x80)
            state.a = (state.a << 1) & 0xFF
            state.update_nz(state.a)
        else:
            val = cpu.memory.read(addr)
            state.c = bool(val & 0x80)
            val = (val << 1) & 0xFF
            cpu.memory.write(addr, val)
            state.update_nz(val)

    elif mnemonic == "LSR":
        if info.mode == AddressingMode.ACCUMULATOR:
            state.c = bool(state.a & 0x01)
            state.a = state.a >> 1
            state.update_nz(state.a)
        else:
            val = cpu.memory.read(addr)
            state.c = bool(val & 0x01)
            val = val >> 1
            cpu.memory.write(addr, val)
            state.update_nz(val)

    elif mnemonic == "ROL":
        if info.mode == AddressingMode.ACCUMULATOR:
            old_c = int(state.c)
            state.c = bool(state.a & 0x80)
            state.a = ((state.a << 1) | old_c) & 0xFF
            state.update_nz(state.a)
        else:
            val = cpu.memory.read(addr)
            old_c = int(state.c)
            state.c = bool(val & 0x80)
            val = ((val << 1) | old_c) & 0xFF
            cpu.memory.write(addr, val)
            state.update_nz(val)

    elif mnemonic == "ROR":
        if info.mode == AddressingMode.ACCUMULATOR:
            old_c = int(state.c)
            state.c = bool(state.a & 0x01)
            state.a = (state.a >> 1) | (old_c << 7)
            state.update_nz(state.a)
        else:
            val = cpu.memory.read(addr)
            old_c = int(state.c)
            state.c = bool(val & 0x01)
            val = (val >> 1) | (old_c << 7)
            cpu.memory.write(addr, val)
            state.update_nz(val)

    # --- Jumps / Calls ---
    elif mnemonic == "JMP":
        state.pc = addr

    elif mnemonic == "JSR":
        # Push address of last byte of JSR instruction (PC - 1)
        cpu.push_word((state.pc - 1) & 0xFFFF)
        state.pc = addr

    elif mnemonic == "RTS":
        state.pc = (cpu.pull_word() + 1) & 0xFFFF

    elif mnemonic == "RTI":
        state.status = cpu.pull()
        state.pc = cpu.pull_word()

    # --- Branches ---
    elif mnemonic == "BCC":
        extra_cycles += _branch(cpu, not state.c, operand)

    elif mnemonic == "BCS":
        extra_cycles += _branch(cpu, state.c, operand)

    elif mnemonic == "BEQ":
        extra_cycles += _branch(cpu, state.z, operand)

    elif mnemonic == "BMI":
        extra_cycles += _branch(cpu, state.n, operand)

    elif mnemonic == "BNE":
        extra_cycles += _branch(cpu, not state.z, operand)

    elif mnemonic == "BPL":
        extra_cycles += _branch(cpu, not state.n, operand)

    elif mnemonic == "BVC":
        extra_cycles += _branch(cpu, not state.v, operand)

    elif mnemonic == "BVS":
        extra_cycles += _branch(cpu, state.v, operand)

    # --- Flags ---
    elif mnemonic == "CLC":
        state.c = False

    elif mnemonic == "CLD":
        state.d = False

    elif mnemonic == "CLI":
        state.i = False

    elif mnemonic == "CLV":
        state.v = False

    elif mnemonic == "SEC":
        state.c = True

    elif mnemonic == "SED":
        state.d = True

    elif mnemonic == "SEI":
        state.i = True

    # --- System ---
    elif mnemonic == "BRK":
        # BRK increments PC by 1 (the padding byte) then pushes PC and status
        state.pc = (state.pc + 1) & 0xFFFF
        cpu.push_word(state.pc)
        cpu.push(state.status | 0x30)  # B and bit 5 set
        state.i = True
        # Load IRQ/BRK vector
        state.pc = cpu.memory.read_word(0xFFFE)
        cpu.halted = True

    elif mnemonic == "NOP":
        pass

    else:
        raise ValueError(f"Unimplemented instruction: {mnemonic}")

    total = cycles + extra_cycles
    cpu.cycles += total
    return total


def _run(cpu: CPU6502, max_instructions: int = 10000) -> int:
    """Run instructions until BRK or max_instructions reached.

    Args:
        cpu: The CPU instance.
        max_instructions: Safety limit to prevent infinite loops.

    Returns:
        Total number of instructions executed.
    """
    count = 0
    while not cpu.halted and count < max_instructions:
        cpu.step()
        count += 1
    return count


# ---------------------------------------------------------------------------
# Attach methods to CPU6502
# ---------------------------------------------------------------------------

CPU6502.step = _step  # type: ignore[attr-defined]
CPU6502.run = _run    # type: ignore[attr-defined]
