"""Base simulation framework for physics simulations.

This module provides the abstract :class:`Simulation` base class that all
physics simulations extend, along with supporting configuration and error types.

Classes
-------
SimulationConfig
    Dataclass holding shared simulation parameters (time step, integrator choice).
SimulationDivergenceError
    Raised when the simulation state contains NaN or Inf values.
Simulation
    Abstract base class defining the simulation lifecycle.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from physics_modeling.core.integrators import make_integrator

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from physics_modeling.core.protocols import State

__all__ = [
    "Simulation",
    "SimulationConfig",
    "SimulationDivergenceError",
]


@dataclass
class SimulationConfig:
    """Base configuration shared by all simulations.

    Parameters
    ----------
    dt : float
        Default time step size for integration (seconds).
    integrator : str
        Name of the numerical integrator to use. One of ``"euler"``,
        ``"rk4"``, or ``"verlet"`` (case-insensitive).
    """

    dt: float = 0.01
    integrator: str = "rk4"


class SimulationDivergenceError(RuntimeError):
    """Raised when the simulation state contains NaN or Inf values.

    This typically indicates numerical instability caused by a time step
    that is too large for the system dynamics, or a physically impossible
    configuration (e.g., division by zero distance in gravity).
    """


class Simulation(ABC):
    """Abstract base class for all physics simulations.

    Subclasses must implement :meth:`initial_state` and :meth:`derivatives`.
    The base class manages time-stepping, integrator selection, divergence
    detection, and batch execution.

    Parameters
    ----------
    config : SimulationConfig
        Configuration specifying the time step and integrator.

    Attributes
    ----------
    _state : State
        Current simulation state vector.
    _t : float
        Current simulation time.
    _dt : float
        Default time step.
    _integrator
        Numerical integrator instance created from config.

    Examples
    --------
    >>> class Decay(Simulation):
    ...     def initial_state(self):
    ...         return np.array([1.0])
    ...     def derivatives(self, state, t):
    ...         return -state
    >>> sim = Decay(SimulationConfig(dt=0.01, integrator="euler"))
    >>> sim.step()
    array([0.99])
    """

    def __init__(self, config: SimulationConfig) -> None:
        self._dt: float = config.dt
        self._integrator = make_integrator(config.integrator)
        self._t: float = 0.0
        self._state: State = self.initial_state()

    @abstractmethod
    def initial_state(self) -> State:
        """Return the initial state vector for this simulation.

        Returns
        -------
        State
            A 1-D float64 NumPy array representing the starting conditions.
        """
        ...

    @abstractmethod
    def derivatives(self, state: State, t: float) -> State:
        """Compute the time derivatives of the state vector.

        Parameters
        ----------
        state : State
            Current state vector.
        t : float
            Current simulation time.

        Returns
        -------
        State
            Time derivative of the state (same shape as *state*).
        """
        ...

    @property
    def state(self) -> State:
        """Current simulation state vector."""
        return self._state

    @property
    def t(self) -> float:
        """Current simulation time in seconds."""
        return self._t

    def step(self, dt: float | None = None) -> State:
        """Advance the simulation by one time step.

        Parameters
        ----------
        dt : float | None
            Time step size. If ``None``, uses the default from config.

        Returns
        -------
        State
            The new state vector after advancing.

        Raises
        ------
        SimulationDivergenceError
            If the new state contains NaN or Inf values.
        """
        dt = dt if dt is not None else self._dt
        self._state = self._integrator.step(
            self._state, self._t, dt, self.derivatives
        )
        self._t += dt

        if not np.all(np.isfinite(self._state)):
            raise SimulationDivergenceError(
                f"Simulation diverged at t={self._t:.6f}: "
                f"state contains NaN or Inf values."
            )

        return self._state

    def run(self, t_end: float, dt: float | None = None) -> NDArray:
        """Run the simulation from the current time to *t_end*.

        Executes repeated time steps and records the full state history.

        Parameters
        ----------
        t_end : float
            Target end time for the simulation run.
        dt : float | None
            Time step size. If ``None``, uses the default from config.

        Returns
        -------
        NDArray
            Array of shape ``(steps + 1, state_dim)`` containing the state
            at each time step, starting with the current state.

        Raises
        ------
        SimulationDivergenceError
            If the state diverges during the run.
        """
        dt = dt if dt is not None else self._dt
        steps = int((t_end - self._t) / dt)
        history: NDArray = np.zeros((steps + 1, len(self._state)))
        history[0] = self._state

        for i in range(1, steps + 1):
            self.step(dt)
            history[i] = self._state

        return history
