"""64KB memory system with ROM regions and memory-mapped I/O.

The 6502 addresses a flat 64KB space ($0000–$FFFF). This module provides:
- Read/write with 8-bit values
- Read 16-bit little-endian words
- ROM regions that silently ignore writes
- Memory-mapped I/O via handler objects
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class IOHandler(Protocol):
    """Protocol for memory-mapped I/O peripherals.

    Peripherals register at one or more addresses and intercept reads/writes.
    """

    def read(self, address: int) -> int:
        """Read a byte from the peripheral at the given address."""
        ...

    def write(self, address: int, value: int) -> None:
        """Write a byte to the peripheral at the given address."""
        ...


class Memory:
    """64KB addressable memory with ROM protection and I/O mapping.

    Attributes:
        _ram: The raw 64KB byte array.
        _rom_regions: List of (start, end) address pairs marked read-only.
        _io_handlers: Mapping from address to I/O handler objects.
    """

    def __init__(self) -> None:
        self._ram: bytearray = bytearray(65536)
        self._rom_regions: list[tuple[int, int]] = []  # (start, end) inclusive
        self._io_handlers: dict[int, IOHandler] = {}

    def read(self, address: int) -> int:
        """Read a single byte from the given 16-bit address.

        If an I/O handler is registered at this address, delegates to it.
        Otherwise reads directly from RAM/ROM.

        Args:
            address: Memory address (0x0000–0xFFFF).

        Returns:
            Byte value (0–255).
        """
        address &= 0xFFFF
        if address in self._io_handlers:
            return self._io_handlers[address].read(address) & 0xFF
        return self._ram[address]

    def write(self, address: int, value: int) -> None:
        """Write a single byte to the given 16-bit address.

        - Writes to ROM regions are silently ignored.
        - Writes to I/O-mapped addresses are forwarded to the handler.

        Args:
            address: Memory address (0x0000–0xFFFF).
            value: Byte value (0–255).
        """
        address &= 0xFFFF
        value &= 0xFF

        # Check I/O handlers first (I/O can overlap ROM in some designs)
        if address in self._io_handlers:
            self._io_handlers[address].write(address, value)
            return

        # Ignore writes to ROM
        for start, end in self._rom_regions:
            if start <= address <= end:
                return

        self._ram[address] = value

    def read_word(self, address: int) -> int:
        """Read a 16-bit little-endian word from the given address.

        Reads low byte at `address` and high byte at `address + 1`.
        Wraps within the 16-bit address space.

        Args:
            address: Starting address for the low byte.

        Returns:
            16-bit value (0–65535).
        """
        lo = self.read(address & 0xFFFF)
        hi = self.read((address + 1) & 0xFFFF)
        return (hi << 8) | lo

    def read_word_bug(self, address: int) -> int:
        """Read 16-bit word with the 6502 page-boundary bug.

        The 6502's indirect JMP has a hardware bug: if the low byte of the
        pointer is $FF, the high byte is fetched from $xx00 instead of
        $(xx+1)00. This replicates that behavior.

        Args:
            address: Starting address for the low byte.

        Returns:
            16-bit value (0–65535).
        """
        lo = self.read(address)
        # Wrap within page (high byte stays the same)
        hi_addr = (address & 0xFF00) | ((address + 1) & 0x00FF)
        hi = self.read(hi_addr)
        return (hi << 8) | lo

    def load_rom(self, data: bytes, start: int) -> None:
        """Load data into memory and mark the region as ROM.

        Args:
            data: Raw bytes to load.
            start: Starting address (0x0000–0xFFFF).
        """
        end = start + len(data) - 1
        self._ram[start : start + len(data)] = data
        self._rom_regions.append((start, end))

    def load_bytes(self, data: bytes, start: int) -> None:
        """Load data into memory without marking it as ROM.

        Useful for loading programs into writable RAM.

        Args:
            data: Raw bytes to load.
            start: Starting address (0x0000–0xFFFF).
        """
        self._ram[start : start + len(data)] = data

    def register_io(self, start: int, end: int, handler: IOHandler) -> None:
        """Register an I/O handler for an address range.

        Every address in [start, end] (inclusive) will dispatch reads/writes
        to the given handler.

        Args:
            start: First mapped address.
            end: Last mapped address (inclusive).
            handler: Object implementing IOHandler protocol.
        """
        for addr in range(start, end + 1):
            self._io_handlers[addr] = handler

    def reset(self) -> None:
        """Zero all RAM. ROM contents and I/O mappings are preserved."""
        # Preserve ROM contents
        rom_data: list[tuple[int, int, bytes]] = []
        for start, end in self._rom_regions:
            rom_data.append((start, end, bytes(self._ram[start : end + 1])))

        self._ram = bytearray(65536)

        # Restore ROM
        for start, _end, data in rom_data:
            self._ram[start : start + len(data)] = data
