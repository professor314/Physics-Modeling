"""SEIR compartmental epidemic model.

This module implements the Susceptible-Exposed-Infected-Recovered (SEIR)
model as a system of coupled ordinary differential equations. The SEIR
model extends the SIR model by adding an Exposed (latent) compartment for
individuals who have been infected but are not yet infectious.

The transmission rate ``beta`` uses the normalized form β*S*I/N where
N = S + E + I + R is the total population.

Classes
-------
SEIRConfig
    Configuration dataclass holding initial populations and epidemic parameters.
SEIRSimulation
    Simulation subclass solving the SEIR system via the core integrator engine.

Examples
--------
>>> from physics_modeling.epidemics.seir import SEIRConfig, SEIRSimulation
>>> config = SEIRConfig(S0=999, E0=0, I0=1, R0=0, beta=0.5, sigma=0.2, gamma=0.1)
>>> sim = SEIRSimulation(config)
>>> sim.total_population
1000.0
>>> sim.basic_reproduction_number  # beta / gamma
5.0
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from physics_modeling.core.simulation import Simulation, SimulationConfig

__all__ = ["SEIRConfig", "SEIRSimulation"]


@dataclass
class SEIRConfig(SimulationConfig):
    """Configuration for the SEIR epidemic simulation.

    Parameters
    ----------
    S0 : float
        Initial susceptible population.
    E0 : float
        Initial exposed (latent) population.
    I0 : float
        Initial infected population.
    R0 : float
        Initial recovered population.
    beta : float
        Transmission rate (normalized β/N form used in derivatives).
        Must be strictly positive.
    sigma : float
        Incubation rate (1 / average incubation period in days).
        Rate at which exposed individuals become infectious.
        Must be strictly positive.
    gamma : float
        Recovery rate (1 / average infection duration in days).
        Must be strictly positive.
    dt : float
        Time step size in days (inherited from SimulationConfig).
    integrator : str
        Integrator name: ``"euler"`` or ``"rk4"`` (inherited).
    """

    S0: float = 999.0
    E0: float = 0.0
    I0: float = 1.0
    R0: float = 0.0
    beta: float = 0.5
    sigma: float = 1.0 / 5.0
    gamma: float = 1.0 / 14.0


class SEIRSimulation(Simulation):
    """SEIR compartmental epidemic simulation.

    Solves the coupled ODE system::

        dS/dt = -β * S * I / N
        dE/dt =  β * S * I / N - σ * E
        dI/dt =  σ * E - γ * I
        dR/dt =  γ * I

    where N = S + E + I + R is the total population (conserved).

    Parameters
    ----------
    config : SEIRConfig
        Configuration with initial populations and epidemic parameters.

    Raises
    ------
    ValueError
        If any initial population is negative, or if beta/sigma/gamma are
        not strictly positive.

    Examples
    --------
    >>> config = SEIRConfig(S0=990, E0=5, I0=5, R0=0, beta=0.4, sigma=0.2, gamma=0.1)
    >>> sim = SEIRSimulation(config)
    >>> sim.state
    array([990.,   5.,   5.,   0.])
    >>> sim.total_population
    1000.0
    """

    def __init__(self, config: SEIRConfig) -> None:
        self._validate_config(config)
        self._config = config
        super().__init__(config)

    @staticmethod
    def _validate_config(config: SEIRConfig) -> None:
        """Validate SEIR configuration parameters.

        Parameters
        ----------
        config : SEIRConfig
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
        if config.E0 < 0:
            raise ValueError(
                f"Initial exposed population E0 must be >= 0, got {config.E0}"
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
        if config.sigma <= 0:
            raise ValueError(
                f"Incubation rate sigma must be > 0, got {config.sigma}"
            )
        if config.gamma <= 0:
            raise ValueError(
                f"Recovery rate gamma must be > 0, got {config.gamma}"
            )

    def initial_state(self) -> NDArray[np.float64]:
        """Return the initial SEIR state vector [S, E, I, R].

        Returns
        -------
        NDArray[np.float64]
            Array of shape ``(4,)`` with ``[S0, E0, I0, R0]``.
        """
        return np.array(
            [self._config.S0, self._config.E0, self._config.I0, self._config.R0],
            dtype=np.float64,
        )

    def derivatives(
        self, state: NDArray[np.float64], t: float
    ) -> NDArray[np.float64]:
        """Compute time derivatives of the SEIR state.

        Parameters
        ----------
        state : NDArray[np.float64]
            Current state vector ``[S, E, I, R]``.
        t : float
            Current simulation time (unused, included for integrator API).

        Returns
        -------
        NDArray[np.float64]
            Derivatives ``[dS/dt, dE/dt, dI/dt, dR/dt]``.
        """
        s, e, i, r = state[0], state[1], state[2], state[3]
        beta = self._config.beta
        sigma = self._config.sigma
        gamma = self._config.gamma
        n = s + e + i + r

        # Prevent division by zero if population is zero
        if n < 1e-12:
            return np.zeros(4, dtype=np.float64)

        infection_rate = beta * s * i / n

        ds = -infection_rate
        de = infection_rate - sigma * e
        di = sigma * e - gamma * i
        dr = gamma * i

        return np.array([ds, de, di, dr], dtype=np.float64)

    @property
    def config(self) -> SEIRConfig:
        """The simulation configuration."""
        return self._config

    @property
    def total_population(self) -> float:
        """Total population N = S + E + I + R (should remain constant).

        Returns
        -------
        float
            Sum of all compartments in the current state.
        """
        return float(np.sum(self._state))

    @property
    def basic_reproduction_number(self) -> float:
        """Basic reproduction number R₀ = β / γ.

        For the SEIR model with normalized β, this represents the expected
        number of secondary infections from a single infected individual
        in a fully susceptible population.

        Returns
        -------
        float
            The basic reproduction number.
        """
        return self._config.beta / self._config.gamma
