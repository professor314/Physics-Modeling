"""N-Body Gravitational — 3D Animated Visualization.

A standalone runnable demo that visualizes the :class:`NBodySimulation`
in 3D using matplotlib. Features orbital trails with colored bodies,
starting with a binary star system plus a small test particle.

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
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers 3D projection

from physics_modeling.gravity.nbody import NBodyConfig, NBodySimulation

__all__ = ["run_nbody_3d"]


def _create_binary_star_system() -> tuple[
    NBodyConfig, np.ndarray, np.ndarray, np.ndarray
]:
    """Create a binary star + test particle initial configuration.

    Returns a binary star pair in circular orbit with a small test
    particle orbiting at a larger radius.

    Returns
    -------
    tuple
        ``(config, masses, positions, velocities)`` ready for
        NBodySimulation construction.
    """
    G = 1.0
    config = NBodyConfig(G=G, softening=0.01, integrator="verlet", dt=0.005)

    # Binary star masses
    m_star = 5.0
    m_particle = 0.001

    masses = np.array([m_star, m_star, m_particle], dtype=np.float64)

    # Binary separation and orbital velocity
    separation = 1.0
    v_orbital = np.sqrt(G * m_star / (2.0 * separation))

    positions = np.array(
        [
            [-separation / 2, 0.0, 0.0],
            [separation / 2, 0.0, 0.0],
            [0.0, 3.0, 0.0],
        ],
        dtype=np.float64,
    )

    velocities = np.array(
        [
            [0.0, -v_orbital, 0.0],
            [0.0, v_orbital, 0.0],
            [1.2, 0.0, 0.2],
        ],
        dtype=np.float64,
    )

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
    if config is None or masses is None or positions is None or velocities is None:
        config, masses, positions, velocities = _create_binary_star_system()

    sim = NBodySimulation(config, masses, positions, velocities)
    n = sim.n_bodies

    # Trail storage
    trails: list[list[np.ndarray]] = [[] for _ in range(n)]
    max_trail: int = 300
    sub_steps: int = 8

    # --- Figure setup ---
    fig = plt.figure(figsize=(10, 8))
    ax: Any = fig.add_subplot(111, projection="3d")

    # Axis limits based on initial positions
    extent = float(np.max(np.abs(positions))) * 2.0
    ax.set_xlim(-extent, extent)
    ax.set_ylim(-extent, extent)
    ax.set_zlim(-extent, extent)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("N-Body Gravitational Simulation")

    # Generate distinct colors for each body
    cmap = plt.cm.Set1  # type: ignore[attr-defined]
    colors = [cmap(i / max(n, 1)) for i in range(n)]

    # Marker sizes proportional to mass (log scale for visibility)
    log_masses = np.log10(masses + 1.0)
    sizes = 50 + 150 * (log_masses / max(log_masses.max(), 1.0))

    # --- Animation callback ---
    def _animate(_frame: int) -> Any:
        # Advance simulation
        for _ in range(sub_steps):
            sim.step()

        pos = sim.get_positions()

        # Update trails
        for i in range(n):
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
        ax.set_title(f"N-Body Gravitational (t = {sim.t:.2f})")

        # Draw trails
        for i in range(n):
            if len(trails[i]) > 1:
                trail_arr = np.array(trails[i])
                ax.plot(
                    trail_arr[:, 0],
                    trail_arr[:, 1],
                    trail_arr[:, 2],
                    color=colors[i],
                    linewidth=0.8,
                    alpha=0.5,
                )

        # Draw bodies
        ax.scatter(
            pos[:, 0],
            pos[:, 1],
            pos[:, 2],
            s=sizes,
            c=colors[:n],
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
