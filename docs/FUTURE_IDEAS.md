# Future Ideas & Extensions

Potential improvements and new features to build on top of the original Modeling Motion codebase. These represent planned extensions — none of these are part of the original 2004 coursework.

New code for these ideas goes in the `extensions/` directory.

---

## Numerical Methods

| Idea | Description | Extends |
|------|-------------|---------|
| RK4 Integration | Add 4th-order Runge-Kutta as an alternative to Euler's method | `original/assignments/springsim.py`, `universe.py` |
| Adaptive Step Size | Automatically adjust dt based on error estimates | All simulation programs |
| Verlet Integration | Symplectic integrator that conserves energy better for orbital mechanics | `references/glowscript-examples/BinaryStar-VPython.py` |
| Comparison Dashboard | Run the same simulation with different integrators and compare accuracy/performance | All |

## Performance & Modernization

| Idea | Description | Extends |
|------|-------------|---------|
| NumPy Vectorization | Replace manual loops with numpy array operations for N-body simulations | `original/assignments/universe.py`, `fountain.py` |
| SciPy ODE Solvers | Use `scipy.integrate.odeint` for differential equation models | `original/assignments/sir.py`, `logistic.py` |
| Parallel Collision Detection | Use spatial hashing or octrees for efficient N-body collision checking | `original/assignments/collision.py` |
| GPU Acceleration | Use CuPy or JAX for massive particle simulations | Gas/particle simulations |

## New Physics Models

| Idea | Description | Extends |
|------|-------------|---------|
| Double Pendulum | Lagrangian mechanics with chaos visualization | `original/assignments/springsim.py` |
| N-Body Gravitational | Simulate solar systems with arbitrary number of bodies | `references/glowscript-examples/BinaryStar-VPython.py` |
| Lorenz Attractor | Classic chaos theory demonstration | New |
| Wave Equation | 1D and 2D wave propagation with interference | New |
| Electromagnetic Fields | Visualize E and B fields from moving charges | `references/glowscript-examples/DipoleElectricField.py` |
| Quantum Mechanics | Schrödinger equation time evolution for 1D potentials | New |
| Fluid Dynamics | Simple SPH (Smoothed Particle Hydrodynamics) simulation | New |

## Visualization Improvements

| Idea | Description | Extends |
|------|-------------|---------|
| Matplotlib 2D Backend | Plot-based output for non-3D simulations (SIR, logistic, Riemann) | `original/assignments/sir.py`, `logistic.py`, `riemann.py` |
| Interactive Parameters | Sliders and controls to adjust simulation parameters in real-time | All visual programs |
| Jupyter Notebooks | Interactive notebooks for each simulation with explanations | All |
| Animation Export | Save simulations as MP4 or GIF for sharing | All visual programs |
| Dark Mode Theme | Modern visual styling for vpython scenes | All 3D programs |

## Rubik's Cube Enhancements

| Idea | Description | Extends |
|------|-------------|---------|
| Solving Algorithm | Implement a solving algorithm (Kociemba, CFOP, Thistlethwaite) | `original/rubiks-cube/best_cube.py` |
| Keyboard Controls | Rotate faces with keyboard shortcuts | `original/rubiks-cube/` |
| Scramble Generator | Random scramble generator with move notation | `original/rubiks-cube/` |
| State Validation | Verify a cube state is solvable | `original/rubiks-cube/cube_class.py` |
| Timer | Speedcubing timer with scramble display | New |

## Testing & Validation

| Idea | Description | Extends |
|------|-------------|---------|
| Unit Tests | Verify physics accuracy (conservation of energy/momentum) | All simulations |
| Property-Based Tests | Use Hypothesis to find edge cases in numerical code | Integration code |
| Benchmarks | Performance comparison across different implementations | All |
| Known Solutions | Compare against analytical solutions where available | `spring.py` (SHM), `sir.py` (exact logistic) |

## Documentation & Education

| Idea | Description | Extends |
|------|-------------|---------|
| Physics Explanations | Markdown docs explaining the math behind each simulation | All |
| Tutorial Series | Step-by-step guide to writing physics simulations | All |
| Video Demos | Screen recordings of simulations running | All visual programs |
| Comparison with Textbook | Show how code maps to physics textbook equations | `springsim.py`, `sir.py` |

---

## How to Contribute

1. Pick an idea from above
2. Create a GitHub Issue referencing this document
3. Implement in `extensions/` (never modify `original/`)
4. Submit a PR with tests and documentation
