"""Logistic growth equation simulation.

This module implements the logistic growth ODE ``dy/dt = r*y*(1 - y/K)`` as a
:class:`Simulation` subclass. It supports overlaying multiple runs with
different step counts to visualize how numerical accuracy depends on step size.

Classes
-------
LogisticConfig
    Configuration dataclass holding growth parameters and time span.
LogisticSimulation
    Simulation subclass solving the logistic equation via the core integrators.

Examples
--------
>>> from physics_modeling.calculus.logistic import LogisticConfig, LogisticSimulation
>>> config = LogisticConfig(y0=100.0, r=0.1, K=1000.0, t_end=75.0)
>>> sim = LogisticSimulation(config)
>>> sim.state
array([100.])
>>> sim.analytical_solution(0.0)
100.0
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

import numpy as np
from numpy.typing import NDArray

from physics_modeling.core.simulation import Simulation, SimulationConfig

__all__ = ["LogisticConfig", "LogisticSimulation"]


@dataclass
class LogisticConfig(SimulationConfig):
    """Configuration for the logistic growth simulation.

    Parameters
    ----------
    y0 : float
        Initial population at t=0. Must be positive.
    r : float
        Intrinsic growth rate. Must be positive.
    K : float
        Carrying capacity (equilibrium population). Must be positive.
    t_end : float
        End time for the simulation (seconds/days).
    dt : float
        Time step size (inherited from SimulationConfig).
    integrator : str
        Integrator name: ``"euler"`` or ``"rk4"`` (inherited).
    """

    y0: float = 100.0
    r: float = 0.1
    K: float = 1000.0
    t_end: float = 75.0


class LogisticSimulation(Simulation):
    """Logistic growth equation simulation.

    Solves the ODE::

        dy/dt = r * y * (1 - y / K)

    where *r* is the growth rate, *K* is the carrying capacity, and *y*
    is the current population. The solution approaches K as t → ∞.

    Parameters
    ----------
    config : LogisticConfig
        Configuration with growth parameters.

    Raises
    ------
    ValueError
        If y0, r, or K are not strictly positive.

    Examples
    --------
    >>> config = LogisticConfig(y0=50.0, r=0.2, K=500.0, t_end=100.0)
    >>> sim = LogisticSimulation(config)
    >>> sim.analytical_solution(100.0)  # doctest: +SKIP
    499.95...
    """

    def __init__(self, config: LogisticConfig) -> None:
        self._validate_config(config)
        self._config = config
        super().__init__(config)

    @staticmethod
    def _validate_config(config: LogisticConfig) -> None:
        """Validate logistic configuration parameters.

        Parameters
        ----------
        config : LogisticConfig
            Configuration to validate.

        Raises
        ------
        ValueError
            If y0, r, or K are not strictly positive.
        """
        if config.y0 <= 0:
            raise ValueError(
                f"Initial population y0 must be > 0, got {config.y0}"
            )
        if config.r <= 0:
            raise ValueError(
                f"Growth rate r must be > 0, got {config.r}"
            )
        if config.K <= 0:
            raise ValueError(
                f"Carrying capacity K must be > 0, got {config.K}"
            )

    def initial_state(self) -> NDArray[np.float64]:
        """Return the initial state vector [y].

        Returns
        -------
        NDArray[np.float64]
            Array of shape ``(1,)`` with ``[y0]``.
        """
        return np.array([self._config.y0], dtype=np.float64)

    def derivatives(
        self, state: NDArray[np.float64], t: float
    ) -> NDArray[np.float64]:
        """Compute time derivative of the logistic state.

        Parameters
        ----------
        state : NDArray[np.float64]
            Current state vector ``[y]``.
        t : float
            Current simulation time (unused, included for integrator API).

        Returns
        -------
        NDArray[np.float64]
            Derivative ``[dy/dt]`` where ``dy/dt = r * y * (1 - y/K)``.
        """
        y = state[0]
        r = self._config.r
        k = self._config.K
        dydt = r * y * (1.0 - y / k)
        return np.array([dydt], dtype=np.float64)

    def analytical_solution(self, t: float) -> float:
        """Compute the exact analytical solution at time *t*.

        The logistic equation has the closed-form solution::

            y(t) = K / (1 + ((K - y0) / y0) * exp(-r * t))

        Parameters
        ----------
        t : float
            Time at which to evaluate the analytical solution.

        Returns
        -------
        float
            Exact population value at time *t*.

        Examples
        --------
        >>> config = LogisticConfig(y0=100.0, r=0.1, K=1000.0)
        >>> sim = LogisticSimulation(config)
        >>> sim.analytical_solution(0.0)
        100.0
        >>> sim.analytical_solution(75.0)  # doctest: +SKIP
        946.6...
        """
        y0 = self._config.y0
        r = self._config.r
        k = self._config.K
        return k / (1.0 + ((k - y0) / y0) * exp(-r * t))

    def run_multiple_step_counts(
        self, step_counts: list[int]
    ) -> list[tuple[NDArray[np.float64], NDArray[np.float64]]]:
        """Run simulation with multiple step counts for convergence analysis.

        Runs the logistic simulation from t=0 to t_end with each given
        number of steps, returning the time and population arrays for each.

        Parameters
        ----------
        step_counts : list[int]
            List of step counts to use. Each run is independent.

        Returns
        -------
        list[tuple[NDArray[np.float64], NDArray[np.float64]]]
            List of (time_array, population_array) tuples, one per step count.

        Examples
        --------
        >>> config = LogisticConfig(y0=100.0, r=0.1, K=1000.0, t_end=75.0)
        >>> sim = LogisticSimulation(config)
        >>> results = sim.run_multiple_step_counts([10, 100, 1000])
        >>> len(results)
        3
        """
        results: list[tuple[NDArray[np.float64], NDArray[np.float64]]] = []
        t_end = self._config.t_end

        for n_steps in step_counts:
            dt = t_end / n_steps
            cfg = LogisticConfig(
                y0=self._config.y0,
                r=self._config.r,
                K=self._config.K,
                t_end=t_end,
                dt=dt,
                integrator=self._config.integrator,
            )
            sim = LogisticSimulation(cfg)
            history = sim.run(t_end, dt)
            t_array = np.linspace(0.0, t_end, n_steps + 1)
            y_array = history[:, 0]
            results.append((t_array, y_array))

        return results
