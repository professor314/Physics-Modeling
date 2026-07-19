"""Elastic collision simulation for spherical objects in 2D and 3D.

This module models elastic collisions between spherical objects, detecting
overlaps and resolving them using the standard elastic collision formula
that preserves both momentum and kinetic energy.

Classes
-------
CollisionConfig
    Configuration dataclass for the elastic collision simulation.
CollisionSimulation
    Simulation of elastic collisions between spherical objects.

Functions
---------
detect_collisions
    Find all overlapping pairs of spheres in the current state.
resolve_collision
    Apply the elastic collision formula to a pair of colliding spheres.

Examples
--------
>>> from physics_modeling.collisions.elastic import (
...     CollisionSimulation, CollisionConfig
... )
>>> config = CollisionConfig(n_objects=2, dimensions=3)
>>> sim = CollisionSimulation(config)
>>> sim.step()  # advance one time step
array([...])
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal

import numpy as np

from physics_modeling.core.simulation import Simulation, SimulationConfig

if TYPE_CHECKING:
    from numpy.typing import NDArray

    from physics_modeling.core.protocols import State

__all__ = [
    "CollisionConfig",
    "CollisionSimulation",
    "detect_collisions",
    "resolve_collision",
]


@dataclass
class CollisionConfig(SimulationConfig):
    """Configuration for the elastic collision simulation.

    Parameters
    ----------
    dt : float
        Time step size for integration (seconds).
    integrator : str
        Numerical integrator name (``"euler"``, ``"rk4"``, or ``"verlet"``).
    dimensions : Literal[2, 3]
        Number of spatial dimensions for the simulation. Either 2 or 3.
    n_objects : int
        Number of spherical objects to simulate. Must be >= 2.
    radii : NDArray | None
        Array of sphere radii with shape ``(n_objects,)``. If ``None``,
        defaults to all radii of 1.0.
    masses : NDArray | None
        Array of sphere masses with shape ``(n_objects,)``. If ``None``,
        defaults to all masses of 1.0.
    initial_positions : NDArray | None
        Optional initial positions array of shape ``(n_objects, 6)`` where
        each row is ``[x, y, z, vx, vy, vz]`` (z components are zero for 2D).
        If ``None``, positions are randomly generated.
    box_size : float
        Size of the bounding box for initial random placement. Objects are
        placed within ``[-box_size/2, box_size/2]`` in each dimension.

    Raises
    ------
    ValueError
        If parameters fail validation constraints.
    """

    dimensions: Literal[2, 3] = 3
    n_objects: int = 2
    radii: np.ndarray | None = field(default=None, repr=False)
    masses: np.ndarray | None = field(default=None, repr=False)
    initial_positions: np.ndarray | None = field(default=None, repr=False)
    box_size: float = 20.0

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.dimensions not in (2, 3):
            raise ValueError(
                f"dimensions must be 2 or 3, got {self.dimensions}"
            )
        if self.n_objects < 2:
            raise ValueError(
                f"n_objects must be >= 2, got {self.n_objects}"
            )
        if self.radii is None:
            self.radii = np.ones(self.n_objects, dtype=np.float64)
        else:
            self.radii = np.asarray(self.radii, dtype=np.float64)
            if self.radii.shape != (self.n_objects,):
                raise ValueError(
                    f"radii must have shape ({self.n_objects},), "
                    f"got {self.radii.shape}"
                )
        if self.masses is None:
            self.masses = np.ones(self.n_objects, dtype=np.float64)
        else:
            self.masses = np.asarray(self.masses, dtype=np.float64)
            if self.masses.shape != (self.n_objects,):
                raise ValueError(
                    f"masses must have shape ({self.n_objects},), "
                    f"got {self.masses.shape}"
                )
        if self.box_size <= 0:
            raise ValueError(
                f"box_size must be > 0, got {self.box_size}"
            )


def detect_collisions(
    state: State,
    radii: NDArray[np.float64],
    dimensions: int = 3,
) -> list[tuple[int, int]]:
    """Find all overlapping pairs of spheres in the current state.

    Checks whether the Euclidean distance between the centers of any two
    spheres is less than the sum of their radii.

    Parameters
    ----------
    state : State
        1-D state vector of shape ``(n_objects * 6,)`` laid out as
        ``[x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, ...]``.
    radii : NDArray[np.float64]
        Array of sphere radii with shape ``(n_objects,)``.
    dimensions : int
        Number of spatial dimensions (2 or 3). When 2, the z component
        is ignored for distance calculations.

    Returns
    -------
    list[tuple[int, int]]
        List of ``(i, j)`` index pairs where ``i < j`` for all overlapping
        sphere pairs.

    Examples
    --------
    >>> import numpy as np
    >>> # Two objects at distance 1.5 with radii 1.0 each -> collision
    >>> state = np.array([0, 0, 0, 0, 0, 0, 1.5, 0, 0, 0, 0, 0], dtype=np.float64)
    >>> radii = np.array([1.0, 1.0])
    >>> detect_collisions(state, radii, dimensions=3)
    [(0, 1)]
    """
    n_objects = len(radii)
    collisions: list[tuple[int, int]] = []

    for i in range(n_objects):
        for j in range(i + 1, n_objects):
            # Extract positions
            pos_i = state[6 * i : 6 * i + 3].copy()
            pos_j = state[6 * j : 6 * j + 3].copy()

            if dimensions == 2:
                pos_i[2] = 0.0
                pos_j[2] = 0.0

            diff = pos_i - pos_j
            dist = np.sqrt(np.dot(diff, diff))

            if dist < radii[i] + radii[j]:
                collisions.append((i, j))

    return collisions


def resolve_collision(
    state: State,
    i: int,
    j: int,
    masses: NDArray[np.float64],
    radii: NDArray[np.float64],
    dimensions: int = 3,
) -> State:
    """Apply the elastic collision formula to a pair of colliding spheres.

    Uses the standard elastic collision formula for two spheres:

    .. math::

        v_1' = v_1 - \\frac{2 m_2}{m_1 + m_2}
               \\frac{(v_1 - v_2) \\cdot (x_1 - x_2)}{|x_1 - x_2|^2}
               (x_1 - x_2)

        v_2' = v_2 - \\frac{2 m_1}{m_1 + m_2}
               \\frac{(v_2 - v_1) \\cdot (x_2 - x_1)}{|x_2 - x_1|^2}
               (x_2 - x_1)

    Additionally separates the spheres so they no longer overlap by moving
    each sphere along the collision normal proportional to their inverse mass.

    Parameters
    ----------
    state : State
        1-D state vector of shape ``(n_objects * 6,)`` laid out as
        ``[x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, ...]``.
    i : int
        Index of the first colliding sphere.
    j : int
        Index of the second colliding sphere.
    masses : NDArray[np.float64]
        Array of sphere masses with shape ``(n_objects,)``.
    radii : NDArray[np.float64]
        Array of sphere radii with shape ``(n_objects,)``.
    dimensions : int
        Number of spatial dimensions (2 or 3). When 2, the z component
        is zeroed in the collision normal calculation.

    Returns
    -------
    State
        Updated state vector with post-collision velocities and separated
        positions.

    Examples
    --------
    >>> import numpy as np
    >>> # Head-on collision between two equal-mass spheres
    >>> state = np.array([0, 0, 0, 1, 0, 0, 1.5, 0, 0, -1, 0, 0],
    ...                  dtype=np.float64)
    >>> masses = np.array([1.0, 1.0])
    >>> radii = np.array([1.0, 1.0])
    >>> new_state = resolve_collision(state, 0, 1, masses, radii)
    >>> new_state[3]  # v1x after collision
    -1.0
    """
    new_state = state.copy()

    # Extract positions and velocities
    x1 = new_state[6 * i : 6 * i + 3].copy()
    v1 = new_state[6 * i + 3 : 6 * i + 6].copy()
    x2 = new_state[6 * j : 6 * j + 3].copy()
    v2 = new_state[6 * j + 3 : 6 * j + 6].copy()

    if dimensions == 2:
        x1[2] = 0.0
        x2[2] = 0.0
        v1[2] = 0.0
        v2[2] = 0.0

    m1 = masses[i]
    m2 = masses[j]

    # Collision normal vector
    dx = x1 - x2
    dist_sq = np.dot(dx, dx)

    # Avoid division by zero for exactly coincident spheres
    if dist_sq < 1e-12:
        # Separate along a default axis
        dx = np.array([1.0, 0.0, 0.0], dtype=np.float64)
        dist_sq = 1.0

    # Apply elastic collision formula
    dv = v1 - v2
    dot_dv_dx = np.dot(dv, dx)

    # Only resolve if objects are approaching each other.
    # Objects approach when dot(v1-v2, x1-x2) < 0 (relative velocity
    # has a component toward the other object).
    if dot_dv_dx >= 0:
        # Objects are separating or sliding, no resolution needed
        return new_state

    v1_new = v1 - (2.0 * m2 / (m1 + m2)) * (dot_dv_dx / dist_sq) * dx
    v2_new = v2 - (2.0 * m1 / (m1 + m2)) * (dot_dv_dx / dist_sq) * (-dx)

    # Separate overlapping spheres along collision normal
    dist = np.sqrt(dist_sq)
    overlap = (radii[i] + radii[j]) - dist
    if overlap > 0:
        normal = dx / dist
        # Move each sphere proportional to inverse mass
        total_inv_mass = 1.0 / m1 + 1.0 / m2
        move_i = (overlap * (1.0 / m1) / total_inv_mass) * normal
        move_j = (overlap * (1.0 / m2) / total_inv_mass) * normal
        x1_new = x1 + move_i
        x2_new = x2 - move_j
        new_state[6 * i : 6 * i + 3] = x1_new
        new_state[6 * j : 6 * j + 3] = x2_new

    # Update velocities
    new_state[6 * i + 3 : 6 * i + 6] = v1_new
    new_state[6 * j + 3 : 6 * j + 6] = v2_new

    return new_state


class CollisionSimulation(Simulation):
    """Simulation of elastic collisions between spherical objects.

    The state vector is a 1-D array of length ``6 * n_objects``, laid out as::

        [x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, ...]

    Each object has 3 position components followed by 3 velocity components.
    Between collisions, objects move at constant velocity (zero acceleration).
    After each integration step, collisions are detected and resolved using
    the elastic collision formula, preserving both momentum and kinetic energy.

    Parameters
    ----------
    config : CollisionConfig
        Configuration specifying object count, radii, masses, and dimensions.

    Attributes
    ----------
    _config : CollisionConfig
        Stored configuration for physics parameters.

    Examples
    --------
    >>> config = CollisionConfig(n_objects=3, dimensions=3)
    >>> sim = CollisionSimulation(config)
    >>> sim.step()
    array([...])
    """

    def __init__(self, config: CollisionConfig) -> None:
        self._config: CollisionConfig = config
        super().__init__(config)

    def initial_state(self) -> State:
        """Return the initial state vector for all objects.

        If ``initial_positions`` is provided in the config, that is used
        directly. Otherwise, objects are placed at random non-overlapping
        positions with random velocities.

        Returns
        -------
        State
            1-D float64 array of shape ``(6 * n_objects,)``.
        """
        n = self._config.n_objects
        dims = self._config.dimensions

        if self._config.initial_positions is not None:
            initial = np.asarray(
                self._config.initial_positions, dtype=np.float64
            )
            if initial.shape != (n, 6):
                raise ValueError(
                    f"initial_positions must have shape ({n}, 6), "
                    f"got {initial.shape}"
                )
            return initial.flatten()

        rng = np.random.default_rng()
        half_box = self._config.box_size / 2.0
        assert self._config.radii is not None  # guaranteed by __post_init__
        max_radius = float(np.max(self._config.radii))

        state = np.zeros(6 * n, dtype=np.float64)

        # Place objects ensuring no overlap
        positions: list[NDArray[np.float64]] = []
        for i in range(n):
            max_attempts = 1000
            for _ in range(max_attempts):
                pos = rng.uniform(
                    -half_box + max_radius,
                    half_box - max_radius,
                    size=3,
                )
                if dims == 2:
                    pos[2] = 0.0

                # Check for overlap with existing objects
                valid = True
                for existing_pos_idx, existing_pos in enumerate(positions):
                    diff = pos - existing_pos
                    dist = np.sqrt(np.dot(diff, diff))
                    min_dist = (
                        self._config.radii[i]
                        + self._config.radii[existing_pos_idx]
                    )
                    if dist < min_dist * 1.1:  # 10% margin
                        valid = False
                        break

                if valid:
                    positions.append(pos)
                    break
            else:
                # Fallback: place at grid position
                pos = np.array(
                    [i * 3.0 * max_radius, 0.0, 0.0], dtype=np.float64
                )
                if dims == 2:
                    pos[2] = 0.0
                positions.append(pos)

        # Assign positions and random velocities
        for i in range(n):
            state[6 * i : 6 * i + 3] = positions[i]
            vel = rng.uniform(-5.0, 5.0, size=3)
            if dims == 2:
                vel[2] = 0.0
            state[6 * i + 3 : 6 * i + 6] = vel

        return state

    def derivatives(self, state: State, t: float) -> State:
        """Compute time derivatives — constant velocity (zero acceleration).

        Between collisions, objects move in straight lines at constant
        velocity. The derivative of position is velocity, and the derivative
        of velocity is zero.

        Parameters
        ----------
        state : State
            Current state vector of shape ``(6 * n_objects,)``.
        t : float
            Current simulation time (unused for constant velocity).

        Returns
        -------
        State
            Time derivative array: ``[vx1, vy1, vz1, 0, 0, 0, ...]``.
        """
        n = self._config.n_objects
        deriv = np.zeros_like(state)

        for i in range(n):
            base = 6 * i
            # dx/dt = v
            deriv[base] = state[base + 3]      # dx/dt = vx
            deriv[base + 1] = state[base + 4]  # dy/dt = vy
            deriv[base + 2] = state[base + 5]  # dz/dt = vz
            # dv/dt = 0 (no forces between collisions)

        return deriv

    def step(self, dt: float | None = None) -> State:
        """Advance the simulation by one time step with collision resolution.

        After the base integrator step, this method detects overlapping
        sphere pairs and resolves each collision using the elastic collision
        formula. Multiple collision pairs are resolved iteratively.

        Parameters
        ----------
        dt : float | None
            Time step size. If ``None``, uses the default from config.

        Returns
        -------
        State
            The new state vector after advancing and resolving collisions.
        """
        # Perform the integration step
        super().step(dt)

        assert self._config.radii is not None
        assert self._config.masses is not None

        # Detect and resolve collisions iteratively
        max_iterations = 10
        for _ in range(max_iterations):
            collisions = detect_collisions(
                self._state,
                self._config.radii,
                self._config.dimensions,
            )
            if not collisions:
                break
            for i, j in collisions:
                self._state = resolve_collision(
                    self._state,
                    i,
                    j,
                    self._config.masses,
                    self._config.radii,
                    self._config.dimensions,
                )

        return self._state
