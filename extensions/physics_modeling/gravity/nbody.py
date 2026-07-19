"""N-Body gravitational simulation.

This module implements the classical N-body gravitational problem where
N point masses interact via Newtonian gravity. A softening parameter
prevents singularities at close approaches.

Classes
-------
NBodyConfig
    Configuration dataclass holding gravitational constant, softening, and
    integrator choice.
NBodySimulation
    Simulation subclass computing pairwise gravitational forces.

Examples
--------
>>> from physics_modeling.gravity.nbody import NBodyConfig, NBodySimulation
>>> import numpy as np
>>> masses = np.array([1e10, 1e10, 1.0])
>>> positions = np.array([
...     [-0.5, 0.0, 0.0],
...     [ 0.5, 0.0, 0.0],
...     [ 0.0, 1.0, 0.0],
... ])
>>> velocities = np.array([
...     [ 0.0, -0.5, 0.0],
...     [ 0.0,  0.5, 0.0],
...     [ 0.5,  0.0, 0.0],
... ])
>>> config = NBodyConfig(G=1.0, softening=0.01)
>>> sim = NBodySimulation(config, masses, positions, velocities)
>>> sim.state.shape
(18,)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from physics_modeling.core.simulation import Simulation, SimulationConfig

__all__ = ["NBodyConfig", "NBodySimulation"]


@dataclass
class NBodyConfig(SimulationConfig):
    """Configuration for the N-body gravitational simulation.

    Parameters
    ----------
    G : float
        Gravitational constant. Use 6.674e-11 for SI or 1.0 for
        normalized units.
    softening : float
        Softening length to prevent force singularities at small
        separations. The force denominator becomes
        ``(|r|² + softening²)^(3/2)`` instead of ``|r|³``.
    integrator : str
        Integrator name. Default is ``"verlet"`` (symplectic) which
        provides better long-term energy conservation for orbital
        dynamics.
    dt : float
        Time step size (inherited from SimulationConfig).
    """

    G: float = 6.674e-11
    softening: float = 1e-4
    integrator: str = "verlet"


class NBodySimulation(Simulation):
    """N-body gravitational simulation with pairwise force computation.

    State vector layout: ``[x1,y1,z1,...,xN,yN,zN, vx1,vy1,vz1,...,vxN,vyN,vzN]``
    — all positions followed by all velocities, flattened.

    The acceleration on body *i* is computed as:

        a_i = sum_{j≠i} G * m_j * (r_j - r_i) / (|r_j - r_i|² + ε²)^(3/2)

    Parameters
    ----------
    config : NBodyConfig
        Configuration with G, softening, and integrator choice.
    masses : NDArray[np.float64]
        Array of shape ``(N,)`` containing the mass of each body.
    positions : NDArray[np.float64]
        Array of shape ``(N, 3)`` containing initial [x, y, z] positions.
    velocities : NDArray[np.float64]
        Array of shape ``(N, 3)`` containing initial [vx, vy, vz] velocities.

    Raises
    ------
    ValueError
        If array shapes are inconsistent or masses are non-positive.

    Examples
    --------
    >>> import numpy as np
    >>> masses = np.array([1.0, 1.0])
    >>> pos = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    >>> vel = np.array([[0.0, 0.5, 0.0], [0.0, -0.5, 0.0]])
    >>> sim = NBodySimulation(NBodyConfig(G=1.0, softening=0.01), masses, pos, vel)
    >>> sim.n_bodies
    2
    """

    def __init__(
        self,
        config: NBodyConfig,
        masses: NDArray[np.float64],
        positions: NDArray[np.float64],
        velocities: NDArray[np.float64],
    ) -> None:
        self._validate_inputs(masses, positions, velocities)
        self._config = config
        self._masses = np.asarray(masses, dtype=np.float64)
        self._initial_positions = np.asarray(positions, dtype=np.float64)
        self._initial_velocities = np.asarray(velocities, dtype=np.float64)
        self._n_bodies = len(masses)
        super().__init__(config)

    @staticmethod
    def _validate_inputs(
        masses: NDArray[np.float64],
        positions: NDArray[np.float64],
        velocities: NDArray[np.float64],
    ) -> None:
        """Validate input arrays for consistency.

        Parameters
        ----------
        masses : NDArray[np.float64]
            Body masses.
        positions : NDArray[np.float64]
            Initial positions.
        velocities : NDArray[np.float64]
            Initial velocities.

        Raises
        ------
        ValueError
            If shapes are inconsistent or masses are non-positive.
        """
        masses = np.asarray(masses)
        positions = np.asarray(positions)
        velocities = np.asarray(velocities)

        if masses.ndim != 1:
            raise ValueError(f"masses must be 1-D, got shape {masses.shape}")
        n = len(masses)
        if positions.shape != (n, 3):
            raise ValueError(
                f"positions must have shape ({n}, 3), got {positions.shape}"
            )
        if velocities.shape != (n, 3):
            raise ValueError(
                f"velocities must have shape ({n}, 3), got {velocities.shape}"
            )
        if np.any(masses <= 0):
            raise ValueError("All masses must be strictly positive")

    @property
    def n_bodies(self) -> int:
        """Number of gravitational bodies in the simulation."""
        return self._n_bodies

    @property
    def masses(self) -> NDArray[np.float64]:
        """Mass array of shape ``(N,)``."""
        return self._masses

    @property
    def config(self) -> NBodyConfig:
        """The simulation configuration."""
        return self._config

    def initial_state(self) -> NDArray[np.float64]:
        """Return the initial state vector [positions..., velocities...].

        Returns
        -------
        NDArray[np.float64]
            Flattened array of shape ``(6*N,)`` with all positions
            followed by all velocities.
        """
        return np.concatenate([
            self._initial_positions.ravel(),
            self._initial_velocities.ravel(),
        ])

    def derivatives(
        self, state: NDArray[np.float64], t: float
    ) -> NDArray[np.float64]:
        """Compute time derivatives: velocities and accelerations.

        Parameters
        ----------
        state : NDArray[np.float64]
            Current state ``[x1,y1,z1,...,xN,yN,zN, vx1,...,vzN]``.
        t : float
            Current simulation time (unused, system is autonomous).

        Returns
        -------
        NDArray[np.float64]
            Derivatives ``[vx1,vy1,vz1,..., ax1,ay1,az1,...]``.
        """
        n = self._n_bodies
        positions = state[: 3 * n].reshape(n, 3)
        velocities = state[3 * n :].reshape(n, 3)

        G = self._config.G
        eps2 = self._config.softening ** 2
        accelerations = np.zeros((n, 3), dtype=np.float64)

        # Compute pairwise gravitational forces
        for i in range(n):
            for j in range(i + 1, n):
                r_ij = positions[j] - positions[i]
                dist_sq = np.dot(r_ij, r_ij) + eps2
                inv_dist_cubed = dist_sq ** (-1.5)

                # Force on i due to j
                force_mag_on_i = G * self._masses[j] * inv_dist_cubed
                accelerations[i] += force_mag_on_i * r_ij

                # Force on j due to i (Newton's third law)
                force_mag_on_j = G * self._masses[i] * inv_dist_cubed
                accelerations[j] -= force_mag_on_j * r_ij

        return np.concatenate([velocities.ravel(), accelerations.ravel()])

    def get_positions(self, state: NDArray[np.float64] | None = None) -> NDArray[np.float64]:
        """Extract position array from state vector.

        Parameters
        ----------
        state : NDArray[np.float64] | None
            State to extract from. If ``None``, uses current state.

        Returns
        -------
        NDArray[np.float64]
            Array of shape ``(N, 3)`` with body positions.
        """
        if state is None:
            state = self._state
        return state[: 3 * self._n_bodies].reshape(self._n_bodies, 3)

    def get_velocities(self, state: NDArray[np.float64] | None = None) -> NDArray[np.float64]:
        """Extract velocity array from state vector.

        Parameters
        ----------
        state : NDArray[np.float64] | None
            State to extract from. If ``None``, uses current state.

        Returns
        -------
        NDArray[np.float64]
            Array of shape ``(N, 3)`` with body velocities.
        """
        if state is None:
            state = self._state
        return state[3 * self._n_bodies :].reshape(self._n_bodies, 3)

    @property
    def total_energy(self) -> float:
        """Compute total energy (kinetic + potential) of the system.

        Returns
        -------
        float
            Total mechanical energy of the N-body system.
        """
        positions = self.get_positions()
        velocities = self.get_velocities()
        G = self._config.G
        eps2 = self._config.softening ** 2

        # Kinetic energy
        ke = 0.0
        for i in range(self._n_bodies):
            ke += 0.5 * self._masses[i] * np.dot(velocities[i], velocities[i])

        # Potential energy
        pe = 0.0
        for i in range(self._n_bodies):
            for j in range(i + 1, self._n_bodies):
                r_ij = positions[j] - positions[i]
                dist = np.sqrt(np.dot(r_ij, r_ij) + eps2)
                pe -= G * self._masses[i] * self._masses[j] / dist

        return float(ke + pe)
