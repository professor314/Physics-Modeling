"""MOS 6502 CPU Simulator.

A complete emulator of the 6502 processor with assembler, debugger,
and memory-mapped I/O peripherals.
"""

__version__ = "0.1.0"

from cpu_6502.cpu import CPU6502, CPUState
from cpu_6502.memory import Memory
from cpu_6502.assembler import Assembler
from cpu_6502.lcd import LCDDisplay
from cpu_6502.debugger import Debugger

# Import executor to attach step()/run() methods to CPU6502
import cpu_6502.executor  # noqa: F401

__all__ = [
    "CPU6502",
    "CPUState",
    "Memory",
    "Assembler",
    "LCDDisplay",
    "Debugger",
]
