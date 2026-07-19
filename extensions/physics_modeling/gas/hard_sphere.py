"""Hard sphere ideal gas simulation.

This module models N hard-sphere particles in a bounded rectangular container.
Particles travel ballistically between elastic collisions with each other and
with the container walls. Thermodynamic quantities (temperature, kinetic energy,
speed distribution) are computed from the instantaneous particle velocities.

Classes
-------
GasConfig
    Configuration dataclass for the hard sphere gas simulation.
HardSphereGas
    Simulation of an ideal gas of hard spheres with elastic collisions.

Notes
-----
Collision detection uses an O(N²) all-pairs check, which is acceptable for
N ≈ 200 particles. Event-driven collision detection could be implemented as
a future optimisation for larger systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from physics_modeling.core.simulation import Simulation, SimulationConfig

if TYPE_CHECKING:
    from numpy.typing import NDArray

__all__ = ["GasConfig", "HardSphereGas"]

# Boltzmann constant in SI units (J/K)
K_BOLTZMANN: float = 1.380649e-23


@dataclass
class GasConfig(SimulationConfig):
    """Configuration for the hard sphere gas simulation.

    Parameters
    ----------
    dt : float
        Time step for ballistic advancement (seconds).
    integrator : str
        Integrator name (not used directly — step is overridden).
    n_particles : int
        Number of particles in the gas.
    container_size : tuple[float, float, float]
        Dimensions (Lx, Ly, Lz) of the rectangular container.
    particle_radius : float
        Radius of each hard sphere particle.
    particle_mass : float
        Mass of each particle (uniform).
    temperature : float
        Initial temperature in Kelvin for Maxwell-Boltzmann speed sampling.
    """

    n_particles: int = 200
    container_size: tuple[float, float, float] = (10.0, 10.0, 10.0)
    particle_radius: float = 0.1
    particle_mass: float = 1.0
    temperature: float = 300.0


class HardSphereGas(Simulation):
    """Simulation of an ideal gas of N hard spheres in a box.

    Particles undergo free ballistic flight punctuated by elastic collisions
    with other particles and specular reflections off the container walls.

    The state vector is a flattened array of shape ``(N*6,)`` where each
    particle contributes ``[x, y, z, vx, vy, vz]``.

    Parameters
    ----------
    config : GasConfig
        Configuration specifying particle count, container geometry, and
        initial temperature.

    Attributes
    ----------
    config : GasConfig
        Stored configuration.
    _n : int
        Number of particles.
    _radius : float
        Particle radius.
    _mass : float
        Particle mass.
    _box : NDArray
        Container dimensions as a (3,) array.

    Examples
    --------
    >>> cfg = GasConfig(n_particles=50, temperature=300.0, dt=0.001)
    >>> gas = HardSphereGas(cfg)
    >>> gas.state.shape
    (300,)
    >>> _ = gas.step()
    >>> gas.kinetic_energy > 0
    True
    """

    def __init__(self, config: GasConfig) -> None:
        self.config: GasConfig = config
        self._n: int = config.n_particles
        self._radius: float = config.particle_radius
        self._mass: float = config.particle_mass
        self._box: NDArray = np.array(config.container_size, dtype=np.float64)
        super().__init__(config)

    def initial_state(self) -> NDArray:
        """Generate initial positions and velocities for all particles.

        Positions are distributed randomly within the container (with a
        margin of one particle radius from walls). Velocities are sampled
        from a Maxwell-Boltzmann distribution at the configured temperature.

        Returns
        -------
        NDArray
            Flattened state vector of shape ``(N*6,)`` with layout
            ``[x0, y0, z0, vx0, vy0, vz0, x1, y1, z1, ...]``.
        """
        rng = np.random.default_rng()

        # Positions: uniform in [radius, L - radius] for each dimension
        positions = np.zeros((self._n, 3), dtype=np.float64)
        for dim in range(3):
            lo = self._radius
            hi = self._box[dim] - self._radius
            positions[:, dim] = rng.uniform(lo, hi, size=self._n)

        # Velocities: Maxwell-Boltzmann → each component is Gaussian
        # with sigma = sqrt(k_B * T / m)
        sigma = np.sqrt(K_BOLTZMANN * self.config.temperature / self._mass)
        velocities = rng.normal(0.0, sigma, size=(self._n, 3))

        # Combine into (N, 6) then flatten
        state = np.column_stack([positions, velocities])
        return state.ravel()

    def derivatives(self, state: NDArray, t: float) -> NDArray:
        """Compute time derivatives of the state vector.

        For hard-sphere gas between collisions, particles experience no
        forces — they travel in straight lines. The derivatives are:
        dx/dt = vx, dy/dt = vy, dz/dt = vz, dvx/dt = 0, dvy/dt = 0, dvz/dt = 0.

        Parameters
        ----------
        state : NDArray
            Current flattened state vector of shape ``(N*6,)``.
        t : float
            Current simulation time (unused for this system).

        Returns
        -------
        NDArray
            Time derivatives: velocities in position slots, zeros in
            velocity slots.
        """
        particles = state.reshape(-1, 6)
        derivs = np.zeros_like(particles)
        derivs[:, :3] = particles[:, 3:]  # dx/dt = v
        # dv/dt = 0 (free flight)
        return derivs.ravel()

    def step(self, dt: float | None = None) -> NDArray:
        """Advance the simulation by one time step.

        Override the base class to implement:
        1. Ballistic advancement of all particles.
        2. Wall collision detection and reflection.
        3. Particle-particle elastic collision detection and resolution.

        Parameters
        ----------
        dt : float | None
            Time step size. If ``None``, uses the configured default.

        Returns
        -------
        NDArray
            The new state vector after advancement and collision resolution.
        """
        dt = dt if dt is not None else self._dt

        # 1. Ballistic advance
        particles = self._state.reshape(-1, 6).copy()
        particles[:, :3] += particles[:, 3:] * dt

        # 2. Wall collisions (reflect off boundaries)
        particles = self._resolve_wall_collisions(particles)

        # 3. Particle-particle collisions (O(N²) all-pairs)
        particles = self._resolve_particle_collisions(particles)

        self._state = particles.ravel()
        self._t += dt
        return self._state

    def _resolve_wall_collisions(self, particles: NDArray) -> NDArray:
        """Detect and resolve wall collisions for all particles.

        When a particle's position exceeds a container boundary (accounting
        for its radius), the corresponding velocity component is reflected
        and the position is clamped to the boundary.

        Parameters
        ----------
        particles : NDArray
            Array of shape ``(N, 6)`` with positions and velocities.

        Returns
        -------
        NDArray
            Updated particles array with wall reflections applied.
        """
        for dim in range(3):
            lo = self._radius
            hi = self._box[dim] - self._radius

            # Particles that hit the lower wall
            mask_lo = particles[:, dim] < lo
            particles[mask_lo, dim] = lo + (lo - particles[mask_lo, dim])
            particles[mask_lo, dim + 3] = np.abs(particles[mask_lo, dim + 3])

            # Particles that hit the upper wall
            mask_hi = particles[:, dim] > hi
            particles[mask_hi, dim] = hi - (particles[mask_hi, dim] - hi)
            particles[mask_hi, dim + 3] = -np.abs(particles[mask_hi, dim + 3])

        return particles

    def _resolve_particle_collisions(self, particles: NDArray) -> NDArray:
        """Detect and resolve elastic particle-particle collisions.

        Uses an O(N²) all-pairs distance check. When two particles overlap
        (centre distance < 2 * radius), an elastic collision is resolved
        using the standard formula for equal or unequal masses.

        Parameters
        ----------
        particles : NDArray
            Array of shape ``(N, 6)`` with positions and velocities.

        Returns
        -------
        NDArray
            Updated particles array with collision velocities resolved.
        """
        positions = particles[:, :3]
        velocities = particles[:, 3:]
        n = self._n
        min_dist = 2.0 * self._radius

        # Compute pairwise distances (vectorised upper triangle)
        for i in range(n):
            # Vectorised comparison of particle i against all j > i
            if i >= n - 1:
                break
            dx = positions[i + 1:] - positions[i]
            dist_sq = np.sum(dx * dx, axis=1)
            min_dist_sq = min_dist * min_dist

            # Find colliding pairs
            colliding = np.where(dist_sq < min_dist_sq)[0]

            for idx in colliding:
                j = i + 1 + idx
                # Relative position and velocity
                r = positions[i] - positions[j]
                dist = np.sqrt(np.dot(r, r))

                if dist < 1e-12:
                    continue  # Skip degenerate case

                r_hat = r / dist
                v_rel = velocities[i] - velocities[j]
                v_along = np.dot(v_rel, r_hat)

                # Only resolve if particles are approaching
                if v_along > 0:
                    continue

                # Equal mass elastic collision: exchange velocity components
                # along the line of centres
                # General formula for arbitrary masses:
                m1 = self._mass
                m2 = self._mass
                factor1 = (2.0 * m2) / (m1 + m2)
                factor2 = (2.0 * m1) / (m1 + m2)

                velocities[i] -= factor1 * v_along * r_hat
                velocities[j] += factor2 * v_along * r_hat

                # Separate overlapping particles
                overlap = min_dist - dist
                if overlap > 0:
                    separation = (overlap / 2.0 + 1e-6) * r_hat
                    positions[i] += separation
                    positions[j] -= separation

        particles[:, :3] = positions
        particles[:, 3:] = velocities
        return particles

    @property
    def temperature(self) -> float:
        """Compute the gas temperature from average kinetic energy.

        Uses the equipartition theorem: <KE> = (3/2) * k_B * T
        for 3 translational degrees of freedom per particle.

        Returns
        -------
        float
            Temperature in Kelvin.
        """
        ke = self.kinetic_energy
        # <KE per particle> = (3/2) * k_B * T
        # T = (2/3) * <KE per particle> / k_B
        ke_per_particle = ke / self._n
        return (2.0 / 3.0) * ke_per_particle / K_BOLTZMANN

    @property
    def kinetic_energy(self) -> float:
        """Compute the total kinetic energy of all particles.

        Returns
        -------
        float
            Total kinetic energy: sum of (1/2) * m * |v|² for all particles.
        """
        particles = self._state.reshape(-1, 6)
        velocities = particles[:, 3:]
        speed_sq = np.sum(velocities * velocities, axis=1)
        return 0.5 * self._mass * float(np.sum(speed_sq))

    @property
    def speed_distribution(self) -> tuple[NDArray, NDArray]:
        """Compute a histogram of particle speeds.

        Parameters for the histogram (50 bins) are determined automatically
        from the current speed range.

        Returns
        -------
        tuple[NDArray, NDArray]
            A tuple of (bin_centres, counts) where bin_centres has shape
            ``(n_bins,)`` and counts has shape ``(n_bins,)``.
        """
        return self.get_speed_distribution(n_bins=50)

    def get_speed_distribution(self, n_bins: int = 50) -> tuple[NDArray, NDArray]:
        """Compute a histogram of particle speeds with configurable bins.

        Parameters
        ----------
        n_bins : int
            Number of histogram bins.

        Returns
        -------
        tuple[NDArray, NDArray]
            A tuple of (bin_centres, counts) where bin_centres has shape
            ``(n_bins,)`` and counts has shape ``(n_bins,)``.
        """
        particles = self._state.reshape(-1, 6)
        velocities = particles[:, 3:]
        speeds = np.sqrt(np.sum(velocities * velocities, axis=1))

        counts, bin_edges = np.histogram(speeds, bins=n_bins)
        bin_centres = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        return bin_centres, counts.astype(np.float64)

    @property
    def positions(self) -> NDArray:
        """Particle positions as an (N, 3) array.

        Returns
        -------
        NDArray
            Positions of shape ``(N, 3)``.
        """
        return self._state.reshape(-1, 6)[:, :3].copy()

    @property
    def velocities(self) -> NDArray:
        """Particle velocities as an (N, 3) array.

        Returns
        -------
        NDArray
            Velocities of shape ``(N, 3)``.
        """
        return self._state.reshape(-1, 6)[:, 3:].copy()

    @property
    def speeds(self) -> NDArray:
        """Particle speed magnitudes as an (N,) array.

        Returns
        -------
        NDArray
            Speed magnitudes for each particle.
        """
        v = self.velocities
        return np.sqrt(np.sum(v * v, axis=1))
