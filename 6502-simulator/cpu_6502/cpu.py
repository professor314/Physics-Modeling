"""6502 CPU state and core CPU shell.

Provides the CPUState dataclass (registers + status flags) and the CPU6502
class that wires together memory, the opcode decoder, and the execution loop.
"""

from __future__ import annotations

from dataclasses import dataclass

from cpu_6502.memory import Memory


@dataclass
class CPUState:
    """Complete MOS 6502 register file.

    All registers are unsigned integers clamped to their documented widths.
    Status flags are stored as individual booleans for clarity; pack/unpack
    via the `status` property.

    Bit layout of the P (status) register:
        7  6  5  4  3  2  1  0
        N  V  1  B  D  I  Z  C
    Bit 5 is always read as 1 (unused, hardwired high).
    """

    a: int = 0        # Accumulator (8-bit, 0–255)
    x: int = 0        # Index register X (8-bit)
    y: int = 0        # Index register Y (8-bit)
    sp: int = 0xFD    # Stack pointer (8-bit, stack lives at $0100–$01FF)
    pc: int = 0       # Program counter (16-bit, 0–65535)

    # Status flags
    n: bool = False   # Negative (bit 7)
    v: bool = False   # Overflow (bit 6)
    b: bool = False   # Break command (bit 4)
    d: bool = False   # Decimal mode (bit 3)
    i: bool = True    # Interrupt disable (bit 2)
    z: bool = True    # Zero (bit 1)
    c: bool = False   # Carry (bit 0)

    @property
    def status(self) -> int:
        """Pack flags into the P register byte. Bit 5 is always 1."""
        return (
            (int(self.n) << 7)
            | (int(self.v) << 6)
            | (1 << 5)  # Bit 5 always set
            | (int(self.b) << 4)
            | (int(self.d) << 3)
            | (int(self.i) << 2)
            | (int(self.z) << 1)
            | int(self.c)
        )

    @status.setter
    def status(self, value: int) -> None:
        """Unpack a P register byte into individual flags.

        Bit 5 is ignored on write (it's always read as 1).
        """
        self.n = bool(value & 0x80)
        self.v = bool(value & 0x40)
        self.b = bool(value & 0x10)
        self.d = bool(value & 0x08)
        self.i = bool(value & 0x04)
        self.z = bool(value & 0x02)
        self.c = bool(value & 0x01)

    # --- Helper methods for flag updates ---

    def update_nz(self, value: int) -> None:
        """Update Negative and Zero flags based on an 8-bit result."""
        value &= 0xFF
        self.n = bool(value & 0x80)
        self.z = (value == 0)


class CPU6502:
    """MOS 6502 CPU emulator shell.

    Connects the register state, memory bus, and stack operations.
    Instruction execution is handled by a separate executor module
    that operates on this class.

    Attributes:
        state: The CPU register file.
        memory: The 64KB memory system.
        cycles: Total elapsed clock cycles.
        halted: Whether the CPU has been stopped (BRK or explicit halt).
    """

    def __init__(self, memory: Memory | None = None) -> None:
        self.state: CPUState = CPUState()
        self.memory: Memory = memory if memory is not None else Memory()
        self.cycles: int = 0
        self.halted: bool = False

    # ------------------------------------------------------------------
    # Stack operations
    # ------------------------------------------------------------------

    def push(self, value: int) -> None:
        """Push a byte onto the stack.

        The 6502 stack lives at page $01 ($0100–$01FF). The stack pointer
        points to the next free location and decrements after a push.
        SP wraps: pushing when SP=$00 wraps to $FF.

        Args:
            value: Byte to push (0–255).
        """
        self.memory.write(0x0100 + self.state.sp, value & 0xFF)
        self.state.sp = (self.state.sp - 1) & 0xFF

    def pull(self) -> int:
        """Pull (pop) a byte from the stack.

        Increments SP first, then reads. SP wraps: pulling when SP=$FF
        wraps to $00.

        Returns:
            Byte value (0–255).
        """
        self.state.sp = (self.state.sp + 1) & 0xFF
        return self.memory.read(0x0100 + self.state.sp)

    def push_word(self, value: int) -> None:
        """Push a 16-bit value onto the stack (high byte first, then low).

        This matches the 6502 convention: JSR pushes PC high then PC low,
        so pulling gives low first then high.

        Args:
            value: 16-bit value (0–65535).
        """
        self.push((value >> 8) & 0xFF)  # High byte
        self.push(value & 0xFF)          # Low byte

    def pull_word(self) -> int:
        """Pull a 16-bit value from the stack (low byte first, then high).

        Returns:
            16-bit value (0–65535).
        """
        lo = self.pull()
        hi = self.pull()
        return (hi << 8) | lo

    # ------------------------------------------------------------------
    # Reset and interrupt vectors
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Perform a hardware reset.

        Reads the reset vector at $FFFC–$FFFD and sets PC.
        Sets SP to $FD, clears registers, sets I flag.
        """
        self.state = CPUState()  # Fresh state (SP=$FD, I=True, Z=True)
        self.state.pc = self.memory.read_word(0xFFFC)
        self.cycles = 0
        self.halted = False

    def load_rom(self, data: bytes, start: int) -> None:
        """Convenience: load ROM into memory and reset.

        Args:
            data: Raw program bytes.
            start: Starting address for the ROM.
        """
        self.memory.load_rom(data, start)

    # ------------------------------------------------------------------
    # Fetch helpers
    # ------------------------------------------------------------------

    def fetch_byte(self) -> int:
        """Fetch the byte at PC and advance PC by 1.

        Returns:
            Byte value (0–255).
        """
        value = self.memory.read(self.state.pc)
        self.state.pc = (self.state.pc + 1) & 0xFFFF
        return value

    def fetch_word(self) -> int:
        """Fetch a 16-bit little-endian word at PC and advance PC by 2.

        Returns:
            16-bit value (0–65535).
        """
        lo = self.fetch_byte()
        hi = self.fetch_byte()
        return (hi << 8) | lo
