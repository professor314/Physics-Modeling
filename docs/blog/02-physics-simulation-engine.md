# Building a Physics Simulation Engine in Python

*How the physics_modeling package is architected: base classes, numerical integrators, separation of physics from visualization, and property-based testing.*

## The Core Abstraction

Every physics simulation answers the same question: given a system's current state, what is its state at the next instant? Whether you're modeling a spring, an epidemic, or a galaxy of gravitating bodies, the computation follows one pattern: compute derivatives, advance time, repeat.

The `physics_modeling` package encodes this pattern in a `Simulation` base class:

```python
from abc import ABC, abstractmethod
import numpy as np
from physics_modeling.core import SimulationConfig, make_integrator

class Simulation(ABC):
    def __init__(self, config: SimulationConfig) -> None:
        self._dt = config.dt
        self._integrator = make_integrator(config.integrator)
        self._t = 0.0
        self._state = self.initial_state()

    @abstractmethod
    def initial_state(self) -> np.ndarray:
        """Return the starting state vector."""
        ...

    @abstractmethod
    def derivatives(self, state: np.ndarray, t: float) -> np.ndarray:
        """Compute d(state)/dt at the given state and time."""
        ...

    def step(self, dt: float | None = None) -> np.ndarray:
        dt = dt if dt is not None else self._dt
        self._state = self._integrator.step(
            self._state, self._t, dt, self.derivatives
        )
        self._t += dt
        if not np.all(np.isfinite(self._state)):
            raise SimulationDivergenceError(...)
        return self._state
```

A concrete simulation only needs to define two things: what the initial conditions are, and how the state changes over time. Everything else — time-stepping, integrator selection, divergence detection, batch execution — is handled by the base class.

## The State Vector Convention

All simulations encode their state as a flat 1-D numpy float64 array. For a spring pendulum in 3D, that's `[x, y, z, vx, vy, vz]` — six elements. For an N-body simulation with 10 particles, it's `[x0, y0, z0, ..., x9, y9, z9, vx0, vy0, vz0, ..., vx9, vy9, vz9]` — 60 elements.

This flat representation makes the integrators generic. They don't know whether they're integrating a pendulum or a galaxy — they just advance a numpy array forward in time using the derivative function they're given. The physical meaning lives entirely in the `derivatives()` method.

The convention also makes the `run()` method trivial to implement — it collects states into a `(steps, state_dim)` array that's immediately plottable with matplotlib.

## Three Integrators

The package ships with three integrators of increasing sophistication:

### Euler (first-order)

```python
class EulerIntegrator:
    def step(self, state, t, dt, derivatives):
        return state + derivatives(state, t) * dt
```

Fast, simple, inaccurate. Error accumulates as O(dt) per step. Useful for quick visualizations where you don't care about long-term accuracy.

### RK4 (fourth-order Runge-Kutta)

```python
class RK4Integrator:
    def step(self, state, t, dt, derivatives):
        k1 = derivatives(state, t)
        k2 = derivatives(state + 0.5 * dt * k1, t + 0.5 * dt)
        k3 = derivatives(state + 0.5 * dt * k2, t + 0.5 * dt)
        k4 = derivatives(state + dt * k3, t + dt)
        return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
```

Four derivative evaluations per step, but O(dt⁴) local error. The general-purpose workhorse — accurate enough for most simulations without special structure requirements.

### Velocity Verlet (symplectic)

```python
class VerletIntegrator:
    def step(self, state, t, dt, derivatives):
        n = len(state) // 2
        pos, vel = state[:n], state[n:]
        acc = derivatives(state, t)[n:]
        new_pos = pos + vel * dt + 0.5 * acc * dt**2
        mid_state = np.concatenate([new_pos, vel])
        new_acc = derivatives(mid_state, t + dt)[n:]
        new_vel = vel + 0.5 * (acc + new_acc) * dt
        return np.concatenate([new_pos, new_vel])
```

Symplectic — it preserves the geometric structure of Hamiltonian systems. Energy doesn't drift over long runs the way it does with Euler or even RK4. Required for the N-body simulation where you want stable orbits over thousands of time steps.

The Verlet integrator requires a specific state layout: first half is positions, second half is velocities. This constraint is validated at runtime — if you pass an odd-length state vector, it raises a `ValueError`.

## Separation of Physics from Visualization

Each simulation module follows a consistent pattern:

```
physics_modeling/oscillators/
├── spring_pendulum.py       # Pure physics: config, state, derivatives
└── spring_pendulum_viz.py   # matplotlib figure, sliders, animation
```

The physics file defines a `Simulation` subclass. It has no imports from matplotlib, no figure creation, no event handling. It takes in parameters and produces numpy arrays.

The viz file imports the physics class, creates a matplotlib figure, runs the simulation in a timer callback, and draws the results. Sliders call `sim.config.k = new_value` and the next animation frame uses the new parameter.

This separation has concrete benefits:

1. **Testable physics.** You can instantiate `SpringPendulum` in a test, step it forward, and assert properties of the state — without ever opening a window.

2. **Reusable engine.** Notebooks import the physics class directly. The CLI imports the viz function. A hypothetical web frontend could import just the physics and stream state over a WebSocket.

3. **Minimal dependencies.** The core physics runs with only numpy. Matplotlib is only needed if you want interactive visualization.

## Property-Based Testing

Traditional unit tests verify specific cases: "given these exact inputs, expect this exact output." Property-based testing (via Hypothesis) verifies invariants across randomly generated inputs.

For physics simulations, the interesting properties are:

**Dimensional consistency.** For any valid configuration, `sim.step()` returns an array with the same shape as `sim.initial_state()`.

**Divergence detection.** If a configuration leads to NaN or Inf values (e.g., zero mass, negative spring constant producing runaway oscillation), the simulation raises `SimulationDivergenceError` rather than silently producing garbage.

**Energy bounds.** For conservative systems (no damping, no air resistance), total energy should remain approximately constant over a run. "Approximately" depends on the integrator — Euler drifts badly, RK4 drifts slowly, Verlet conserves energy to machine precision.

**Reversibility.** For the Rubik's cube (which uses the same testing infrastructure), applying a move and its inverse returns to the original state. `apply_move(apply_move(state, U), U') == state` for all states.

A Hypothesis test for the spring pendulum looks like:

```python
from hypothesis import given, settings
from hypothesis.strategies import floats

@given(
    k=floats(min_value=0.1, max_value=100.0),
    mass=floats(min_value=0.1, max_value=50.0),
    dt=floats(min_value=0.0001, max_value=0.05),
)
@settings(max_examples=200)
def test_state_dimension_preserved(k, mass, dt):
    config = SpringPendulumConfig(k=k, mass=mass, dt=dt)
    sim = SpringPendulum(config)
    initial_shape = sim.state.shape
    sim.step()
    assert sim.state.shape == initial_shape
```

Hypothesis generates hundreds of random configurations — extreme spring constants, tiny masses, large time steps — and verifies the invariant holds everywhere. When it finds a failure, it shrinks the example to the minimal reproducing case.

## The CLI Layer

The CLI is deliberately thin. It's an argparse dispatcher that maps subcommands to viz launcher functions:

```bash
$ physics-modeling list
Available simulations:

  spring-pendulum      3D spring pendulum with interactive sliders
  double-pendulum      2D double pendulum with chaotic motion + trail
  gravity              3D bouncing objects under gravity (fountain mode)
  nbody                3D N-body gravitational simulation
  sir                  2D SIR epidemic model with parameter sliders
  ...
```

Each simulation is a lazy import — running `physics-modeling sir` only imports the SIR module, not the entire package. The CLI also checks for display availability before attempting to open a window, giving a clear error message in headless environments.

## Architecture Decisions That Paid Off

**Flat state vectors.** Tempting to use structured objects (position vectors, velocity vectors, per-particle records). But numpy operates on flat arrays, integrators need flat arrays, and matplotlib's `plot(history[:, 0], history[:, 1])` needs flat columns. Fighting this creates needless reshape overhead.

**Dataclass configs.** Each simulation has a frozen dataclass holding all its parameters. This makes configuration serializable, hashable, testable, and IDE-completable. Passing 8 keyword arguments to a constructor invites bugs; passing a typed config object catches them at definition time.

**No global state.** Every `Simulation` instance is independent. You can run three spring pendulums with different parameters in the same process without them interfering. This makes parallel parameter sweeps trivial.

**Integrator as a protocol.** The `Integrator` protocol defines a single method: `step(state, t, dt, derivatives) -> state`. Any object satisfying that interface works. Adding a new integrator (adaptive RK45, leapfrog, symplectic Euler) requires zero changes to existing simulation code.

The result is a library where adding a new simulation means writing one file with `initial_state()` and `derivatives()`, one file with matplotlib visualization, and one line in the CLI dispatcher. The engine handles everything else.
