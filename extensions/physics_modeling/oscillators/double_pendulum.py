"""Double pendulum simulation using Lagrangian mechanics.

This module implements a classical double pendulum — two rigid rods
connected end-to-end with point masses at each joint, swinging under
gravity. The system is chaotic for large-angle initial conditions.

Classes
-------
DoublePendulumConfig
    Configuration dataclass holding lengths, masses, and initial angles.
DoublePendulum
    Simulation subclass solving the Lagrangian equations of motion.

Examples
--------
>>> from physics_modeling.oscillators.double_pendulum import (
...     DoublePendulum,
...     DoublePendulumConfig,
... )
>>> config = DoublePendulumConfig(theta1_0=2.0, theta2_0=2.0)
>>> sim = DoublePendulum(config)
>>> sim.state.shape
(4,)
>>> sim.state  # [theta1, theta2, omega1, omega2]
array([2., 2., 0., 0.])
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from physics_modeling.core.simulation import Simulation, SimulationConfig

__all__ = ["DoublePendulum", "DoublePendulumConfig"]


@dataclass
class DoublePendulumConfig(SimulationConfig):
    """Configuration for the double pendulum simulation.

    Parameters
    ----------
    L1 : float
        Length of the first rod (m).
    L2 : float
        Length of the second rod (m).
    m1 : float
        Mass of the first bob (kg).
    m2 : float
        Mass of the second bob (kg).
    g : float
        Gravitational acceleration (m/s²).
    theta1_0 : float
        Initial angle of the first rod from vertical (radians).
    theta2_0 : float
        Initial angle of the second rod from vertical (radians).
    omega1_0 : float
        Initial angular velocity of the first rod (rad/s).
    omega2_0 : float
        Initial angular velocity of the second rod (rad/s).
    dt : float
        Time step size (inherited from SimulationConfig).
    integrator : str
        Integrator name (inherited from SimulationConfig).
    """

    L1: float = 1.0
    L2: float = 1.0
    m1: float = 1.0
    m2: float = 1.0
    g: float = 9.8
    theta1_0: float = 2.0
    theta2_0: float = 2.0
    omega1_0: float = 0.0
    omega2_0: float = 0.0


class DoublePendulum(Simulation):
    """Double pendulum simulation using Lagrangian equations of motion.

    Solves the coupled second-order ODE system derived from the Lagrangian
    of a double pendulum. The state vector is ``[θ1, θ2, ω1, ω2]`` where
    θ are angles from vertical and ω are angular velocities.

    The equations of motion are::

        ω1' = [-g(2m1+m2)sinθ1 - m2*g*sin(θ1-2θ2)
                - 2sin(θ1-θ2)*m2*(ω2²L2 + ω1²L1*cos(θ1-θ2))]
               / [L1*(2m1 + m2 - m2*cos(2θ1 - 2θ2))]

        ω2' = [2sin(θ1-θ2)*(ω1²L1*(m1+m2) + g*(m1+m2)*cosθ1
                + ω2²L2*m2*cos(θ1-θ2))]
               / [L2*(2m1 + m2 - m2*cos(2θ1 - 2θ2))]

    Parameters
    ----------
    config : DoublePendulumConfig
        Configuration with rod lengths, masses, and initial conditions.

    Raises
    ------
    ValueError
        If any length or mass is non-positive.

    Examples
    --------
    >>> config = DoublePendulumConfig(L1=1.0, L2=1.0, m1=1.0, m2=1.0)
    >>> sim = DoublePendulum(config)
    >>> sim.step()  # doctest: +SKIP
    array([...])
    """

    def __init__(self, config: DoublePendulumConfig) -> None:
        self._validate_config(config)
        self._config = config
        super().__init__(config)

    @staticmethod
    def _validate_config(config: DoublePendulumConfig) -> None:
        """Validate double pendulum configuration parameters.

        Parameters
        ----------
        config : DoublePendulumConfig
            Configuration to validate.

        Raises
        ------
        ValueError
            If lengths or masses are non-positive.
        """
        if config.L1 <= 0:
            raise ValueError(f"L1 must be positive, got {config.L1}")
        if config.L2 <= 0:
            raise ValueError(f"L2 must be positive, got {config.L2}")
        if config.m1 <= 0:
            raise ValueError(f"m1 must be positive, got {config.m1}")
        if config.m2 <= 0:
            raise ValueError(f"m2 must be positive, got {config.m2}")

    def initial_state(self) -> NDArray[np.float64]:
        """Return the initial state vector [θ1, θ2, ω1, ω2].

        Returns
        -------
        NDArray[np.float64]
            Array of shape ``(4,)`` with initial angles and angular velocities.
        """
        return np.array(
            [
                self._config.theta1_0,
                self._config.theta2_0,
                self._config.omega1_0,
                self._config.omega2_0,
            ],
            dtype=np.float64,
        )

    def derivatives(
        self, state: NDArray[np.float64], t: float
    ) -> NDArray[np.float64]:
        """Compute time derivatives using Lagrangian equations of motion.

        Parameters
        ----------
        state : NDArray[np.float64]
            Current state vector ``[θ1, θ2, ω1, ω2]``.
        t : float
            Current simulation time (unused, system is autonomous).

        Returns
        -------
        NDArray[np.float64]
            Derivatives ``[dθ1/dt, dθ2/dt, dω1/dt, dω2/dt]``.
        """
        theta1, theta2, omega1, omega2 = state
        L1 = self._config.L1
        L2 = self._config.L2
        m1 = self._config.m1
        m2 = self._config.m2
        g = self._config.g

        delta = theta1 - theta2
        denom = 2.0 * m1 + m2 - m2 * np.cos(2.0 * delta)

        # Angular acceleration of first pendulum
        num1 = (
            -g * (2.0 * m1 + m2) * np.sin(theta1)
            - m2 * g * np.sin(theta1 - 2.0 * theta2)
            - 2.0 * np.sin(delta) * m2
            * (omega2**2 * L2 + omega1**2 * L1 * np.cos(delta))
        )
        alpha1 = num1 / (L1 * denom)

        # Angular acceleration of second pendulum
        num2 = (
            2.0 * np.sin(delta)
            * (
                omega1**2 * L1 * (m1 + m2)
                + g * (m1 + m2) * np.cos(theta1)
                + omega2**2 * L2 * m2 * np.cos(delta)
            )
        )
        alpha2 = num2 / (L2 * denom)

        return np.array([omega1, omega2, alpha1, alpha2], dtype=np.float64)

    @property
    def config(self) -> DoublePendulumConfig:
        """The simulation configuration."""
        return self._config

    def cartesian_positions(
        self, state: NDArray[np.float64] | None = None
    ) -> tuple[tuple[float, float], tuple[float, float]]:
        """Convert angular state to Cartesian (x, y) positions of both bobs.

        Parameters
        ----------
        state : NDArray[np.float64] | None
            State to convert. If ``None``, uses the current state.

        Returns
        -------
        tuple[tuple[float, float], tuple[float, float]]
            ``((x1, y1), (x2, y2))`` positions of the first and second bobs.
            The pivot is at the origin; y points downward.
        """
        if state is None:
            state = self._state
        theta1, theta2 = state[0], state[1]
        L1, L2 = self._config.L1, self._config.L2

        x1 = L1 * np.sin(theta1)
        y1 = -L1 * np.cos(theta1)

        x2 = x1 + L2 * np.sin(theta2)
        y2 = y1 - L2 * np.cos(theta2)

        return (float(x1), float(y1)), (float(x2), float(y2))
