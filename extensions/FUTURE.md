# Future Models & Features

Planned extensions to the physics-modeling package. Each item references which existing module it builds on.

## New Physics Models

| Model | Description | Difficulty | Builds On |
|-------|-------------|-----------|-----------|
| Lorenz Attractor | Classic 3-variable chaotic system | Easy | `core/` integrators |
| Damped Driven Oscillator | Forced oscillation with resonance | Easy | `oscillators/` |
| Wave Equation (1D) | String vibration with boundary conditions | Medium | `core/` integrators |
| Wave Equation (2D) | Membrane vibration, interference patterns | Medium | numpy vectorization |
| Predator-Prey (Lotka-Volterra) | Ecological population dynamics | Easy | `epidemics/` |
| Three-Body Problem | Chaotic gravitational interactions | Medium | `gravity/nbody.py` |
| Charged Particle in EM Field | Lorentz force, cyclotron motion | Medium | `core/` integrators |
| Schrödinger Equation (1D) | Quantum tunneling, wave packets | Hard | numpy + complex arrays |
| Fluid Dynamics (SPH) | Smoothed Particle Hydrodynamics | Hard | `gas/` collision framework |
| Ising Model | Statistical mechanics, phase transitions | Medium | Monte Carlo, no ODE |
| Projectile with Drag | Ballistic motion with air resistance | Easy | `gravity/bouncing.py` |
| Orbital Mechanics | Hohmann transfers, Kepler elements | Medium | `gravity/nbody.py` |

## Infrastructure Improvements

| Feature | Description |
|---------|-------------|
| Plotly Backend | Interactive 3D in Jupyter without matplotlib | 
| PyVista Backend | Hardware-accelerated 3D for standalone |
| Jupyter Widgets | ipywidgets sliders for all simulations |
| Adaptive Step Size | Auto-adjust dt based on local error |
| State Serialization | Save/load simulation snapshots (npz + JSON) |
| Performance Profiling | Benchmark each simulation, identify bottlenecks |
| NumPy Vectorization | Replace inner loops with vectorized operations |
| Multi-package Split | Separate core/simulations/viz into independent packages |

## Documentation

| Item | Description |
|------|-------------|
| Physics Docs | Derivation of equations for each simulation |
| API Reference | Auto-generated from docstrings (mkdocs/sphinx) |
| Tutorial Series | Step-by-step guides for beginners |
| Video Demos | Screen recordings of simulations |

## How to Contribute an Idea

1. Open a GitHub Issue with the "enhancement" label
2. Describe the physics/math involved
3. Reference which existing module it extends
4. Indicate difficulty level (easy/medium/hard)
