"""N-Body Gravitational — 3D Animated Visualization.

A standalone runnable demo that visualizes the :class:`NBodySimulation`
in 3D using matplotlib. Features orbital trails with colored bodies,
starting with a binary star system plus test particles. Interactive
sliders control gravitational constant, star mass, and particle count.

Run directly::

    py -m physics_modeling.gravity.nbody_viz

Or call programmatically::

    from physics_modeling.gravity.nbody_viz import run_nbody_3d
    run_nbody_3d()
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers 3D projection

from physics_modeling.gravity.nbody import NBodyConfig, NBodySimulation

__all__ = ["run_nbody_3d"]


def _create_system(
    G: float = 1.0,
    star_mass: float = 5.0,
    n_particles: int = 3,
) -> tuple[NBodyConfig, np.ndarray, np.ndarray, np.ndarray]:
    """Create a binary star + N test particle initial configuration.

    Parameters
    ----------
    G : float
        Gravitational constant.
    star_mass : float
        Mass of each star in the binary pair.
    n_particles : int
        Number of test particles to add around the binary.

    Returns
    -------
    tuple
        ``(config, masses, positions, velocities)`` ready for
        NBodySimulation construction.
    """
    config = NBodyConfig(G=G, softening=0.01, integrator="verlet", dt=0.005)

    m_particle = 0.001
    n_total = 2 + n_particles

    masses = np.zeros(n_total, dtype=np.float64)
    masses[0] = star_mass
    masses[1] = star_mass
    for i in range(2, n_total):
        masses[i] = m_particle

    # Binary separation and orbital velocity
    separation = 1.0
    v_orbital = np.sqrt(G * star_mass / (2.0 * separation))

    positions = np.zeros((n_total, 3), dtype=np.float64)
    velocities = np.zeros((n_total, 3), dtype=np.float64)

    # Binary stars
    positions[0] = [-separation / 2, 0.0, 0.0]
    positions[1] = [separation / 2, 0.0, 0.0]
    velocities[0] = [0.0, -v_orbital, 0.0]
    velocities[1] = [0.0, v_orbital, 0.0]

    # Test particles at varying distances and angles
    rng = np.random.default_rng(42)
    for i in range(2, n_total):
        angle = rng.uniform(0, 2 * np.pi)
        radius = rng.uniform(2.0, 4.0)
        z_offset = rng.uniform(-0.5, 0.5)
        positions[i] = [radius * np.cos(angle), radius * np.sin(angle), z_offset]
        # Roughly circular velocity
        speed = np.sqrt(G * 2 * star_mass / radius) * rng.uniform(0.8, 1.2)
        velocities[i] = [-speed * np.sin(angle), speed * np.cos(angle), rng.uniform(-0.1, 0.1)]

    return config, masses, positions, velocities


def run_nbody_3d(
    config: NBodyConfig | None = None,
    masses: np.ndarray | None = None,
    positions: np.ndarray | None = None,
    velocities: np.ndarray | None = None,
) -> None:
    """Launch the interactive 3D N-body visualization.

    Creates a matplotlib 3D figure with FuncAnimation, drawing:
    - Colored spheres for each body (sized by mass)
    - Orbital trails showing each body's trajectory history

    Interactive sliders allow adjustment of:
    - G (gravitational constant)
    - Star mass (resets simulation)
    - Number of particles (resets simulation)

    If no arguments are provided, a binary star + test particle system
    is used as the default demonstration.

    Parameters
    ----------
    config : NBodyConfig | None
        Simulation configuration. If ``None``, uses binary star defaults.
    masses : ndarray | None
        Body masses of shape ``(N,)``.
    positions : ndarray | None
        Initial positions of shape ``(N, 3)``.
    velocities : ndarray | None
        Initial velocities of shape ``(N, 3)``.
    """
    # Initial parameters
    init_G = 1.0
    init_star_mass = 5.0
    init_n_particles = 3

    if config is None or masses is None or positions is None or velocities is None:
        config, masses, positions, velocities = _create_system(
            init_G, init_star_mass, init_n_particles
        )

    sim = NBodySimulation(config, masses, positions, velocities)
    n = sim.n_bodies

    # Trail storage
    trails: list[list[np.ndarray]] = [[] for _ in range(n)]
    max_trail: int = 300
    sub_steps: int = 8
    extent = float(np.max(np.abs(positions))) * 2.0

    # --- Figure setup ---
    fig = plt.figure(figsize=(10, 9))
    ax: Any = fig.add_subplot(111, projection="3d")

    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_zlim(-extent, extent)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("N-Body Gravitational Simulation")

    # Generate distinct colors
    cmap = plt.cm.Set1  # type: ignore[attr-defined]
    max_bodies = 20
    all_colors = [cmap(i / max(max_bodies, 1)) for i in range(max_bodies)]

    # --- Sliders ---
    fig.subplots_adjust(bottom=0.20)

    ax_G = fig.add_axes([0.2, 0.12, 0.6, 0.03])
    ax_mass = fig.add_axes([0.2, 0.07, 0.6, 0.03])
    ax_npart = fig.add_axes([0.2, 0.02, 0.6, 0.03])

    slider_G = Slider(ax_G, "G", 0.1, 5.0, valinit=init_G)
    slider_mass = Slider(ax_mass, "Star Mass", 1.0, 20.0, valinit=init_star_mass)
    slider_npart = Slider(ax_npart, "# Particles", 1, 15, valinit=init_n_particles, valstep=1, valfmt="%d")

    def _on_slider_change(_val: float) -> None:
        """Reset simulation when any slider changes."""
        nonlocal sim, n, trails, extent
        new_G = slider_G.val
        new_star_mass = slider_mass.val
        new_n_particles = int(slider_npart.val)

        new_config, new_masses, new_positions, new_velocities = _create_system(
            new_G, new_star_mass, new_n_particles
        )
        sim = NBodySimulation(new_config, new_masses, new_positions, new_velocities)
        n = sim.n_bodies
        trails = [[] for _ in range(n)]
        extent = float(np.max(np.abs(new_positions))) * 2.0

    slider_G.on_changed(_on_slider_change)
    slider_mass.on_changed(_on_slider_change)
    slider_npart.on_changed(_on_slider_change)

    # --- Animation callback ---
    def _animate(_frame: int) -> Any:
        # Advance simulation
        for _ in range(sub_steps):
            sim.step()

        pos = sim.get_positions()
        current_n = sim.n_bodies

        # Update trails
        for i in range(current_n):
            if i < len(trails):
                trails[i].append(pos[i].copy())
                if len(trails[i]) > max_trail:
                    trails[i].pop(0)

        # Clear and redraw
        ax.cla()
        ax.set_xlim(-extent, extent)
        ax.set_ylim(-extent, extent)
        ax.set_zlim(-extent, extent)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(f"N-Body Gravitational (t = {sim.t:.2f}, bodies = {current_n})")

        # Draw trails
        for i in range(current_n):
            if i < len(trails) and len(trails[i]) > 1:
                trail_arr = np.array(trails[i])
                ax.plot(
                    trail_arr[:, 0],
                    trail_arr[:, 1],
                    trail_arr[:, 2],
                    color=all_colors[i % max_bodies],
                    linewidth=0.8,
                    alpha=0.5,
                )

        # Marker sizes proportional to mass (log scale)
        current_masses = sim._masses[:current_n]
        log_masses = np.log10(current_masses + 1.0)
        sizes = 50 + 150 * (log_masses / max(log_masses.max(), 1.0))

        # Draw bodies
        ax.scatter(
            pos[:, 0],
            pos[:, 1],
            pos[:, 2],
            s=sizes,
            c=[all_colors[i % max_bodies] for i in range(current_n)],
            depthshade=True,
            alpha=0.9,
            edgecolors="k",
            linewidths=0.5,
        )

        return []

    _anim = FuncAnimation(  # noqa: F841
        fig, _animate, interval=33, cache_frame_data=False
    )

    plt.tight_layout()
    fig._anim = _anim  # type: ignore[attr-defined]  # prevent GC
    plt.show()


if __name__ == "__main__":
    run_nbody_3d()
