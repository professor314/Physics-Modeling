"""Numerical integrators for time-stepping differential equations.

This module provides three integrators of increasing sophistication:

* **EulerIntegrator** — first-order explicit Euler (fast, low accuracy).
* **RK4Integrator** — fourth-order Runge-Kutta (general-purpose, high accuracy).
* **VerletIntegrator** — velocity Verlet symplectic integrator (energy-conserving
  for Hamiltonian systems).

All integrators satisfy the :class:`~physics_modeling.core.protocols.Integrator`
protocol and operate on NumPy float64 state vectors.
"""

from __future__ import annotations

import numpy as np

from physics_modeling.core.protocols import DerivativeFn, State

__all__ = [
    "EulerIntegrator",
    "RK4Integrator",
    "VerletIntegrator",
    "make_integrator",
]


class EulerIntegrator:
    """First-order explicit Euler integrator.

    Computes the next state as::

        x(t + dt) = x(t) + f(x, t) * dt

    Simple and fast but accumulates significant error over many steps.
    Best suited for visualization where exact accuracy is not critical.
    """

    def step(
        self,
        state: State,
        t: float,
        dt: float,
        derivatives: DerivativeFn,
    ) -> State:
        """Advance the state by one Euler step.

        Parameters
        ----------
        state : State
            Current state vector.
        t : float
            Current simulation time.
        dt : float
            Time step size.
        derivatives : DerivativeFn
            Function computing d(state)/dt.

        Returns
        -------
        State
            New state after one Euler step.
        """
        return state + derivatives(state, t) * dt


class RK4Integrator:
    """Fourth-order Runge-Kutta integrator.

    Evaluates the derivative function four times per step and combines
    the results with standard weights (1/6, 1/3, 1/3, 1/6)::

        k1 = f(x, t)
        k2 = f(x + 0.5*dt*k1, t + 0.5*dt)
        k3 = f(x + 0.5*dt*k2, t + 0.5*dt)
        k4 = f(x + dt*k3, t + dt)
        x(t + dt) = x(t) + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)

    Offers excellent accuracy for smooth problems without requiring
    energy-conservation guarantees.
    """

    def step(
        self,
        state: State,
        t: float,
        dt: float,
        derivatives: DerivativeFn,
    ) -> State:
        """Advance the state by one RK4 step.

        Parameters
        ----------
        state : State
            Current state vector.
        t : float
            Current simulation time.
        dt : float
            Time step size.
        derivatives : DerivativeFn
            Function computing d(state)/dt.

        Returns
        -------
        State
            New state after one fourth-order Runge-Kutta step.
        """
        k1 = derivatives(state, t)
        k2 = derivatives(state + 0.5 * dt * k1, t + 0.5 * dt)
        k3 = derivatives(state + 0.5 * dt * k2, t + 0.5 * dt)
        k4 = derivatives(state + dt * k3, t + dt)
        return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


class VerletIntegrator:
    """Velocity Verlet symplectic integrator.

    Designed for Hamiltonian systems where the state vector is structured as
    ``[positions..., velocities...]`` with equal-length halves. The algorithm
    preserves the symplectic structure, providing excellent long-term energy
    conservation for conservative systems.

    Update rules::

        new_pos = pos + vel*dt + 0.5*acc*dt²
        new_vel = vel + 0.5*(acc + new_acc)*dt

    where ``acc`` is the acceleration (second half of the derivative vector)
    evaluated at the current state, and ``new_acc`` is the acceleration at
    the predicted new position.

    Notes
    -----
    The state vector **must** have even length. The first half is interpreted
    as generalised positions and the second half as generalised velocities.
    """

    def step(
        self,
        state: State,
        t: float,
        dt: float,
        derivatives: DerivativeFn,
    ) -> State:
        """Advance the state by one Velocity Verlet step.

        Parameters
        ----------
        state : State
            Current state vector of shape ``(2*n,)`` where the first *n*
            elements are positions and the last *n* are velocities.
        t : float
            Current simulation time.
        dt : float
            Time step size.
        derivatives : DerivativeFn
            Function computing d(state)/dt. Must return a vector whose
            second half represents acceleration.

        Returns
        -------
        State
            New state after one Velocity Verlet step.

        Raises
        ------
        ValueError
            If the state vector has odd length.
        """
        if len(state) % 2 != 0:
            raise ValueError(
                f"VerletIntegrator requires an even-length state vector, got {len(state)}"
            )

        n = len(state) // 2
        pos = state[:n]
        vel = state[n:]

        # Current acceleration (second half of derivatives)
        acc = derivatives(state, t)[n:]

        # Position update
        new_pos = pos + vel * dt + 0.5 * acc * dt**2

        # Acceleration at new position (use current velocity as placeholder)
        mid_state = np.concatenate([new_pos, vel])
        new_acc = derivatives(mid_state, t + dt)[n:]

        # Velocity update
        new_vel = vel + 0.5 * (acc + new_acc) * dt

        return np.concatenate([new_pos, new_vel])


def make_integrator(name: str) -> EulerIntegrator | RK4Integrator | VerletIntegrator:
    """Create an integrator instance by name.

    Parameters
    ----------
    name : str
        Name of the integrator. Must be one of ``"euler"``, ``"rk4"``, or
        ``"verlet"`` (case-insensitive).

    Returns
    -------
    EulerIntegrator | RK4Integrator | VerletIntegrator
        An instance of the requested integrator.

    Raises
    ------
    ValueError
        If *name* is not a recognised integrator name.

    Examples
    --------
    >>> integrator = make_integrator("rk4")
    >>> isinstance(integrator, RK4Integrator)
    True
    """
    integrators = {
        "euler": EulerIntegrator,
        "rk4": RK4Integrator,
        "verlet": VerletIntegrator,
    }
    key = name.lower().strip()
    if key not in integrators:
        raise ValueError(
            f"Unknown integrator {name!r}. Choose from: {', '.join(integrators)}"
        )
    return integrators[key]()
