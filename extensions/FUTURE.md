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

### Dual-Mode Visualization (Standalone + Jupyter)

The existing `visualization/` module has infrastructure for this (Renderer protocol, environment detection) but it's not wired into the viz files yet.

**Goal:** Every simulation works in BOTH modes:
- **Standalone**: `physics-modeling spring-pendulum` opens a matplotlib window (current behavior)
- **Jupyter**: `from physics_modeling.oscillators import SpringPendulum; sim.show()` renders inline with Plotly/ipywidgets

**Detailed tasks:**

1. **Wire viz files through the Renderer protocol**
   - Each `_viz.py` file currently uses matplotlib directly
   - Refactor to accept a `renderer` parameter, defaulting to `MatplotlibRenderer`
   - When in a notebook, auto-select `PlotlyRenderer` instead

2. **Implement PlotlyRenderer** (`visualization/plotly_backend.py`)
   - Implement the `Renderer` protocol using Plotly for 2D and 3D
   - Support `add_slider()` via Plotly FigureWidget or ipywidgets
   - Renders inline in Jupyter cells

3. **Implement environment auto-switching**
   - `detect_environment()` already exists in `visualization/environment.py`
   - Add `get_default_renderer()` that returns Plotly in notebooks, Matplotlib in standalone
   - Each viz file calls this if no explicit renderer is passed

4. **Add `.show()` convenience method to Simulation classes**
   - `sim.show()` picks the right renderer and launches the visualization
   - Works in both standalone (opens window) and notebook (renders inline)
   - No need to import viz files separately

5. **ipywidgets integration for notebooks** (`visualization/widgets.py`)
   - Wrapper providing sliders/buttons via ipywidgets
   - Maps to the same `add_slider()` interface used by matplotlib widgets
   - Enables real-time parameter changes inside Jupyter cells

**Dependencies:** `plotly`, `ipywidgets` (already in `[project.optional-dependencies].notebook`)

**Current state:** `visualization/renderer.py` (protocol), `environment.py` (detection), and `matplotlib_backend.py` (2D/3D renderers with slider support) are already built. This work wires them into the existing viz files and adds the Plotly alternative.

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
