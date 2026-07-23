# physics-modeling

A modern Python physics simulation library built as the professional rewrite of original coursework from The Evergreen State College (2004). Features numerical integrators (Euler, RK4, Verlet), oscillators, gravity, collisions, gas dynamics, epidemics, and more — all with interactive matplotlib visualizations and a CLI runner.

## Installation

```bash
cd extensions
pip install -e .
```

### Optional extras

```bash
pip install -e ".[dev]"       # pytest, hypothesis, mypy, ruff
pip install -e ".[notebook]"  # Jupyter + ipywidgets
pip install -e ".[3d]"        # PyVista 3D rendering
```

## Quick Start

```python
from physics_modeling.core import Simulation, SimulationConfig, RK4Integrator
from physics_modeling.oscillators.spring_pendulum import SpringPendulum, SpringPendulumConfig
import numpy as np

# Configure and run a spring pendulum simulation
config = SpringPendulumConfig(k=10.0, damping=0.05, mass=1.0, dt=0.01, integrator="rk4")
sim = SpringPendulum(config)

# Run for 10 seconds, get full state history
history = sim.run(t_end=10.0)
print(f"Simulated {len(history)} steps, final position: {history[-1, :3]}")
```

## Simulations

| CLI Command | Module | Description |
|---|---|---|
| `spring-pendulum` | `oscillators.spring_pendulum` | 3D spring pendulum with interactive sliders |
| `double-pendulum` | `oscillators.double_pendulum` | 2D double pendulum with chaotic motion and trail |
| `lissajous` | `oscillators.lissajous` | 3D Lissajous figure visualization |
| `gravity` | `gravity.bouncing` | 3D bouncing objects under gravity (fountain mode) |
| `nbody` | `gravity.nbody` | 3D N-body gravitational simulation (binary star + particles) |
| `collisions` | `collisions.elastic` | Elastic collision simulation |
| `gas` | `gas.hard_sphere` | Ideal gas hard-sphere simulation |
| `sir` | `epidemics.sir` | SIR epidemic model with parameter sliders |
| `seir` | `epidemics.seir` | SEIR epidemic model with parameter sliders |
| `logistic` | `calculus.logistic` | Logistic growth equation visualization |
| `riemann` | `calculus.riemann` | Riemann sum visualization with interactive controls |
| `bouncing` | `gravity.bouncing` | Alias for `gravity` |

## CLI Usage

After installation, launch any simulation from the command line:

```bash
physics-modeling list              # Show all available simulations
physics-modeling spring-pendulum   # Launch spring pendulum
physics-modeling nbody             # Launch N-body simulation
physics-modeling sir               # Launch SIR epidemic model
```

## Project Structure

```
extensions/
├── physics_modeling/
│   ├── core/              # Simulation base class, integrators, runner
│   ├── oscillators/       # Spring pendulum, double pendulum, Lissajous
│   ├── gravity/           # Bouncing, N-body
│   ├── collisions/        # Elastic collisions
│   ├── gas/               # Hard-sphere ideal gas
│   ├── epidemics/         # SIR, SEIR models
│   ├── calculus/          # Riemann sums, logistic equation
│   ├── visualization/     # Shared plotting utilities
│   └── cli/               # Command-line interface
├── tests/                 # Property-based and unit tests
├── notebooks/             # Jupyter training notebooks
├── docs/                  # Physics documentation per simulation
├── CONTRIBUTING.md        # How to add new simulations
├── FUTURE.md              # Roadmap and planned features
└── pyproject.toml         # Package configuration
```

## Notebooks

Interactive Jupyter notebooks for exploring simulations with parameter sliders:

- `notebooks/spring_pendulum_trainer.ipynb`
- `notebooks/nbody_trainer.ipynb`
- `notebooks/sir_model_trainer.ipynb`
- `notebooks/riemann_sums_trainer.ipynb`
- `notebooks/lissajous_trainer.ipynb`

## Development

```bash
pip install -e ".[dev]"

pytest tests/ -v          # Run tests
mypy physics_modeling/    # Type checking
ruff check physics_modeling/  # Linting
```

## Requirements

- Python >= 3.10
- numpy >= 1.24
- matplotlib >= 3.7

## Links

- [Contributing Guide](CONTRIBUTING.md)
- [Future Roadmap](FUTURE.md)
- [Notebooks](notebooks/)
