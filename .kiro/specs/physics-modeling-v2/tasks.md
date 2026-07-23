# Implementation Plan: physics-modeling-v2

## Overview

This plan implements the `physics-modeling` package in five phases. Phase 1 is fully detailed and executable now — it delivers a pip-installable package with core engine, three simulations (spring pendulum, gravity/bouncing, SIR), base matplotlib visualization, property-based tests, and CI/CD. Phases 2–5 are documented at a higher level and will be detailed when reached.

All code lives under `extensions/physics_modeling/`. The existing `extensions/spring_pendulum_3d.py` demo will be refactored into the proper package structure.

Platform: Windows, PowerShell, `py` command. Python 3.10+ (user has 3.14).

---

## Tasks

### Phase 1: Core Engine, Package Scaffolding, and Initial Simulations

- [x] 1. Set up package scaffolding and build configuration
  - [x] 1.1 Create package directory structure and pyproject.toml
    - Create `extensions/physics_modeling/` directory tree with `__init__.py` files for: `core/`, `oscillators/`, `gravity/`, `epidemics/`, `visualization/`, `cli/`
    - Create `extensions/pyproject.toml` with project metadata, Python 3.10+ requirement, dependencies (numpy, matplotlib), optional dependency groups (dev: pytest, hypothesis, hypothesis-numpy, mypy, ruff, pytest-cov)
    - Add `py.typed` marker file
    - Add `extensions/README.md` with installation instructions and quick-start
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 1.2 Create CI/CD pipeline configuration
    - Create `.github/workflows/ci.yml` with matrix testing (Python 3.10, 3.11, 3.12)
    - Steps: checkout, setup-python with pip cache, `pip install -e ".[dev]"`, ruff check, mypy --strict, pytest with --cov and --cov-fail-under=80
    - Set triggers on push to any branch and pull requests to main
    - Working directory set to `extensions/` for all steps
    - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5, 20.6_

  - [x] 1.3 Create ruff and mypy configuration
    - Add `[tool.ruff]` section to pyproject.toml with PEP 8, import sorting (isort), unused imports
    - Add `[tool.mypy]` section with strict mode enabled
    - Add `extensions/tests/conftest.py` with shared Hypothesis strategies and pytest configuration
    - _Requirements: 21.1, 21.2, 21.3, 21.4, 21.5_

- [x] 2. Implement core numerical engine
  - [x] 2.1 Implement integrator protocol and all three integrators
    - Create `physics_modeling/core/protocols.py` with `Integrator` Protocol (step method signature)
    - Create `physics_modeling/core/integrators.py` with `EulerIntegrator`, `RK4Integrator`, `VerletIntegrator`
    - Euler: `state + derivatives(state, t) * dt`
    - RK4: four-slope weighted combination with standard (1/6, 1/3, 1/3, 1/6) weights
    - Verlet: position-velocity symplectic update with half-step acceleration
    - Add type annotations and NumPy-style docstrings on all public functions
    - _Requirements: 2.1, 2.2, 2.3, 2.6_

  - [ ]* 2.2 Write property test: Integrator Dimensionality (Property 1)
    - **Property 1: Integrator Dimensionality and Formula Correctness**
    - Test that for any state vector dimension (1-20) and any derivative function, all integrators produce output of same shape as input
    - Test that Euler output equals `state + derivatives(state, t) * dt` exactly
    - Use Hypothesis with `hypothesis.extra.numpy.arrays` for random state vectors
    - **Validates: Requirements 2.1, 2.6**

  - [x] 2.3 Implement base Simulation class and SimulationRunner
    - Create `physics_modeling/core/simulation.py` with abstract `Simulation` base class
    - Implement `SimulationConfig` dataclass with `dt` and `integrator` fields
    - Implement `initial_state()`, `derivatives()` abstract methods
    - Implement `step(dt)` and `run(t_end, dt)` methods
    - Add NaN/Inf divergence detection raising `SimulationDivergenceError`
    - Create `physics_modeling/core/runner.py` with `SimulationRunner` class
    - Create `physics_modeling/core/__init__.py` re-exporting all public names
    - _Requirements: 2.5, 2.7_

  - [ ]* 2.4 Write property test: Simulation Run Output Shape (Property 21)
    - **Property 21: Simulation Run Output Shape**
    - Test that `run(t_end, dt)` returns array of shape `(int(t_end/dt) + 1, D)` where D is state dimension
    - Test that first row equals initial state
    - Create a minimal concrete Simulation subclass for testing (e.g., simple decay `dx/dt = -x`)
    - **Validates: Requirements 2.7**

  - [ ]* 2.5 Write property test: Energy Conservation (Property 2 — SHO case)
    - **Property 2: Energy Conservation in Conservative Systems**
    - Test simple harmonic oscillator (`x'' = -x`) with Verlet and RK4: energy preserved within 0.1% over 10,000 steps with dt=0.01
    - Use Hypothesis for random amplitudes (0.1 to 10.0) as initial conditions
    - **Validates: Requirements 2.4**

  - [ ]* 2.6 Write property test: Integrator Accuracy (Property 3 — SHO case)
    - **Property 3: Integrator Accuracy Against Analytical Solutions**
    - Test all integrators against analytical `A*cos(t)` for SHO with dt=0.01, t in [0, 10]
    - Verify position values within 1% of analytical solution
    - **Validates: Requirements 2.8**

- [x] 3. Checkpoint — Core engine tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Implement Spring Pendulum simulation
  - [x] 4.1 Implement SpringPendulum physics module
    - Create `physics_modeling/oscillators/spring_pendulum.py` with `SpringPendulum` class extending `Simulation`
    - Create `SpringPendulumConfig` dataclass (k, damping, mass, rest_length, g, air_resistance, initial_angle, initial_velocity)
    - Implement `derivatives()` computing: spring force, damping force, air resistance, gravity → net acceleration
    - State vector: `[x, y, z, vx, vy, vz]` (6D)
    - Refactor physics logic from existing `extensions/spring_pendulum_3d.py`
    - Support all three integrators
    - Add input validation (negative mass, zero rest_length → ValueError)
    - _Requirements: 3.1, 3.2, 3.4, 3.7_

  - [ ]* 4.2 Write property test: Spring Pendulum Energy Conservation (Property 2 — spring case)
    - **Property 2: Energy Conservation in Conservative Systems (spring pendulum)**
    - When damping=0 and air_resistance=0, total mechanical energy (KE + GPE + elastic PE) conserved within 0.5% over 1000 steps using RK4
    - Use Hypothesis for random initial angles and k values
    - **Validates: Requirements 3.3**

- [x] 5. Implement Gravity and Bouncing simulation
  - [x] 5.1 Implement Gravity/Bouncing physics module
    - Create `physics_modeling/gravity/__init__.py` and `physics_modeling/gravity/bouncing.py`
    - Create `GravityConfig` dataclass (g, restitution, boundary_y, extent)
    - Implement single-object gravity with floor bounce (velocity reversal * restitution)
    - Implement multi-object support with stacked state arrays
    - Implement boundary removal for objects exiting extent
    - Add input validation (restitution outside [0,1] → ValueError)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [ ]* 5.2 Write property tests: Gravity Bounce (Properties 15 and 16)
    - **Property 15: Gravity Bounce Energy Preservation**
    - When restitution=1.0, kinetic energy before bounce equals KE after bounce within 1%
    - **Property 16: Boundary Object Removal**
    - Objects exceeding extent are removed from active list
    - **Validates: Requirements 4.3, 4.5**

- [x] 6. Implement SIR Epidemic Model
  - [x] 6.1 Implement SIR physics module
    - Create `physics_modeling/epidemics/__init__.py` and `physics_modeling/epidemics/sir.py`
    - Create `SIRConfig` dataclass (S0, I0, R0, beta, gamma, dt, integrator)
    - Implement `derivatives()`: `[-β*S*I/N, β*S*I/N - γ*I, γ*I]`
    - State vector: `[S, I, R]` (3D)
    - Support both Euler and RK4 integrators
    - Add validation for non-negative populations
    - _Requirements: 8.1, 8.2, 8.4_

  - [ ]* 6.2 Write property test: SIR Population Conservation (Property 5)
    - **Property 5: Epidemiological Population Conservation**
    - S + I + R = N preserved within 1e-10 at every time step
    - Use Hypothesis for random (S0, I0, R0) and (beta, gamma) parameters
    - **Validates: Requirements 8.3**

  - [ ]* 6.3 Write property test: SIR Monotone Decrease (Property 6)
    - **Property 6: SIR Monotone Decrease When R₀ < 1**
    - When β/γ < 1, infected population I(t) is monotonically non-increasing
    - Generate random parameters satisfying β*N/γ < 1 constraint
    - **Validates: Requirements 8.5**

- [x] 7. Checkpoint — All Phase 1 simulations pass tests
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement base visualization backend
  - [x] 8.1 Implement Renderer protocol and matplotlib backend
    - Create `physics_modeling/visualization/__init__.py`, `renderer.py`, `environment.py`, `matplotlib_backend.py`
    - Implement `Renderer` Protocol with `setup()`, `draw()`, `add_slider()`, `close()` methods
    - Implement `detect_environment()` → "notebook" | "standalone" | "headless"
    - Implement `MatplotlibRenderer` for 2D time-series plots and 3D animated views
    - Support `FuncAnimation`-based animation loop for standalone mode
    - _Requirements: 16.1, 16.2, 16.5, 16.6_

  - [x] 8.2 Implement Spring Pendulum 3D visualization
    - Create visualization adapter connecting `SpringPendulum` simulation to `MatplotlibRenderer`
    - Port helix-generation code from `extensions/spring_pendulum_3d.py` into the renderer
    - Implement interactive sliders (k, damping, mass, gravity) using matplotlib widgets
    - Display animated 3D pendulum with spring coil, bob, and fading trail
    - _Requirements: 3.5, 3.6, 16.7_

  - [x] 8.3 Implement Gravity and SIR visualizations
    - Gravity: 3D scatter plot of bouncing spheres with configurable colors
    - SIR: 2D time-series plot with S, I, R curves, legend, axis labels, and parameter sliders for β and γ
    - _Requirements: 4.6, 8.6, 8.7_

- [x] 9. Implement CLI entry points
  - [x] 9.1 Create CLI module with simulation launchers
    - Create `physics_modeling/cli/__init__.py` and `physics_modeling/cli/main.py`
    - Add `[project.scripts]` entry point in pyproject.toml: `physics-modeling = "physics_modeling.cli.main:main"`
    - Implement subcommands: `spring-pendulum`, `gravity`, `sir`
    - Each subcommand creates the simulation + renderer and calls `start()`
    - Handle headless gracefully (compute-only mode)
    - _Requirements: 17.1, 17.2, 17.4, 17.5_

- [x] 10. Final integration and package validation
  - [x] 10.1 Wire all components together and validate package installation
    - Ensure `pip install -e .` works from `extensions/` directory
    - Verify `from physics_modeling.core import Simulation, RK4Integrator` imports work
    - Verify `from physics_modeling.oscillators import SpringPendulum` imports work
    - Verify CLI command `physics-modeling spring-pendulum` launches correctly
    - Run full test suite: `py -m pytest tests/ -v --cov=physics_modeling --cov-fail-under=80`
    - Run ruff and mypy checks
    - _Requirements: 1.1, 1.2, 23.1, 23.2_

- [x] 11. Final checkpoint — Phase 1 complete
  - Ensure all tests pass, ruff + mypy pass, package installs cleanly. Ask the user if questions arise.

---

### Phase 2: Remaining Physics Simulations (Future)

- [x] 12. Implement remaining physics modules
  - [x] 12.1 Implement Logistic Equation and Riemann Sums (calculus/)
    - Logistic equation with analytical solution comparison
    - Riemann sums with left/right/midpoint/trapezoid methods and rectangle visualization
    - Property tests for Properties 3 (logistic case) and 8 (monotone convergence)
    - _Requirements: 10.1–10.5, 12.1–12.6_

  - [x] 12.2 Implement Lissajous Figures (oscillators/lissajous.py)
    - Parametric curve generation with 3D gradient coloring
    - Property tests for Properties 7 (closure) and 18 (formula correctness)
    - _Requirements: 11.1–11.5_

  - [x] 12.3 Implement Elastic Collisions (collisions/elastic.py)
    - 2D and 3D collision detection and elastic resolution
    - Property test for Property 4 (momentum + energy conservation)
    - _Requirements: 6.1–6.6_

  - [x] 12.4 Implement Hard Sphere Gas (gas/hard_sphere.py)
    - N-particle hard sphere simulation with event-driven collisions
    - Thermodynamic measurements (temperature, pressure)
    - Property test for Property 17 (kinetic energy conservation)
    - _Requirements: 7.1–7.5_

  - [x] 12.5 Implement Double Pendulum, N-Body, and SEIR
    - Double pendulum with Lagrangian equations and chaos demonstration
    - N-body gravitational with Verlet integration and softening
    - SEIR extension of SIR with exposed compartment
    - Property tests for Properties 2 (double pendulum, N-body), 5 (SEIR), 20 (softening)
    - _Requirements: 5.1–5.5, 9.1–9.4, 13.1–13.4_

---

### Phase 3: Rubik's Cube Application (SEPARATE REPO: professor314/rubiks-cube)

> This is a standalone project, NOT part of the physics-modeling package.
> Will be created as a new GitHub repo. Has its own pyproject.toml, README, and CLI.

- [x] 13.1 Implement cube state representation and move system
  - CubeState with (6,3,3) facelet array, Move enum, apply/inverse, validation
  - _DONE — code exists at extensions/physics_modeling/rubiks_cube/ and will be moved_

- [x] 13.2 Create scrambler.py
- [x] 13.3 Create timer.py
- [x] 13.4 Create solver.py
- [x] 13.5 Create rubiks-cube project scaffolding
- [x] 13.6 Create cube_viz.py — 3D rendering function
- [x] 13.7 Create cube_viz.py — keyboard controls and main loop
- [x] 13.8 Initialize git repo and push to GitHub

---

### Phase 4: 6502 CPU Simulator (SEPARATE REPO: professor314/6502-simulator)

> This is a standalone project, NOT part of the physics-modeling package.
> Will be created as a new GitHub repo. Has its own pyproject.toml, README, and CLI.

- [ ] 14.1 Create 6502-simulator project scaffolding
  - Create new directory structure for standalone repo:
    - `cpu_6502/` package
    - `pyproject.toml` (name: 6502-simulator, deps: numpy, matplotlib)
    - `README.md` (project description, 6502 overview, usage examples)
    - `.gitignore`
    - `tests/` directory
  - Move existing cpu_6502/ code from extensions/physics_modeling/ (if any)
  - Remove cpu_6502/ from extensions/physics_modeling/
  - Remove 6502 from physics-modeling CLI

- [ ] 14.2 Create cpu_6502/cpu.py — CPUState dataclass
  - Registers: A, X, Y, SP, PC + status flags (N, V, B, D, I, Z, C)
  - `status` property (pack/unpack flags to byte)
  - ~60 lines.
  - _Requirements: 15.2_

- [ ] 14.2 Create cpu_6502/memory.py — Memory class
  - 64KB bytearray, read(addr), write(addr, val)
  - ROM regions (write ignored), memory-mapped I/O handler registration
  - load_rom(data, start_address)
  - ~80 lines.
  - _Requirements: 15.3, 15.4_

- [ ] 14.3 Create cpu_6502/opcodes.py — opcode table
  - [ ] 14.3a Define AddressingMode enum (IMMEDIATE, ZERO_PAGE, ZERO_PAGE_X, ZERO_PAGE_Y, ABSOLUTE, ABSOLUTE_X, ABSOLUTE_Y, INDIRECT, INDEXED_INDIRECT, INDIRECT_INDEXED, IMPLIED, ACCUMULATOR, RELATIVE)
  - [ ] 14.3b Define Instruction dataclass: opcode(int), mnemonic(str), mode(AddressingMode), cycles(int), operand_bytes(int)
  - [ ] 14.3c Create OPCODE_TABLE dict for load/store/transfer opcodes (LDA, LDX, LDY, STA, STX, STY, TAX, TAY, TXA, TYA, TSX, TXS) — ~30 entries
  - [ ] 14.3d Add arithmetic/logic opcodes (ADC, SBC, AND, ORA, EOR, CMP, CPX, CPY, INC, DEC, INX, INY, DEX, DEY) — ~50 entries
  - [ ] 14.3e Add shift/rotate opcodes (ASL, LSR, ROL, ROR) — ~20 entries
  - [ ] 14.3f Add branch/jump/stack opcodes (BCC, BCS, BEQ, BNE, BMI, BPL, BVC, BVS, JMP, JSR, RTS, RTI, BRK, NOP, PHA, PLA, PHP, PLP, SEC, CLC, SEI, CLI, SED, CLD, CLV) — ~50 entries
  - [ ] 14.3g Add decode(memory, pc) function that reads opcode byte + operand bytes and returns Instruction
  - Total: ~200 lines of data + ~30 lines of decode logic. Reference: http://www.6502.org/tutorials/6502opcodes.html
  - _Requirements: 15.1_

- [ ] 14.4 Create cpu_6502/executor.py — instruction execution (load/store/transfer)
  - LDA, LDX, LDY, STA, STX, STY, TAX, TAY, TXA, TYA, TSX, TXS
  - Flag updates for N and Z
  - ~80 lines.
  - _Requirements: 15.1_

- [ ] 14.5 Create cpu_6502/executor.py — arithmetic and logic
  - [ ] 14.5a Implement ADC (add with carry) — binary mode: A = A + operand + C, set N/Z/C/V flags
  - [ ] 14.5b Implement ADC BCD mode — when D flag set: decimal addition, carry on >99
  - [ ] 14.5c Implement SBC (subtract) — binary mode: A = A - operand - !C, set N/Z/C/V flags
  - [ ] 14.5d Implement SBC BCD mode — decimal subtraction with borrow
  - [ ] 14.5e Implement AND, ORA, EOR — bitwise ops on A, set N/Z
  - [ ] 14.5f Implement CMP, CPX, CPY — compare by subtracting, set N/Z/C but don't store result
  - [ ] 14.5g Implement INC, DEC (memory), INX, INY, DEX, DEY (register) — set N/Z
  - [ ] 14.5h Implement ASL, LSR, ROL, ROR — shift/rotate A or memory, set N/Z/C
  - BCD reference: https://www.nesdev.org/wiki/Decimal_mode
  - ~150 lines total.
  - _Requirements: 15.1, 15.11_

- [ ] 14.6 Create cpu_6502/executor.py — branches, jumps, stack
  - BCC, BCS, BEQ, BNE, BMI, BPL, BVC, BVS (relative addressing)
  - JMP, JSR, RTS, RTI, BRK
  - PHA, PLA, PHP, PLP
  - Stack pointer wrap-around ($0100-$01FF page)
  - ~120 lines.
  - _Requirements: 15.5, 15.6_

- [ ] 14.7 Create cpu_6502/cpu.py — CPU6502 class (main execution loop)
  - fetch(), decode(), execute() cycle
  - step() → execute one instruction, return cycles
  - run(n_instructions) and run_until(address)
  - Wire together memory + opcodes + executor
  - ~100 lines.
  - _Requirements: 15.1, 15.2_

- [ ] 14.8 Create cpu_6502/assembler.py — two-pass assembler
  - [ ] 14.8a Define addressing mode syntax patterns and regex matchers:
    - `#$nn` → IMMEDIATE, `$nn` → ZERO_PAGE, `$nn,X` → ZERO_PAGE_X, `$nn,Y` → ZERO_PAGE_Y
    - `$nnnn` → ABSOLUTE, `$nnnn,X` → ABSOLUTE_X, `$nnnn,Y` → ABSOLUTE_Y
    - `($nnnn)` → INDIRECT, `($nn,X)` → INDEXED_INDIRECT, `($nn),Y` → INDIRECT_INDEXED
    - `A` → ACCUMULATOR, (no operand) → IMPLIED, `label` → RELATIVE/ABSOLUTE
  - [ ] 14.8b Implement Pass 1: scan for labels (lines with `label:` prefix), record PC address in symbol table
  - [ ] 14.8c Implement Pass 2: parse mnemonic + operand, detect addressing mode, look up opcode, emit bytes
  - [ ] 14.8d Handle directives: `.byte $xx`, `.word $xxxx`, `.org $xxxx`
  - [ ] 14.8e Raise AssemblyError with line number on any failure
  - ~200 lines total.
  - _Requirements: 15.7_

- [ ] 14.9 Create cpu_6502/disassembler.py
  - Convert bytes back to assembly text with addresses
  - ~80 lines.
  - _Requirements: 15.7_

- [ ] 14.10 Create cpu_6502/lcd.py — memory-mapped LCD display
  - LCDDisplay class: 16x2 character grid mapped to address range
  - write(address, value) updates cursor/display buffer
  - get_display() → list of row strings
  - ~60 lines.
  - _Requirements: 15.4_

- [ ] 14.11 Create cpu_6502/debugger.py — step-through debugger
  - Debugger class: step(), get_registers(), get_disassembly(), get_memory_view()
  - set_breakpoint(address), run_until_break()
  - ~80 lines.
  - _Requirements: 15.9_

- [ ] 14.12 Create cpu_6502/viz.py — standalone TUI/matplotlib panel
  - Show registers, current instruction, memory hex dump, LCD display
  - Keyboard: 's'=step, 'r'=run, 'b'=breakpoint, 'q'=quit
  - ~150 lines.
  - _Requirements: 15.10_

- [ ] 14.13 Update cpu_6502/__init__.py and add CLI entry point
  - Export all public classes
  - Add `6502` subcommand to cli/main.py
  - ~20 lines.

- [ ] 14.15 Initialize git repo and push to GitHub
  - `git init` in the 6502-simulator directory
  - Create repo on GitHub: professor314/6502-simulator
  - Push initial commit

- [ ] 14.16 Verify — load and run a simple 6502 program
  - Write a test program that counts from 0 to 10 and writes to LCD
  - Assemble, load into memory, run, verify LCD output
  - Confirms full pipeline works end-to-end.

---

### Phase 5: Jupyter Trainer Notebooks and Documentation

- [ ] 15.0 Clean up physics-modeling repo
  - Remove `extensions/physics_modeling/rubiks_cube/` (moved to separate repo)
  - Remove `extensions/physics_modeling/cpu_6502/` (moved to separate repo)
  - Remove rubiks-cube and 6502 entries from cli/main.py
  - Remove rubiks-cube and 6502 references from pyproject.toml optional deps
  - Commit and push to Physics-Modeling repo

- [ ] 15.1 Create notebooks/spring_pendulum_trainer.ipynb
  - Physics explanation (SHM, Hooke's law, Euler's method)
  - Build simulation step by step
  - Interactive widgets for k, damping
  - Exercise: add air resistance
  - _Requirements: 18.1–18.5_

- [ ] 15.2 Create notebooks/sir_model_trainer.ipynb
  - SIR math derivation, R₀ explanation
  - Build SIR simulation incrementally
  - Widget sliders for β, γ
  - Exercise: implement SEIR extension
  - _Requirements: 18.1–18.5_

- [ ] 15.3 Create notebooks/nbody_trainer.ipynb
  - Gravitational force derivation, Verlet integrator explanation
  - Build binary star system step by step
  - Exercise: add a third body
  - _Requirements: 18.1–18.5_

- [ ] 15.4 Create notebooks/riemann_sums_trainer.ipynb
  - Integration fundamentals, Riemann sum types
  - Visualize convergence as n increases
  - Exercise: implement trapezoidal rule
  - _Requirements: 18.1–18.5_

- [ ] 15.5 Create notebooks/lissajous_trainer.ipynb
  - Parametric curves, frequency ratios, closure conditions
  - Interactive frequency/phase widgets
  - Exercise: predict closed vs open curves
  - _Requirements: 18.1–18.5_

- [ ] 15.6 Create docs/README.md (extensions)
  - Full installation guide, API overview, module listing
  - _Requirements: 22.1_

- [ ] 15.7 Create docs/physics/ explanation documents
  - One markdown doc per simulation module explaining the math
  - _Requirements: 22.2_

- [ ] 15.8 Create CONTRIBUTING.md
  - Dev setup, coding standards, PR guidelines, test instructions
  - _Requirements: 22.4_

- [ ] 15.9 Create FUTURE.md
  - Planned models: Lorenz attractor, wave equation, quantum, fluid, EM fields
  - Organized by difficulty and dependency
  - _Requirements: 23.7_

---

### Phase 5b: README Audit and Blog Posts

- [ ] 16.1 Audit and update Physics-Modeling top-level README.md
  - Ensure it accurately reflects current state (12 simulations, no rubiks/6502)
  - Update project structure section
  - Add link to extensions/FUTURE.md
  - Make sure install + run instructions are correct for Python 3.14

- [ ] 16.2 Audit and update extensions/README.md
  - Full API overview table (all modules, classes, key functions)
  - Installation instructions (pip install -e .)
  - Quick-start code examples for each simulation
  - Link to CONTRIBUTING.md and FUTURE.md

- [ ] 16.3 Audit rubiks-cube/README.md
  - Verify controls section is accurate
  - Add screenshot placeholder or ASCII art
  - Verify install instructions work

- [ ] 16.4 Create blog post: "Modernizing a 2004 Physics Codebase"
  - `docs/blog/01-modernizing-legacy-code.md`
  - Story: found old college code, organized it, made it run on Python 3.14
  - Topics: VPython → matplotlib migration, compatibility shim approach, preserving original code
  - ~1000 words

- [ ] 16.5 Create blog post: "Building a Physics Simulation Engine in Python"
  - `docs/blog/02-physics-simulation-engine.md`
  - Technical: Euler vs RK4 vs Verlet, base Simulation class pattern, separation of physics from viz
  - Code examples showing how to create a new simulation
  - ~1500 words

- [ ] 16.6 Create blog post: "Interactive Rubik's Cube with Matplotlib"
  - `docs/blog/03-rubiks-cube-matplotlib.md`
  - How to render 3D objects with Poly3DCollection, facelet coordinate math, keyboard events
  - The tricky parts: move cycle definitions, validation logic
  - ~1000 words

- [ ] 16.7 Push all changes to GitHub repos

---

## Notes

- Tasks marked with `*` are optional property-based test tasks and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Phase 1 is fully executable now; Phases 2–5 will be detailed when reached
- Platform: Windows + PowerShell. Use `py -m pytest` not `python -m pytest`
- The existing `extensions/spring_pendulum_3d.py` serves as reference for refactoring into the package
- matplotlib is the confirmed 3D backend (vpython doesn't work on Python 3.14)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 12, "tasks": ["13.2", "13.3", "13.4"] },
    { "id": 13, "tasks": ["13.5"] },
    { "id": 14, "tasks": ["13.6"] },
    { "id": 15, "tasks": ["13.7"] },
    { "id": 16, "tasks": ["13.8"] },
    { "id": 17, "tasks": ["14.1", "14.2", "14.3"] },
    { "id": 18, "tasks": ["14.4", "14.5", "14.6"] },
    { "id": 19, "tasks": ["14.7"] },
    { "id": 20, "tasks": ["14.8", "14.9", "14.10", "14.11"] },
    { "id": 21, "tasks": ["14.12", "14.13"] },
    { "id": 22, "tasks": ["14.14"] },
    { "id": 23, "tasks": ["15.1", "15.2", "15.3", "15.4", "15.5"] },
    { "id": 24, "tasks": ["15.6", "15.7", "15.8", "15.9"] }
  ]
}
```
