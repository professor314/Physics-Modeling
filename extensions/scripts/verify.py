#!/usr/bin/env python
"""Quick verification script — checks all simulations in ~5 seconds.

Run from the extensions/ directory:
    py scripts/verify.py

Checks:
  - Every simulation module imports cleanly
  - Every simulation steps without error
  - State actually changes (not frozen)
  - No NaN/Inf values
  - CLI function exists for every sim
"""

import sys
import time
import importlib

import numpy as np


CHECKS = [
    ("spring_pendulum", "physics_modeling.oscillators.spring_pendulum",
     "SpringPendulum", "SpringPendulumConfig", {}, {}),
    ("double_pendulum", "physics_modeling.oscillators.double_pendulum",
     "DoublePendulum", "DoublePendulumConfig", {}, {}),
    ("bouncing", "physics_modeling.gravity.bouncing",
     "BouncingSimulation", "GravityConfig", {"n_objects": 3}, {}),
    ("nbody", "physics_modeling.gravity.nbody",
     "NBodySimulation", "NBodyConfig",
     {"G": 1.0, "softening": 0.01, "integrator": "verlet", "dt": 0.001},
     {"masses": np.array([1e4, 1e4]),
      "positions": np.array([[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]),
      "velocities": np.array([[0.0, -50.0, 0.0], [0.0, 50.0, 0.0]])}),
    ("sir", "physics_modeling.epidemics.sir",
     "SIRSimulation", "SIRConfig", {}, {}),
    ("seir", "physics_modeling.epidemics.seir",
     "SEIRSimulation", "SEIRConfig", {}, {}),
    ("logistic", "physics_modeling.calculus.logistic",
     "LogisticSimulation", "LogisticConfig", {}, {}),
    ("collisions", "physics_modeling.collisions.elastic",
     "CollisionSimulation", "CollisionConfig", {"n_objects": 3}, {}),
    ("gas", "physics_modeling.gas.hard_sphere",
     "HardSphereGas", "GasConfig",
     {"n_particles": 10, "dt": 0.1, "particle_mass": 1.0, "temperature": 3e22}, {}),
    ("lissajous", "physics_modeling.oscillators.lissajous",
     None, None, {}, {}),  # Not a Simulation subclass
    ("riemann", "physics_modeling.calculus.riemann",
     None, None, {}, {}),  # Not a Simulation subclass
]

VIZ_MODULES = [
    ("spring-pendulum", "physics_modeling.oscillators.spring_pendulum_viz", "run_spring_pendulum_3d"),
    ("double-pendulum", "physics_modeling.oscillators.double_pendulum_viz", "run_double_pendulum_2d"),
    ("lissajous", "physics_modeling.oscillators.lissajous_viz", "run_lissajous_3d"),
    ("gravity", "physics_modeling.gravity.bouncing_viz", "run_bouncing_3d"),
    ("nbody", "physics_modeling.gravity.nbody_viz", "run_nbody_3d"),
    ("sir", "physics_modeling.epidemics.sir_viz", "run_sir_2d"),
    ("seir", "physics_modeling.epidemics.seir_viz", "run_seir_2d"),
    ("logistic", "physics_modeling.calculus.logistic_viz", "run_logistic_2d"),
    ("riemann", "physics_modeling.calculus.riemann_viz", "run_riemann_2d"),
    ("collisions", "physics_modeling.collisions.collisions_viz", "run_collisions_3d"),
    ("gas", "physics_modeling.gas.gas_viz", "run_gas_3d"),
]


def main() -> int:
    print("=" * 60)
    print("  physics-modeling verification")
    print("=" * 60)
    start = time.time()
    failures = 0

    # Check simulations
    print("\n--- Simulation checks ---")
    for name, mod_path, cls_name, cfg_name, cfg_kwargs, extra_args in CHECKS:
        try:
            mod = importlib.import_module(mod_path)
            if cls_name is None:
                # Non-simulation module (lissajous, riemann)
                print(f"  ✓ {name:<20} (module imports OK)")
                continue

            cls = getattr(mod, cls_name)
            cfg_cls = getattr(mod, cfg_name)
            cfg = cfg_cls(**cfg_kwargs)

            if extra_args:
                sim = cls(cfg, **extra_args)
            else:
                sim = cls(cfg)

            initial = sim.state.copy()
            for _ in range(50):
                sim.step()

            final = sim.state
            displacement = np.linalg.norm(final - initial)
            has_nan = not np.all(np.isfinite(final))

            if has_nan:
                print(f"  ✗ {name:<20} NaN/Inf in state!")
                failures += 1
            elif displacement < 1e-10:
                print(f"  ✗ {name:<20} state didn't change (frozen)")
                failures += 1
            else:
                print(f"  ✓ {name:<20} moved {displacement:.4f}")

        except Exception as e:
            print(f"  ✗ {name:<20} ERROR: {e}")
            failures += 1

    # Check viz modules
    print("\n--- Viz module checks ---")
    for command, mod_path, func_name in VIZ_MODULES:
        try:
            mod = importlib.import_module(mod_path)
            func = getattr(mod, func_name)
            assert callable(func)
            print(f"  ✓ {command:<20} → {func_name}")
        except Exception as e:
            print(f"  ✗ {command:<20} ERROR: {e}")
            failures += 1

    # Check CLI
    print("\n--- CLI check ---")
    try:
        from physics_modeling.cli.main import SIMULATIONS as CLI_SIMS
        print(f"  ✓ CLI has {len(CLI_SIMS)} commands registered")
    except Exception as e:
        print(f"  ✗ CLI import failed: {e}")
        failures += 1

    elapsed = time.time() - start
    print(f"\n{'=' * 60}")
    if failures == 0:
        print(f"  ALL CHECKS PASSED ({elapsed:.1f}s)")
    else:
        print(f"  {failures} FAILURE(S) ({elapsed:.1f}s)")
    print("=" * 60)

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
