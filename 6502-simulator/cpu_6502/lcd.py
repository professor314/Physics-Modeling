"""Memory-mapped 16x2 character LCD display (HD44780 style).

This module emulates a simple character LCD mapped to a range of memory
addresses. Writing a byte to the data register places a character at the
current cursor position and advances the cursor. A simple control register
allows clearing the display and resetting the cursor.

Memory map (relative to base address):
    Offset 0: Data register — write ASCII char at cursor position
    Offset 1: Control register — write 0x01 to clear, 0x02 to home cursor
"""

from __future__ import annotations


class LCDDisplay:
    """16x2 character LCD emulator.

    Implements the IOHandler protocol for memory-mapped I/O. Characters
    written to offset 0 are placed at the cursor position and the cursor
    advances. When the cursor reaches the end of a row it wraps to the next
    row, and from the end of row 2 back to the start of row 1.

    Attributes:
        COLS: Number of columns (16).
        ROWS: Number of rows (2).
        buffer: 2D list of characters representing the display.
        cursor_row: Current cursor row (0 or 1).
        cursor_col: Current cursor column (0–15).
    """

    COLS = 16
    ROWS = 2

    def __init__(self) -> None:
        self.buffer: list[list[str]] = [[' '] * self.COLS for _ in range(self.ROWS)]
        self.cursor_row: int = 0
        self.cursor_col: int = 0

    def write(self, address: int, value: int) -> None:
        """Write to the LCD.

        Address offset 0 = data register: write printable ASCII char at cursor.
        Address offset 1 = control register:
            0x01 = clear display
            0x02 = return cursor home (0,0)

        Args:
            address: The memory address (only low bits used for offset).
            value: Byte value to write.
        """
        # Use low bit of address to distinguish data vs control
        offset = address & 0x01

        if offset == 0:
            # Data register — write character at cursor
            ch = chr(value) if 32 <= value < 127 else ' '
            self.buffer[self.cursor_row][self.cursor_col] = ch
            self._advance_cursor()
        else:
            # Control register
            if value == 0x01:
                self.clear()
            elif value == 0x02:
                self.cursor_row = 0
                self.cursor_col = 0

    def read(self, address: int) -> int:
        """Read from the LCD (returns current char at cursor or 0).

        Args:
            address: The memory address.

        Returns:
            ASCII value of character at cursor, or 0 for control register.
        """
        offset = address & 0x01
        if offset == 0:
            return ord(self.buffer[self.cursor_row][self.cursor_col])
        return 0

    def _advance_cursor(self) -> None:
        """Move cursor forward one position, wrapping at end of display."""
        self.cursor_col += 1
        if self.cursor_col >= self.COLS:
            self.cursor_col = 0
            self.cursor_row += 1
            if self.cursor_row >= self.ROWS:
                self.cursor_row = 0

    def get_display(self) -> list[str]:
        """Return the display contents as a list of strings.

        Returns:
            2-element list where each element is a 16-character string
            representing one row of the display.
        """
        return [''.join(row) for row in self.buffer]

    def clear(self) -> None:
        """Clear the display and reset cursor to home position."""
        self.buffer = [[' '] * self.COLS for _ in range(self.ROWS)]
        self.cursor_row = 0
        self.cursor_col = 0

    def __str__(self) -> str:
        """Pretty-print the LCD display with a border."""
        lines = self.get_display()
        border = '+' + '-' * self.COLS + '+'
        return f"{border}\n|{lines[0]}|\n|{lines[1]}|\n{border}"
