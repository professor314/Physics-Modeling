"""SIR compartmental epidemic model.

This module implements the classic Susceptible-Infected-Recovered (SIR) model
as a system of coupled ordinary differential equations. The transmission rate
``beta`` is pre-normalized (not divided by N), matching the original Modeling
Motion implementation where ``beta = 0.00001``.

Classes
-------
SIRConfig
    Configuration dataclass holding initial populations and epidemic parameters.
SIRSimulation
    Simulation subclass solving the SIR system via the core integrator engine.

Examples
--------
>>> from physics_modeling.epidemics.sir import SIRConfig, SIRSimulation
>>> config = SIRConfig(S0=45400, I0=2100, R0=2500, beta=0.00001, gamma=1/14)
>>> sim = SIRSimulation(config)
>>> sim.total_population
50000.0
>>> sim.basic_reproduction_number  # beta * N / gamma
7.0
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from physics_modeling.core.simulation import Simulation, SimulationConfig

__all__ = ["SIRConfig", "SIRSimulation"]


@dataclass
class SIRConfig(SimulationConfig):
    """Configuration for the SIR epidemic simulation.

    Parameters
    ----------
    S0 : float
        Initial susceptible population.
    I0 : float
        Initial infected population.
    R0 : float
        Initial recovered population.
    beta : float
        Transmission rate (pre-normalized, not divided by N).
        Must be strictly positive.
    gamma : float
        Recovery rate (1 / average infection duration in days).
        Must be strictly positive.
    dt : float
        Time step size in days (inherited from SimulationConfig).
    integrator : str
        Integrator name: ``"euler"`` or ``"rk4"`` (inherited).
    """

    S0: float = 45400.0
    I0: float = 2100.0
    R0: float = 2500.0
    beta: float = 0.00001
    gamma: float = 1.0 / 14.0


class SIRSimulation(Simulation):
    """SIR compartmental epidemic simulation.

    Solves the coupled ODE system::

        dS/dt = -beta * S * I
        dI/dt =  beta * S * I - gamma * I
        dR/dt =  gamma * I

    The total population N = S + I + R is conserved as an invariant
    since ``dS + dI + dR = 0`` by construction.

    Parameters
    ----------
    config : SIRConfig
        Configuration with initial populations and epidemic parameters.

    Raises
    ------
    ValueError
        If any initial population is negative, or if beta/gamma are
        not strictly positive.

    Examples
    --------
    >>> config = SIRConfig(S0=990, I0=10, R0=0, beta=0.001, gamma=0.1)
    >>> sim = SIRSimulation(config)
    >>> sim.state
    array([990.,  10.,   0.])
    >>> sim.step()  # doctest: +SKIP
    array([...])
    """

    def __init__(self, config: SIRConfig) -> None:
        self._validate_config(config)
        self._config = config
        super().__init__(config)

    @staticmethod
    def _validate_config(config: SIRConfig) -> None:
        """Validate SIR configuration parameters.

        Parameters
        ----------
        config : SIRConfig
            Configuration to validate.

        Raises
        ------
        ValueError
            If populations are negative or rates are non-positive.
        """
        if config.S0 < 0:
            raise ValueError(
                f"Initial susceptible population S0 must be >= 0, got {config.S0}"
            )
        if config.I0 < 0:
            raise ValueError(
                f"Initial infected population I0 must be >= 0, got {config.I0}"
            )
        if config.R0 < 0:
            raise ValueError(
                f"Initial recovered population R0 must be >= 0, got {config.R0}"
            )
        if config.beta <= 0:
            raise ValueError(
                f"Transmission rate beta must be > 0, got {config.beta}"
            )
        if config.gamma <= 0:
            raise ValueError(
                f"Recovery rate gamma must be > 0, got {config.gamma}"
            )

    def initial_state(self) -> NDArray[np.float64]:
        """Return the initial SIR state vector [S, I, R].

        Returns
        -------
        NDArray[np.float64]
            Array of shape ``(3,)`` with ``[S0, I0, R0]``.
        """
        return np.array(
            [self._config.S0, self._config.I0, self._config.R0],
            dtype=np.float64,
        )

    def derivatives(self, state: NDArray[np.float64], t: float) -> NDArray[np.float64]:
        """Compute time derivatives of the SIR state.

        Parameters
        ----------
        state : NDArray[np.float64]
            Current state vector ``[S, I, R]``.
        t : float
            Current simulation time (unused, included for integrator API).

        Returns
        -------
        NDArray[np.float64]
            Derivatives ``[dS/dt, dI/dt, dR/dt]``.
        """
        s, i, _r = state[0], state[1], state[2]
        beta = self._config.beta
        gamma = self._config.gamma

        ds = -beta * s * i
        di = beta * s * i - gamma * i
        dr = gamma * i

        return np.array([ds, di, dr], dtype=np.float64)

    @property
    def total_population(self) -> float:
        """Total population N = S + I + R (should remain constant).

        Returns
        -------
        float
            Sum of all compartments in the current state.
        """
        return float(np.sum(self._state))

    @property
    def basic_reproduction_number(self) -> float:
        """Basic reproduction number R₀ = beta * N / gamma.

        This represents the expected number of secondary infections from
        a single infected individual in a fully susceptible population.

        Returns
        -------
        float
            The basic reproduction number.
        """
        n = self._config.S0 + self._config.I0 + self._config.R0
        return self._config.beta * n / self._config.gamma
