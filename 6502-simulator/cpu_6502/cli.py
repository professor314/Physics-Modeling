"""Command-line interface for the 6502 simulator.

Usage:
    6502-sim run program.asm        — Assemble and run a program
    6502-sim debug program.asm      — Step through a program interactively
    6502-sim assemble program.asm   — Assemble and output binary file
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cpu_6502.assembler import Assembler, AssemblerError
from cpu_6502.cpu import CPU6502
from cpu_6502.debugger import Debugger
from cpu_6502.disassembler import disassemble
from cpu_6502.lcd import LCDDisplay
from cpu_6502.memory import Memory

# Import executor to attach step/run methods to CPU6502
import cpu_6502.executor  # noqa: F401


def _setup_cpu(program_bytes: bytes) -> tuple[CPU6502, LCDDisplay]:
    """Create a CPU with LCD mapped at $6000 and load a program."""
    memory = Memory()
    lcd = LCDDisplay()
    memory.register_io(0x6000, 0x6001, lcd)

    # Load program at its assembled origin
    memory.load_bytes(program_bytes, 0)

    cpu = CPU6502(memory)
    # Read reset vector to set PC
    cpu.state.pc = memory.read_word(0xFFFC)

    return cpu, lcd


def _cmd_run(args: argparse.Namespace) -> None:
    """Assemble and run a program."""
    source = Path(args.file).read_text(encoding='utf-8')
    asm = Assembler()

    try:
        program = asm.assemble(source)
    except AssemblerError as e:
        print(f"Assembly error: {e}", file=sys.stderr)
        sys.exit(1)

    # Load assembled bytes at the assembler's origin
    memory = Memory()
    lcd = LCDDisplay()
    memory.register_io(0x6000, 0x6001, lcd)
    memory.load_bytes(program, asm.origin)

    cpu = CPU6502(memory)
    cpu.state.pc = memory.read_word(0xFFFC)

    count = cpu.run()

    # Show results
    print(f"Executed {count} instructions ({cpu.cycles} cycles)")
    print(f"\nLCD Display:")
    print(lcd)


def _cmd_debug(args: argparse.Namespace) -> None:
    """Interactive debugger session."""
    source = Path(args.file).read_text(encoding='utf-8')
    asm = Assembler()

    try:
        program = asm.assemble(source)
    except AssemblerError as e:
        print(f"Assembly error: {e}", file=sys.stderr)
        sys.exit(1)

    memory = Memory()
    lcd = LCDDisplay()
    memory.register_io(0x6000, 0x6001, lcd)
    memory.load_bytes(program, asm.origin)

    cpu = CPU6502(memory)
    cpu.state.pc = memory.read_word(0xFFFC)

    dbg = Debugger(cpu)
    print("6502 Debugger — commands: s(tep), r(un), b(reak) $addr, m(em) $addr, q(uit), l(cd)")
    print(dbg.get_state())
    print()

    while True:
        try:
            cmd = input("dbg> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not cmd:
            continue

        parts = cmd.split()
        action = parts[0].lower()

        if action in ('q', 'quit', 'exit'):
            break
        elif action in ('s', 'step'):
            if cpu.halted:
                print("CPU halted.")
                continue
            disasm = dbg.step()
            print(f"  {disasm}")
            print(dbg.get_state())
        elif action in ('r', 'run'):
            if cpu.halted:
                print("CPU halted.")
                continue
            count = dbg.run_until_break()
            print(f"Ran {count} instructions")
            print(dbg.get_state())
        elif action in ('b', 'break'):
            if len(parts) < 2:
                print(f"Breakpoints: {', '.join(f'${a:04X}' for a in sorted(dbg.breakpoints))}")
            else:
                addr_str = parts[1].lstrip('$')
                try:
                    addr = int(addr_str, 16)
                    dbg.set_breakpoint(addr)
                    print(f"Breakpoint set at ${addr:04X}")
                except ValueError:
                    print(f"Invalid address: {parts[1]}")
        elif action in ('m', 'mem', 'memory'):
            addr = 0
            if len(parts) >= 2:
                try:
                    addr = int(parts[1].lstrip('$'), 16)
                except ValueError:
                    print(f"Invalid address: {parts[1]}")
                    continue
            print(dbg.get_memory_dump(addr))
        elif action in ('l', 'lcd'):
            print(lcd)
        elif action in ('d', 'disasm'):
            addr = cpu.state.pc
            if len(parts) >= 2:
                try:
                    addr = int(parts[1].lstrip('$'), 16)
                except ValueError:
                    print(f"Invalid address: {parts[1]}")
                    continue
            for line in disassemble(memory, addr, 8):
                print(f"  {line}")
        else:
            print("Unknown command. Use: s, r, b $addr, m $addr, l, d, q")


def _cmd_assemble(args: argparse.Namespace) -> None:
    """Assemble source to binary file."""
    source = Path(args.file).read_text(encoding='utf-8')
    asm = Assembler()

    try:
        program = asm.assemble(source)
    except AssemblerError as e:
        print(f"Assembly error: {e}", file=sys.stderr)
        sys.exit(1)

    # Determine output filename
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = Path(args.file).with_suffix('.bin')

    out_path.write_bytes(program)
    print(f"Assembled {len(program)} bytes -> {out_path}")
    print(f"Origin: ${asm.origin:04X}")


def main() -> None:
    """Entry point for the 6502-sim CLI."""
    parser = argparse.ArgumentParser(
        prog='6502-sim',
        description='MOS 6502 CPU Simulator — assembler, runner, and debugger'
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # run
    run_parser = subparsers.add_parser('run', help='Assemble and run a program')
    run_parser.add_argument('file', help='Assembly source file (.asm)')

    # debug
    debug_parser = subparsers.add_parser('debug', help='Interactive debugger')
    debug_parser.add_argument('file', help='Assembly source file (.asm)')

    # assemble
    asm_parser = subparsers.add_parser('assemble', help='Assemble to binary')
    asm_parser.add_argument('file', help='Assembly source file (.asm)')
    asm_parser.add_argument('-o', '--output', help='Output binary file path')

    args = parser.parse_args()

    if args.command == 'run':
        _cmd_run(args)
    elif args.command == 'debug':
        _cmd_debug(args)
    elif args.command == 'assemble':
        _cmd_assemble(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
