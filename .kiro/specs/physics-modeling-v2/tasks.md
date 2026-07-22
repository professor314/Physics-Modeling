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

### Phase 3: Rubik's Cube Application (Future)

- [ ] 13. Implement Rubik's Cube full application
  - [x] 13.1 Implement cube state representation and move system
    - `CubeState` with (6,3,3) facelet array, `Move` enum, `apply_move()`, `apply_sequence()`
    - Validation (solvability check), `inverse_move()`, `inverse_sequence()`
    - _Requirements: 14.1, 14.2, 14.3, 14.4_

  - [ ] 13.2 Implement solver, scrambler, and timer
    - Kociemba solver integration, scramble generator (20-25 moves, no same-face consecutive)
    - Timer measuring from first move to solved-state detection
    - Property tests for Properties 9 (round-trip), 10 (state validity), 11 (scramble constraints)
    - _Requirements: 14.5, 14.9, 14.10, 14.11_

  - [ ] 13.3 Implement 3D cube visualization with keyboard/mouse controls
    - 3D rendering with distinct face colors and rotation animations
    - Keyboard input for moves, mouse drag for camera
    - _Requirements: 14.6, 14.7, 14.8_

---

### Phase 4: 6502 CPU Simulator (Future)

- [ ] 14. Implement 6502 CPU simulator
  - [ ] 14.1 Implement CPU core: registers, memory, instruction decoder
    - `CPUState` dataclass, `Memory` class (64KB, ROM regions, memory-mapped I/O)
    - Table-driven opcode decoder with all addressing modes
    - _Requirements: 15.1, 15.2, 15.3, 15.4_

  - [ ] 14.2 Implement full instruction set and BCD arithmetic
    - All documented 6502 opcodes with correct flag behavior
    - Decimal mode (BCD) for ADC/SBC, stack wrap-around
    - Property tests for Properties 12 (round-trip), 13 (ROM protection), 14 (BCD), 19 (stack wrap)
    - _Requirements: 15.5, 15.6, 15.8, 15.11_

  - [ ] 14.3 Implement assembler, disassembler, and debugger
    - Two-pass assembler (label resolution), disassembler, step-through debugger
    - Memory-mapped LCD display (16x2)
    - Standalone visualization with register/memory panels
    - _Requirements: 15.7, 15.9, 15.10_

---

### Phase 5: Jupyter Trainer Notebooks and Documentation (Future)

- [ ] 15. Create Jupyter trainer notebooks and documentation
  - [ ] 15.1 Create trainer notebooks
    - Spring pendulum, SIR model, N-body, Riemann sums, Lissajous
    - Each with physics explanations, incremental code cells, interactive widgets, exercises
    - _Requirements: 18.1–18.5_

  - [ ] 15.2 Create comprehensive documentation
    - Physics explanation documents for each module (equations of motion, numerical methods)
    - API docs from docstrings (mkdocs or sphinx)
    - CONTRIBUTING.md with development setup and PR guidelines
    - _Requirements: 22.1–22.4_

  - [ ] 15.3 Create FUTURE.md and Plotly/PyVista backends
    - FUTURE.md listing planned models (Lorenz, wave equation, quantum, fluid, EM fields)
    - Plotly interactive backend for notebooks
    - PyVista 3D backend for standalone
    - _Requirements: 16.3, 16.4, 23.7_

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
    { "id": 0, "tasks": ["1.1"] },
    { "id": 1, "tasks": ["1.2", "1.3"] },
    { "id": 2, "tasks": ["2.1"] },
    { "id": 3, "tasks": ["2.2", "2.3"] },
    { "id": 4, "tasks": ["2.4", "2.5", "2.6"] },
    { "id": 5, "tasks": ["4.1", "5.1", "6.1"] },
    { "id": 6, "tasks": ["4.2", "5.2", "6.2", "6.3"] },
    { "id": 7, "tasks": ["8.1"] },
    { "id": 8, "tasks": ["8.2", "8.3"] },
    { "id": 9, "tasks": ["9.1"] },
    { "id": 10, "tasks": ["10.1"] },
    { "id": 11, "tasks": ["12.1", "12.2", "12.3", "12.4", "12.5"] },
    { "id": 12, "tasks": ["13.1"] },
    { "id": 13, "tasks": ["13.2", "13.3"] },
    { "id": 14, "tasks": ["14.1"] },
    { "id": 15, "tasks": ["14.2", "14.3"] },
    { "id": 16, "tasks": ["15.1", "15.2", "15.3"] }
  ]
}
```
