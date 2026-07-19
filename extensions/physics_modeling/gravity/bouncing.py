"""Gravity and bouncing simulation for single or multiple objects.

This module models spherical objects falling under constant gravitational
acceleration with elastic floor collisions. Objects that exit the simulation
boundary are removed to prevent unbounded memory growth.

Classes
-------
GravityConfig
    Configuration dataclass for the bouncing simulation.
BouncingSimulation
    Simulation of objects falling under gravity with floor bouncing.

Functions
---------
create_fountain_config
    Create a pre-configured :class:`GravityConfig` for fountain mode.

Examples
--------
>>> from physics_modeling.gravity.bouncing import BouncingSimulation, GravityConfig
>>> config = GravityConfig(n_objects=1, g=9.8, restitution=0.8)
>>> sim = BouncingSimulation(config)
>>> sim.step()  # advance one time step
array([...])
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from physics_modeling.core.simulation import Simulation, SimulationConfig

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from physics_modeling.core.protocols import State

__all__ = [
    "BouncingSimulation",
    "GravityConfig",
    "create_fountain_config",
]


@dataclass
class GravityConfig(SimulationConfig):
    """Configuration for the gravity/bouncing simulation.

    Parameters
    ----------
    dt : float
        Time step size for integration (seconds).
    integrator : str
        Numerical integrator name (``"euler"``, ``"rk4"``, or ``"verlet"``).
    g : float
        Gravitational acceleration magnitude (m/s²). Must be >= 0.
    restitution : float
        Coefficient of restitution for floor bounces. Must be in [0, 1].
        A value of 1.0 means perfectly elastic bounces; 0.0 means no bounce.
    boundary_y : float
        Y-coordinate of the floor plane.
    extent : float
        Maximum distance from the origin in x/z directions before an object
        is removed. Must be > 0.
    n_objects : int
        Number of objects to simulate. Must be >= 1.
    initial_positions : NDArray | None
        Optional initial positions array of shape ``(n_objects, 3)``.
        If ``None``, positions are randomly generated above the floor.
    initial_velocities : NDArray | None
        Optional initial velocities array of shape ``(n_objects, 3)``.
        If ``None``, velocities are randomly generated.

    Raises
    ------
    ValueError
        If parameters fail validation constraints.
    """

    g: float = 9.8
    restitution: float = 0.8
    boundary_y: float = 0.0
    extent: float = 50.0
    n_objects: int = 1
    initial_positions: np.ndarray | None = field(default=None, repr=False)
    initial_velocities: np.ndarray | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.g < 0:
            raise ValueError(
                f"Gravitational acceleration g must be >= 0, got {self.g}"
            )
        if not (0.0 <= self.restitution <= 1.0):
            raise ValueError(
                f"Coefficient of restitution must be in [0, 1], "
                f"got {self.restitution}"
            )
        if self.extent <= 0:
            raise ValueError(
                f"Extent must be > 0, got {self.extent}"
            )
        if self.n_objects < 1:
            raise ValueError(
                f"n_objects must be >= 1, got {self.n_objects}"
            )


class BouncingSimulation(Simulation):
    """Simulation of objects falling under gravity with floor bouncing.

    The state vector is a 1-D array of length ``6 * n_objects``, laid out as::

        [x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, ...]

    Each object has 3 position components followed by 3 velocity components.

    Parameters
    ----------
    config : GravityConfig
        Configuration specifying gravity, restitution, and object count.

    Attributes
    ----------
    _config : GravityConfig
        Stored configuration for physics parameters.
    _active_mask : NDArray[np.bool_]
        Boolean mask indicating which objects are still within bounds.

    Examples
    --------
    >>> config = GravityConfig(n_objects=3, g=9.8, restitution=0.7)
    >>> sim = BouncingSimulation(config)
    >>> sim.active_objects()
    3
    >>> sim.step()
    array([...])
    """

    def __init__(self, config: GravityConfig) -> None:
        self._config: GravityConfig = config
        self._active_mask: NDArray[np.bool_] = np.ones(
            config.n_objects, dtype=np.bool_
        )
        super().__init__(config)

    def initial_state(self) -> State:
        """Return the initial state vector for all objects.

        If ``initial_positions`` or ``initial_velocities`` are provided in the
        config, those are used. Otherwise, objects are placed at random
        positions above the floor with random velocities.

        Returns
        -------
        State
            1-D float64 array of shape ``(6 * n_objects,)``.
        """
        n = self._config.n_objects
        rng = np.random.default_rng()

        # Positions: random x, z in [-extent/2, extent/2], y above floor
        if self._config.initial_positions is not None:
            positions = np.asarray(
                self._config.initial_positions, dtype=np.float64
            )
            if positions.shape != (n, 3):
                raise ValueError(
                    f"initial_positions must have shape ({n}, 3), "
                    f"got {positions.shape}"
                )
        else:
            half_extent = self._config.extent / 4.0
            positions = np.zeros((n, 3), dtype=np.float64)
            positions[:, 0] = rng.uniform(-half_extent, half_extent, size=n)
            positions[:, 1] = rng.uniform(
                self._config.boundary_y + 5.0,
                self._config.boundary_y + 20.0,
                size=n,
            )
            positions[:, 2] = rng.uniform(-half_extent, half_extent, size=n)

        # Velocities: random
        if self._config.initial_velocities is not None:
            velocities = np.asarray(
                self._config.initial_velocities, dtype=np.float64
            )
            if velocities.shape != (n, 3):
                raise ValueError(
                    f"initial_velocities must have shape ({n}, 3), "
                    f"got {velocities.shape}"
                )
        else:
            velocities = rng.uniform(-5.0, 5.0, size=(n, 3))
            # Ensure some upward velocity for fountain-like behaviour
            velocities[:, 1] = rng.uniform(2.0, 10.0, size=n)

        # Flatten to 1-D: [x1,y1,z1,vx1,vy1,vz1, x2,y2,z2,vx2,vy2,vz2, ...]
        state = np.zeros(6 * n, dtype=np.float64)
        for i in range(n):
            state[6 * i : 6 * i + 3] = positions[i]
            state[6 * i + 3 : 6 * i + 6] = velocities[i]

        return state

    def derivatives(self, state: State, t: float) -> State:
        """Compute time derivatives for all objects under gravity.

        For each object, acceleration is ``[0, -g, 0]`` (constant downward
        gravity). Inactive objects (removed) have zero derivatives.

        Parameters
        ----------
        state : State
            Current state vector of shape ``(6 * n_objects,)``.
        t : float
            Current simulation time (unused for constant gravity).

        Returns
        -------
        State
            Time derivative array: ``[vx1, vy1, vz1, 0, -g, 0, ...]``.
        """
        n = self._config.n_objects
        g = self._config.g
        deriv = np.zeros_like(state)

        for i in range(n):
            if not self._active_mask[i]:
                continue
            base = 6 * i
            # dx/dt = v
            deriv[base] = state[base + 3]      # dx/dt = vx
            deriv[base + 1] = state[base + 4]  # dy/dt = vy
            deriv[base + 2] = state[base + 5]  # dz/dt = vz
            # dv/dt = a = [0, -g, 0]
            deriv[base + 3] = 0.0              # dvx/dt = 0
            deriv[base + 4] = -g               # dvy/dt = -g
            deriv[base + 5] = 0.0              # dvz/dt = 0

        return deriv

    def step(self, dt: float | None = None) -> State:
        """Advance the simulation by one time step with bounce and removal.

        After the base integrator step, this method:

        1. Checks for floor collisions (y < boundary_y) and applies bounce
           by reversing vy and multiplying by the coefficient of restitution.
        2. Clamps the object position to be at or above the floor.
        3. Removes objects that have exited the boundary extent in x or z.

        Parameters
        ----------
        dt : float | None
            Time step size. If ``None``, uses the default from config.

        Returns
        -------
        State
            The new state vector after advancing and applying constraints.
        """
        # Perform the integration step
        result = super().step(dt)

        n = self._config.n_objects
        boundary_y = self._config.boundary_y
        restitution = self._config.restitution
        extent = self._config.extent

        for i in range(n):
            if not self._active_mask[i]:
                continue

            base = 6 * i
            x = self._state[base]
            y = self._state[base + 1]
            z = self._state[base + 2]

            # Check floor collision
            if y < boundary_y:
                # Clamp position to floor
                self._state[base + 1] = boundary_y
                # Reverse and attenuate vertical velocity
                self._state[base + 4] = (
                    -self._state[base + 4] * restitution
                )

            # Check extent removal (x/z beyond boundary)
            if abs(x) > extent or abs(z) > extent:
                self._active_mask[i] = False
                # Zero out the object's state
                self._state[base : base + 6] = 0.0

        return self._state

    def active_objects(self) -> int:
        """Return the number of objects still within simulation bounds.

        Returns
        -------
        int
            Count of active (non-removed) objects.
        """
        return int(np.sum(self._active_mask))


def create_fountain_config(n_objects: int = 50) -> GravityConfig:
    """Create a pre-configured GravityConfig for fountain mode.

    Generates a configuration suitable for a fountain simulation where
    objects are launched upward from near the origin and bounce off the
    floor.

    Parameters
    ----------
    n_objects : int
        Number of objects in the fountain. Default is 50.

    Returns
    -------
    GravityConfig
        Configuration with reasonable defaults for a fountain simulation.

    Examples
    --------
    >>> config = create_fountain_config(100)
    >>> config.n_objects
    100
    >>> config.restitution
    0.7
    """
    return GravityConfig(
        dt=0.01,
        integrator="rk4",
        g=9.8,
        restitution=0.7,
        boundary_y=0.0,
        extent=50.0,
        n_objects=n_objects,
    )
