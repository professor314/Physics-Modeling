# 6502 CPU Simulator

A complete MOS 6502 CPU simulator in Python — assembler, step-through debugger, and virtual LCD display. Inspired by [Ben Eater's breadboard computer](https://eater.net/6502) project.

## Features

- Full 6502 instruction set (all 151 documented opcodes)
- 13 addressing modes
- 64KB memory with configurable ROM regions
- Memory-mapped I/O (virtual 16×2 LCD display)
- Two-pass assembler with label support
- Disassembler
- Step-through debugger with breakpoints
- BCD (decimal mode) arithmetic
- Interrupt handling (BRK, IRQ vectors)

## Install

```bash
pip install -e .
```

## Quick Start

```python
from cpu_6502 import CPU6502, Assembler

# Assemble a program
asm = Assembler()
program = asm.assemble("""
    .org $8000
start:
    LDA #$48        ; 'H'
    STA $6000       ; write to LCD
    LDA #$65        ; 'e'
    STA $6000
    LDA #$6C        ; 'l'
    STA $6000
    STA $6000
    LDA #$6F        ; 'o'
    STA $6000
    BRK

    .org $FFFC
    .word $8000     ; reset vector
""")

# Load and run
cpu = CPU6502()
cpu.load_rom(program, 0x8000)
cpu.reset()
cpu.run()

print(cpu.lcd.get_display())  # ['Hello           ', '                ']
```

## CLI

```bash
6502-sim run programs/hello.asm        # Assemble and run
6502-sim debug programs/hello.asm      # Step-through debugger
6502-sim assemble programs/hello.asm   # Assemble to binary
```

## Architecture

```
cpu_6502/
├── __init__.py       # Package exports
├── cpu.py            # CPU6502 class (registers, fetch-decode-execute)
├── memory.py         # 64KB memory with ROM and I/O mapping
├── opcodes.py        # Opcode table and instruction decoder
├── executor.py       # Instruction execution logic
├── assembler.py      # Two-pass assembler
├── disassembler.py   # Machine code → assembly text
├── lcd.py            # Memory-mapped 16×2 LCD display
├── debugger.py       # Step-through debugger
└── cli.py            # Command-line interface
```

## 6502 Reference

- [6502.org Tutorials](http://www.6502.org/tutorials/)
- [Opcodes Reference](http://www.6502.org/tutorials/6502opcodes.html)
- [Ben Eater's 6502 Series](https://www.youtube.com/playlist?list=PLowKtXNTBypFbtuVMUVXNR0z1mu7dp7eH)
- [NESdev Wiki — Decimal Mode](https://www.nesdev.org/wiki/Decimal_mode)

## Blog Posts

- [Part 1: The Original MM1 Simulator](../docs/blog/04-original-cpu-simulator.md)
- [Part 2: Building the 6502](../docs/blog/05-building-a-6502-simulator.md)
