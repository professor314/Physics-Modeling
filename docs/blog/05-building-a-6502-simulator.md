# Building a 6502 Simulator in Python (Part 2)

*From a 12-instruction teaching CPU to a full MOS 6502 emulator — inspired by Ben Eater's breadboard projects.*

## Why the 6502?

The MOS 6502 is the processor that defined home computing in the late 1970s and early 1980s. It ran the Apple II, the Commodore 64, the Atari 2600, and the Nintendo Entertainment System. It powered the first affordable personal computers and launched an industry.

What makes it perfect for a simulator project:

1. **Simple enough to understand completely.** The 6502 has only 56 distinct instructions (with addressing mode variants giving 151 opcodes total). Compare that to a modern x86 with thousands of instructions — the 6502 is comprehensible by one person.

2. **Complex enough to be interesting.** It has 13 addressing modes, a stack, interrupt handling, decimal arithmetic (BCD), and memory-mapped I/O. It's a real architecture with real programs written for it.

3. **Ben Eater made it tangible.** Ben Eater's YouTube series shows a 6502 running on a breadboard — wired up with actual chips, an LCD display showing output, and LEDs blinking on the data bus. Watching physical signals flow through a real 6502 makes the architecture click in a way that documentation alone never does.

I want to build the software equivalent: a complete 6502 simulator with the same components Ben wires up on his breadboard — CPU, RAM, ROM, and an LCD display — but running in Python so I can program it, debug it, and extend it.

## The Architecture

### Registers

The 6502 has a minimal register set:

| Register | Bits | Purpose |
|----------|------|---------|
| A | 8 | Accumulator — the main math register |
| X | 8 | Index register — for array indexing |
| Y | 8 | Index register — secondary indexing |
| SP | 8 | Stack pointer — points into page $0100-$01FF |
| PC | 16 | Program counter — address of next instruction |
| P | 8 | Status register — holds the CPU flags |

The status register (P) packs 7 flags into one byte:

```
Bit:  7  6  5  4  3  2  1  0
Flag: N  V  -  B  D  I  Z  C
```

- **N** (Negative): set when result has bit 7 = 1
- **V** (Overflow): set on signed arithmetic overflow
- **B** (Break): distinguishes BRK from IRQ
- **D** (Decimal): enables BCD arithmetic mode
- **I** (Interrupt Disable): masks IRQ
- **Z** (Zero): set when result = 0
- **C** (Carry): carry/borrow from arithmetic

### Memory Map

The 6502 addresses 64KB ($0000-$FFFF):

```
$0000-$00FF  Zero Page (fast access, shorter instructions)
$0100-$01FF  Stack (grows downward from $01FF)
$0200-$5FFF  RAM (general purpose)
$6000-$600F  I/O (LCD display, keyboard, etc.)
$8000-$FFFF  ROM (program code, loaded at startup)
$FFFA-$FFFB  NMI vector
$FFFC-$FFFD  Reset vector (where execution starts)
$FFFE-$FFFF  IRQ/BRK vector
```

The reset vector at $FFFC is key: when the CPU starts (or resets), it reads the 16-bit address at $FFFC-$FFFD and begins executing from there. This is how the boot process works — the ROM programmer stores their entry point address at $FFFC.

### Addressing Modes

This is where the 6502 gets interesting. The same instruction (like LDA — load accumulator) has different opcodes depending on how you specify the operand:

| Mode | Syntax | Example | Meaning |
|------|--------|---------|---------|
| Immediate | `#$nn` | `LDA #$42` | Load the literal value $42 |
| Zero Page | `$nn` | `LDA $10` | Load from address $0010 |
| Zero Page,X | `$nn,X` | `LDA $10,X` | Load from $0010 + X |
| Absolute | `$nnnn` | `LDA $4000` | Load from address $4000 |
| Absolute,X | `$nnnn,X` | `LDA $4000,X` | Load from $4000 + X |
| Absolute,Y | `$nnnn,Y` | `LDA $4000,Y` | Load from $4000 + Y |
| Indirect | `($nnnn)` | `JMP ($FFFC)` | Jump to address stored at $FFFC |
| (Indirect,X) | `($nn,X)` | `LDA ($20,X)` | Pointer from zero page + X |
| (Indirect),Y | `($nn),Y` | `LDA ($20),Y` | Pointer from zero page, then + Y |

The indirect modes are what make the 6502 capable of complex data structures — arrays, linked lists, function pointers — despite having only three registers.

## The Plan

The simulator is being built as a standalone Python project at `professor314/6502-simulator`. The components mirror what Ben Eater wires on his breadboard:

### CPU Core
- `CPUState` dataclass with all registers and flags
- Fetch-decode-execute cycle
- All 151 opcodes implemented correctly

### Memory System
- 64KB address space
- ROM regions (writes ignored)
- Memory-mapped I/O with handler callbacks

### LCD Display
- 16×2 character display (like the HD44780 Ben uses)
- Mapped to a memory address range
- Renders as text in the terminal or matplotlib panel

### Assembler
- Two-pass assembler translating 6502 assembly → machine code
- Labels, all addressing mode syntaxes
- Directives: `.byte`, `.word`, `.org`

### Debugger
- Step-through execution
- Register inspection
- Memory hex dump
- Breakpoints
- Disassembly view

## From MM1 to 6502

The conceptual jump from my college MM1 to the real 6502:

| Feature | MM1 | 6502 |
|---------|-----|------|
| Registers | 8 general-purpose | 3 specific (A, X, Y) + SP, PC |
| Memory | 64 words | 65,536 bytes |
| Instructions | 12 | 56 (151 with modes) |
| Instruction size | Fixed 12-bit | Variable 1-3 bytes |
| Addressing modes | 1 | 13 |
| Stack | None | Hardware stack at $0100-$01FF |
| Interrupts | None | NMI, IRQ, BRK |
| I/O | None | Memory-mapped |
| BCD arithmetic | No | Yes (decimal mode) |

The core concept is identical though: fetch an instruction from memory, decode its fields, execute the operation, repeat. The MM1 taught me the pattern. The 6502 fills in the details of a real-world implementation.

## What's Coming

The 6502 simulator will be built in phases:

1. **CPU core** — registers, memory, opcode table, instruction decoder
2. **Instruction execution** — load/store, arithmetic, branches, stack operations
3. **Assembler** — translate assembly source to machine code
4. **Peripherals** — LCD display, memory-mapped I/O
5. **Debugger** — step-through, breakpoints, memory view
6. **Visualization** — terminal or matplotlib UI showing everything at once

The goal is to write a program in 6502 assembly, assemble it, load it into the simulator, and watch it execute instruction by instruction — with the virtual LCD showing "HELLO WORLD" just like Ben Eater's breadboard computer does.

The code will live at: https://github.com/professor314/6502-simulator

Follow along as I build it from the ground up.
