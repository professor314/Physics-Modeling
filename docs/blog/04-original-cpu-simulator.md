# Building a CPU Simulator in College (Part 1)

*The original MM1 processor simulator — a custom instruction set architecture built in Python as a student.*

## The Assignment

In 2004, week 5 of the Modeling Motion program introduced something unexpected: we weren't simulating springs or epidemics anymore. We were building a computer from scratch — in software.

The assignment was to implement a simple processor simulator. Not a real CPU architecture like x86 or ARM, but a custom one designed for teaching: the **MM1** (Modeling Motion 1). It had 8 registers, 64 words of memory, a 12-bit instruction format, and just enough instructions to write meaningful programs.

## The Architecture

The MM1 is about as simple as a processor can be while still being useful:

**Registers:** 8 general-purpose registers (`r0` through `r7`), each holding an integer value.

**Memory:** 64 words. Instructions live in the low addresses, data in the high addresses. There's no separation between code and data — you could overwrite your own instructions if you weren't careful.

**Instruction Format:** 12 bits packed into fields:

```
bits:   [12-9]  [8-6]  [5-3]  [2-0]
fields: opcode   src1   src2   dest
```

Four bits for the opcode gives us 16 possible instructions. Three bits for each operand gives register indices 0-7 or memory addresses 0-63 (with some encoding tricks).

**Instructions:**

| Opcode | Mnemonic | Operation |
|--------|----------|-----------|
| 0 | ADD | dest = src1 + src2 |
| 1 | SUB | dest = src1 - src2 |
| 2 | MUL | dest = src1 × src2 |
| 3 | DIV | dest = src1 / src2 |
| 4 | INC | dest = dest + 1 |
| 5 | LD  | Load memory → register |
| 6 | ST  | Store register → memory |
| 7 | MOV | Copy one register to another |
| 8 | JMP | Unconditional jump |
| 9 | JZ  | Jump if ALU output is zero |
| 10 | JN | Jump if ALU output is negative |
| 15 | HALT | Stop execution |

## The Components

I built the simulator as Python classes that mirror real hardware components:

### ALU (Arithmetic Logic Unit)

The ALU takes two inputs (A and B), performs an operation (ADD, SUB, MUL, DIV), and produces an output plus two flags:
- **Zero flag**: set when the output equals zero
- **Sign flag**: set when the output is negative

These flags are what make conditional jumps possible — the processor can branch based on whether the last computation was zero or negative.

### Register File

Eight registers, indexed 0-7. Simple read/write interface. The register file is the processor's short-term memory — fast to access, limited in quantity.

### Memory

64 words addressed 0-63. Separate `read()` and `write()` methods with an `address` bus and `data` bus — modeling how real memory works with distinct address and data lines.

### Sequencer

The brain of the processor. Implements the **fetch-decode-execute** cycle:

1. **Fetch**: Read the instruction at the program counter from memory
2. **Decode**: Extract opcode, source, and destination fields from the 12-bit instruction word
3. **Execute**: Dispatch to the appropriate handler (doload, doadd, dojump, etc.)

After each instruction, the program counter advances to the next address — unless a jump instruction redirects it elsewhere.

## A Real Program: Falling Object

Here's the assembly language program I wrote that simulates a falling object under gravity:

```
01 LD 32 r0    # initial velocity = 0
02 LD 33 r1    # acceleration due to gravity = -1
03 LD 34 r2    # time step = 1 sec
04 LD 35 r3    # height = 30
05 LD 36 r4    # constant = 0

06 ADD r0 r1 r0   # velocity += acceleration
07 SUB r3 r0 r3   # height -= velocity
08 JN 10          # if height < 0, jump to reset
09 JMP 06         # otherwise loop

10 LD r3 r4       # reset height to 0
11 MUL r0 r1 r0   # reverse velocity (bounce)
12 JMP 06         # continue

32 DATA 0    # initial velocity
33 DATA -1   # gravity
34 DATA 1    # dt
35 DATA 30   # starting height
36 DATA 0    # zero constant
```

This is essentially the same Euler's method integration we used for the physics simulations — but running on a simulated processor instead of Python directly. The ball falls (velocity increases each step), and when height goes negative (the JN instruction checks the sign flag), it "bounces" by reversing the velocity.

## The Two-Pass Assembler

The assembler translates these text instructions into 12-bit machine code words:

**Pass 1**: Parse each line, extract the opcode and operands
**Pass 2**: Pack them into the bit fields according to the instruction format

For example, `ADD r0 r1 r0` becomes:
- opcode = 0 (ADD)  → bits 12-9 = 0000
- src1 = 0 (r0)     → bits 8-6 = 000
- src2 = 1 (r1)     → bits 5-3 = 001
- dest = 0 (r0)     → bits 2-0 = 000
- Machine word: `0b0000_000_001_000` = 8

The assembled words get loaded into memory, and the processor executes them one at a time, fetching from address 1, then 2, then 3 — unless a jump redirects the program counter.

## What I Learned

Building a CPU simulator taught me more about how computers actually work than any other assignment in the program:

- **Instructions are just numbers.** There's nothing magical about machine code — it's integers with specific bit fields that the hardware knows how to interpret.
- **The fetch-decode-execute cycle is the heartbeat.** Every processor in every computer does this billions of times per second. Understanding it at the Python level made it tangible.
- **Flags and conditional jumps are how decisions happen.** There's no `if` statement in hardware — there's an ALU that sets flags, and a sequencer that reads them.
- **Programs and data share the same memory.** This is the Von Neumann architecture. Your code is data. Your data could be code. This insight opens up self-modifying programs, interpreters, and compilers.

## To Be Continued...

The MM1 was a teaching tool — 12 instructions, 8 registers, 64 words of memory. Real processors are vastly more complex. In Part 2, I'll be building a simulator for the **MOS 6502** — the processor that powered the Apple II, Commodore 64, and NES. Same concepts (fetch-decode-execute, registers, flags, memory) but scaled up to a real-world architecture with 151 opcodes, 13 addressing modes, and hardware peripherals.

The motivation comes from Ben Eater's breadboard computer projects, where he builds a working 6502 computer from discrete components and programs it in assembly. I want to do the same thing in software — a complete 6502 that can run real programs, with a virtual LCD display, ROM, and a step-through debugger.
