"""Interactive debugger for the 6502 CPU simulator.

Provides step-by-step execution, breakpoints, register inspection,
and memory dump capabilities.
"""

from __future__ import annotations

from cpu_6502.cpu import CPU6502
from cpu_6502.disassembler import disassemble_one


class Debugger:
    """6502 CPU debugger with breakpoints and state inspection.

    Attributes:
        cpu: The CPU instance being debugged.
        breakpoints: Set of addresses where execution will pause.
        instruction_count: Number of instructions executed in this session.
    """

    def __init__(self, cpu: CPU6502) -> None:
        self.cpu = cpu
        self.breakpoints: set[int] = set()
        self.instruction_count: int = 0

    def step(self) -> str:
        """Execute one instruction and return its disassembly.

        Returns:
            Formatted disassembly string of the instruction that was executed.
        """
        pc_before = self.cpu.state.pc
        disasm, _ = disassemble_one(self.cpu.memory, pc_before)
        self.cpu.step()
        self.instruction_count += 1
        return disasm

    def run_until_break(self) -> int:
        """Run until BRK instruction or a breakpoint is hit.

        Returns:
            Number of instructions executed during this run.
        """
        count = 0
        max_instructions = 100000  # Safety limit

        while not self.cpu.halted and count < max_instructions:
            if count > 0 and self.cpu.state.pc in self.breakpoints:
                break
            self.cpu.step()
            count += 1
            self.instruction_count += 1

        return count

    def set_breakpoint(self, address: int) -> None:
        """Add a breakpoint at the given address.

        Args:
            address: Memory address where execution should pause.
        """
        self.breakpoints.add(address & 0xFFFF)

    def clear_breakpoint(self, address: int) -> None:
        """Remove a breakpoint at the given address.

        Args:
            address: Memory address to remove the breakpoint from.
        """
        self.breakpoints.discard(address & 0xFFFF)

    def get_state(self) -> str:
        """Format the current CPU state for display.

        Returns:
            Multi-line string showing all registers and flags.
        """
        s = self.cpu.state
        flags = (
            f"{'N' if s.n else 'n'}"
            f"{'V' if s.v else 'v'}"
            f"-"
            f"{'B' if s.b else 'b'}"
            f"{'D' if s.d else 'd'}"
            f"{'I' if s.i else 'i'}"
            f"{'Z' if s.z else 'z'}"
            f"{'C' if s.c else 'c'}"
        )
        return (
            f"PC: ${s.pc:04X}  SP: ${s.sp:02X}  Cycles: {self.cpu.cycles}\n"
            f" A: ${s.a:02X}    X: ${s.x:02X}    Y: ${s.y:02X}\n"
            f" P: ${s.status:02X} [{flags}]"
        )

    def get_memory_dump(self, start: int, length: int = 64) -> str:
        """Format a memory dump as hex + ASCII.

        Args:
            start: Starting address.
            length: Number of bytes to display.

        Returns:
            Formatted memory dump string with hex and ASCII columns.
        """
        lines: list[str] = []
        for offset in range(0, length, 16):
            addr = (start + offset) & 0xFFFF
            hex_parts: list[str] = []
            ascii_parts: list[str] = []

            for i in range(16):
                if offset + i < length:
                    byte = self.cpu.memory.read((addr + i) & 0xFFFF)
                    hex_parts.append(f"{byte:02X}")
                    ascii_parts.append(chr(byte) if 32 <= byte < 127 else '.')
                else:
                    hex_parts.append("  ")
                    ascii_parts.append(' ')

            hex_str = ' '.join(hex_parts)
            ascii_str = ''.join(ascii_parts)
            lines.append(f"${addr:04X}: {hex_str}  |{ascii_str}|")

        return '\n'.join(lines)
