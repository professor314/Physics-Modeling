# physics-modeling

A modern Python physics simulation library featuring numerical integrators (Euler, RK4, Verlet), oscillators, gravity, collisions, gas dynamics, epidemics, and more. Built as the professional rewrite of the original Modeling Motion coursework.

## Installation

### Basic install (from this directory)

```bash
pip install -e .
```

### With development tools (testing, linting, type checking)

```bash
pip install -e ".[dev]"
```

### With Jupyter notebook support

```bash
pip install -e ".[notebook]"
```

### With 3D visualization (PyVista)

```bash
pip install -e ".[3d]"
```

### With Rubik's cube solver

```bash
pip install -e ".[rubiks]"
```

## Quick Start

```python
from physics_modeling.core import Simulation, RK4Integrator
from physics_modeling.oscillators import SpringPendulum
```

## CLI Usage

After installation, run simulations from the command line:

```bash
physics-modeling spring-pendulum
physics-modeling gravity
physics-modeling sir
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Type checking
mypy physics_modeling/

# Linting
ruff check physics_modeling/
```

## Requirements

- Python >= 3.10
- numpy >= 1.24
- matplotlib >= 3.7
