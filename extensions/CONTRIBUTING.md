# Contributing to Physics Modeling

Thanks for considering contributing! This project is a learning-oriented physics simulation library.

## Development Setup

```bash
cd extensions
pip install -e ".[dev]"
```

## Running Simulations

```bash
physics-modeling list                  # see all available
physics-modeling spring-pendulum       # launch one
```

## Code Standards

- Python 3.10+
- Type annotations on all public functions
- NumPy-style docstrings
- Formatted with `ruff check physics_modeling/`
- Type-checked with `mypy --strict physics_modeling/`

## Adding a New Simulation

1. Create a new file in the appropriate subpackage (e.g., `physics_modeling/oscillators/my_sim.py`)
2. Extend `Simulation` from `physics_modeling.core`
3. Implement `initial_state()` and `derivatives()`
4. Create a `_viz.py` file with a `run_my_sim()` function using matplotlib
5. Add it to the CLI in `cli/main.py`
6. Add to the subpackage `__init__.py`

## Pull Request Process

1. Fork the repo
2. Create a feature branch
3. Write your code + tests
4. Run `py scripts/verify.py` (must pass)
5. Run `ruff check` and `mypy --strict`
6. Submit PR with description of what the simulation models
