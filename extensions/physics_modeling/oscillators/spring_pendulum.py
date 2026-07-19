"""Spring pendulum simulation in 3D.

This module provides a spring pendulum model — a point mass attached to a
spring that swings under gravity. The simulation operates in full 3D,
computing the combined effects of spring restoring force, spring damping,
air resistance, and gravity on the bob.

Classes
-------
SpringPendulumConfig
    Dataclass holding all configurable parameters for the spring pendulum.
SpringPendulum
    Simulation class implementing the spring pendulum physics.

Examples
--------
>>> from physics_modeling.oscillators.spring_pendulum import (
...     SpringPendulum,
...     SpringPendulumConfig,
... )
>>> config = SpringPendulumConfig(k=10.0, damping=0.0, mass=1.0)
>>> sim = SpringPendulum(config)
>>> state = sim.step()
>>> state.shape
(6,)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import pi

import numpy as np

from physics_modeling.core.protocols import State
from physics_modeling.core.simulation import Simulation, SimulationConfig

__all__ = ["SpringPendulum", "SpringPendulumConfig"]


@dataclass
class SpringPendulumConfig(SimulationConfig):
    """Configuration for the spring pendulum simulation.

    Parameters
    ----------
    k : float
        Spring constant (N/m). Must be >= 0.
    damping : float
        Spring damping coefficient. Damps radial velocity along the spring.
    mass : float
        Mass of the bob (kg). Must be > 0.
    rest_length : float
        Natural (unstretched) length of the spring (m). Must be > 0.
    g : float
        Gravitational acceleration (m/s²).
    air_resistance : float
        Air resistance coefficient applied to the full velocity vector.
    initial_angle : float
        Initial angle from the negative y-axis (vertical down) in radians.
        The bob starts in the x-y plane at this angle from vertical.
    initial_velocity : tuple[float, float, float]
        Initial velocity components (vx, vy, vz) in m/s.
    dt : float
        Time step size (inherited from SimulationConfig).
    integrator : str
        Integrator name (inherited from SimulationConfig).
    """

    k: float = 10.0
    damping: float = 0.05
    mass: float = 1.0
    rest_length: float = 2.0
    g: float = 9.8
    air_resistance: float = 0.01
    initial_angle: float = 7 * pi / 8
    initial_velocity: tuple[float, float, float] = (0.0, 0.0, 0.5)


class SpringPendulum(Simulation):
    """3D spring pendulum simulation.

    Models a point mass on a spring attached to a fixed pivot at the origin.
    The bob moves under the combined influence of:

    - **Spring restoring force**: pulls the bob toward the rest length
    - **Spring damping**: opposes radial velocity along the spring axis
    - **Air resistance**: opposes the full velocity vector
    - **Gravity**: acts in the negative y-direction

    The state vector is ``[x, y, z, vx, vy, vz]`` — the 3D position and
    velocity of the bob.

    Parameters
    ----------
    config : SpringPendulumConfig
        Configuration dataclass with all physical parameters.

    Raises
    ------
    ValueError
        If ``mass <= 0``, ``k < 0``, or ``rest_length <= 0``.

    Examples
    --------
    >>> config = SpringPendulumConfig(k=10.0, damping=0.0, mass=1.0)
    >>> sim = SpringPendulum(config)
    >>> sim.state.shape
    (6,)
    >>> sim.t
    0.0
    """

    def __init__(self, config: SpringPendulumConfig) -> None:
        if config.mass <= 0:
            raise ValueError(
                f"mass must be positive, got {config.mass}"
            )
        if config.k < 0:
            raise ValueError(
                f"spring constant k must be non-negative, got {config.k}"
            )
        if config.rest_length <= 0:
            raise ValueError(
                f"rest_length must be positive, got {config.rest_length}"
            )
        self._config = config
        super().__init__(config)

    @property
    def config(self) -> SpringPendulumConfig:
        """The simulation configuration."""
        return self._config

    def initial_state(self) -> State:
        """Compute the initial state from angle and rest length.

        The bob is placed at a distance of ``rest_length`` from the origin,
        at the configured ``initial_angle`` from the negative y-axis
        (vertical down), in the x-y plane.

        Returns
        -------
        State
            A 6-element array ``[x, y, z, vx, vy, vz]``.
        """
        cfg = self._config
        angle = cfg.initial_angle

        # Position: angle measured from negative y-axis (vertical down)
        # At angle=0, bob hangs straight down at (0, -rest_length, 0)
        # At angle=pi/2, bob is at (rest_length, 0, 0)
        x = cfg.rest_length * np.sin(angle)
        y = -cfg.rest_length * np.cos(angle)
        z = 0.0

        vx, vy, vz = cfg.initial_velocity

        return np.array([x, y, z, vx, vy, vz], dtype=np.float64)

    def derivatives(self, state: State, t: float) -> State:
        """Compute the time derivatives of the state vector.

        Computes the net force on the bob from spring, damping, air
        resistance, and gravity, then returns velocities and accelerations.

        Parameters
        ----------
        state : State
            Current state ``[x, y, z, vx, vy, vz]``.
        t : float
            Current simulation time (unused, system is autonomous).

        Returns
        -------
        State
            Derivative vector ``[vx, vy, vz, ax, ay, az]``.
        """
        cfg = self._config

        # Unpack state
        pos = state[:3]
        vel = state[3:]

        # Distance from pivot (origin)
        distance = np.linalg.norm(pos)

        # Handle degenerate case where bob is at the pivot
        if distance < 1e-12:
            pos_hat = np.array([0.0, -1.0, 0.0])
            distance = 1e-12
        else:
            pos_hat = pos / distance

        # Spring extension (positive = stretched beyond rest length)
        extension = distance - cfg.rest_length

        # Spring restoring force: pulls bob toward rest length
        # F_spring = -k * extension * pos_hat
        f_spring = -cfg.k * extension * pos_hat

        # Spring damping: opposes radial velocity component
        # F_damp = -damping * dot(vel, pos_hat) * pos_hat
        radial_velocity = np.dot(vel, pos_hat)
        f_damp = -cfg.damping * radial_velocity * pos_hat

        # Air resistance: opposes full velocity
        # F_air = -air_resistance * vel
        f_air = -cfg.air_resistance * vel

        # Gravity: acts in negative y-direction
        # F_gravity = [0, -mass*g, 0]
        f_gravity = np.array([0.0, -cfg.mass * cfg.g, 0.0])

        # Net force and acceleration
        f_net = f_spring + f_damp + f_air + f_gravity
        acceleration = f_net / cfg.mass

        # Return [vx, vy, vz, ax, ay, az]
        return np.concatenate([vel, acceleration])
