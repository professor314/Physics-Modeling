"""Smoke tests for all visualization modules.

These tests verify that:
1. Every simulation can be instantiated with its viz defaults
2. After N steps, the state has actually changed (particles moved)
3. No NaN/Inf values in state
4. The viz function exists and is importable
5. The viz file has a __main__ block

Run: py -m pytest tests/test_viz_smoke.py -v
"""

import importlib
import inspect
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # noqa: E402 — headless backend for CI

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# All simulations with their viz configs
# ---------------------------------------------------------------------------

SIMULATIONS = [
    {
        "name": "spring_pendulum",
        "module": "physics_modeling.oscillators.spring_pendulum",
        "class": "SpringPendulum",
        "config_class": "SpringPendulumConfig",
        "viz_module": "physics_modeling.oscillators.spring_pendulum_viz",
        "viz_func": "run_spring_pendulum_3d",
        "steps": 100,
        "min_displacement": 0.01,
    },
    {
        "name": "double_pendulum",
        "module": "physics_modeling.oscillators.double_pendulum",
        "class": "DoublePendulum",
        "config_class": "DoublePendulumConfig",
        "viz_module": "physics_modeling.oscillators.double_pendulum_viz",
        "viz_func": "run_double_pendulum_2d",
        "steps": 100,
        "min_displacement": 0.001,
    },
    {
        "name": "bouncing",
        "module": "physics_modeling.gravity.bouncing",
        "class": "BouncingSimulation",
        "config_class": "GravityConfig",
        "config_kwargs": {"n_objects": 3},
        "viz_module": "physics_modeling.gravity.bouncing_viz",
        "viz_func": "run_bouncing_3d",
        "steps": 50,
        "min_displacement": 0.01,
    },
    {
        "name": "nbody",
        "module": "physics_modeling.gravity.nbody",
        "class": "NBodySimulation",
        "config_class": "NBodyConfig",
        "config_kwargs": {"G": 1.0, "softening": 0.01, "integrator": "verlet", "dt": 0.001},
        "extra_args": {
            "masses": np.array([1e4, 1e4]),
            "positions": np.array([[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]),
            "velocities": np.array([[0.0, -50.0, 0.0], [0.0, 50.0, 0.0]]),
        },
        "viz_module": "physics_modeling.gravity.nbody_viz",
        "viz_func": "run_nbody_3d",
        "steps": 100,
        "min_displacement": 0.001,
    },
    {
        "name": "sir",
        "module": "physics_modeling.epidemics.sir",
        "class": "SIRSimulation",
        "config_class": "SIRConfig",
        "viz_module": "physics_modeling.epidemics.sir_viz",
        "viz_func": "run_sir_2d",
        "steps": 100,
        "min_displacement": 0.1,
    },
    {
        "name": "seir",
        "module": "physics_modeling.epidemics.seir",
        "class": "SEIRSimulation",
        "config_class": "SEIRConfig",
        "viz_module": "physics_modeling.epidemics.seir_viz",
        "viz_func": "run_seir_2d",
        "steps": 100,
        "min_displacement": 0.001,
    },
    {
        "name": "logistic",
        "module": "physics_modeling.calculus.logistic",
        "class": "LogisticSimulation",
        "config_class": "LogisticConfig",
        "viz_module": "physics_modeling.calculus.logistic_viz",
        "viz_func": "run_logistic_2d",
        "steps": 100,
        "min_displacement": 0.01,
    },
    {
        "name": "collisions",
        "module": "physics_modeling.collisions.elastic",
        "class": "CollisionSimulation",
        "config_class": "CollisionConfig",
        "config_kwargs": {"n_objects": 3, "dimensions": 3},
        "viz_module": "physics_modeling.collisions.collisions_viz",
        "viz_func": "run_collisions_3d",
        "steps": 50,
        "min_displacement": 0.01,
    },
    {
        "name": "gas",
        "module": "physics_modeling.gas.hard_sphere",
        "class": "HardSphereGas",
        "config_class": "GasConfig",
        "config_kwargs": {
            "n_particles": 10, "dt": 0.1, "particle_radius": 0.3,
            "particle_mass": 1.0, "temperature": 3e22,
        },
        "viz_module": "physics_modeling.gas.gas_viz",
        "viz_func": "run_gas_3d",
        "steps": 20,
        "min_displacement": 0.01,
    },
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("sim", SIMULATIONS, ids=[s["name"] for s in SIMULATIONS])
def test_simulation_state_changes(sim):
    """After N steps, the state should have moved by at least min_displacement."""
    mod = importlib.import_module(sim["module"])
    cls = getattr(mod, sim["class"])
    config_cls = getattr(mod, sim["config_class"])

    config_kwargs = sim.get("config_kwargs", {})
    config = config_cls(**config_kwargs)

    extra_args = sim.get("extra_args", {})
    if extra_args:
        instance = cls(config, **extra_args)
    else:
        instance = cls(config)

    initial_state = instance.state.copy()

    for _ in range(sim["steps"]):
        instance.step()

    final_state = instance.state
    displacement = np.linalg.norm(final_state - initial_state)

    assert displacement > sim["min_displacement"], (
        f"{sim['name']}: state didn't change enough after {sim['steps']} steps. "
        f"Displacement: {displacement:.2e}, expected > {sim['min_displacement']}"
    )


@pytest.mark.parametrize("sim", SIMULATIONS, ids=[s["name"] for s in SIMULATIONS])
def test_no_nan_inf(sim):
    """After N steps, state should have no NaN or Inf values."""
    mod = importlib.import_module(sim["module"])
    cls = getattr(mod, sim["class"])
    config_cls = getattr(mod, sim["config_class"])

    config_kwargs = sim.get("config_kwargs", {})
    config = config_cls(**config_kwargs)

    extra_args = sim.get("extra_args", {})
    if extra_args:
        instance = cls(config, **extra_args)
    else:
        instance = cls(config)

    for _ in range(sim["steps"]):
        instance.step()

    assert np.all(np.isfinite(instance.state)), (
        f"{sim['name']}: state contains NaN or Inf after {sim['steps']} steps"
    )


@pytest.mark.parametrize("sim", SIMULATIONS, ids=[s["name"] for s in SIMULATIONS])
def test_viz_function_importable(sim):
    """The viz function should be importable."""
    mod = importlib.import_module(sim["viz_module"])
    func = getattr(mod, sim["viz_func"])
    assert callable(func), f"{sim['viz_func']} is not callable"


@pytest.mark.parametrize("sim", SIMULATIONS, ids=[s["name"] for s in SIMULATIONS])
def test_viz_has_main_block(sim):
    """Each viz file should have an if __name__ == '__main__' block."""
    mod = importlib.import_module(sim["viz_module"])
    source_file = inspect.getfile(mod)
    content = Path(source_file).read_text(encoding="utf-8")
    assert "__name__" in content and "__main__" in content, (
        f"{sim['viz_module']} is missing if __name__ == '__main__' block"
    )


def test_cli_dispatch_matches_viz_functions():
    """All CLI dispatch entries should point to importable functions."""
    from physics_modeling.cli.main import SIMULATIONS as CLI_SIMS

    # These are the expected mappings (command -> viz function import path)
    expected_functions = {
        "spring-pendulum": "physics_modeling.oscillators.spring_pendulum_viz.run_spring_pendulum_3d",
        "double-pendulum": "physics_modeling.oscillators.double_pendulum_viz.run_double_pendulum_2d",
        "gravity": "physics_modeling.gravity.bouncing_viz.run_bouncing_3d",
        "nbody": "physics_modeling.gravity.nbody_viz.run_nbody_3d",
        "sir": "physics_modeling.epidemics.sir_viz.run_sir_2d",
        "seir": "physics_modeling.epidemics.seir_viz.run_seir_2d",
        "logistic": "physics_modeling.calculus.logistic_viz.run_logistic_2d",
        "lissajous": "physics_modeling.oscillators.lissajous_viz.run_lissajous_3d",
        "riemann": "physics_modeling.calculus.riemann_viz.run_riemann_2d",
        "collisions": "physics_modeling.collisions.collisions_viz.run_collisions_3d",
        "gas": "physics_modeling.gas.gas_viz.run_gas_3d",
    }

    for command, func_path in expected_functions.items():
        assert command in CLI_SIMS, f"CLI missing command: {command}"
        module_path, func_name = func_path.rsplit(".", 1)
        mod = importlib.import_module(module_path)
        func = getattr(mod, func_name, None)
        assert func is not None, (
            f"CLI command '{command}' references {func_path} which doesn't exist"
        )
