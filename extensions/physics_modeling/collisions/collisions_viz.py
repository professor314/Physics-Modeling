"""Visualization for elastic collision simulations.

This module provides an animated 3D scatter visualization showing
billiard-ball style elastic collisions in a bounded box.

Functions
---------
run_collisions_3d
    Launch an animated 3D scatter showing elastic sphere collisions.

Examples
--------
>>> from physics_modeling.collisions.collisions_viz import run_collisions_3d
>>> run_collisions_3d()  # opens a matplotlib 3D animation window
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from physics_modeling.collisions.elastic import CollisionConfig, CollisionSimulation

if TYPE_CHECKING:
    pass

__all__ = ["run_collisions_3d"]


def run_collisions_3d(
    n_objects: int = 5,
    box_size: float = 10.0,
    dt: float = 0.02,
    n_frames: int = 500,
    interval: int = 30,
) -> None:
    """Launch an animated 3D scatter showing elastic sphere collisions.

    Creates a bounded box with ``n_objects`` spheres of random initial
    velocities. Spheres bounce off each other elastically and reflect
    off the box walls.

    Parameters
    ----------
    n_objects : int
        Number of spheres to simulate. Default is 5.
    box_size : float
        Side length of the cubic bounding box. Default is 10.0.
    dt : float
        Time step for the simulation. Default is 0.02.
    n_frames : int
        Number of animation frames to render. Default is 500.
    interval : int
        Delay between frames in milliseconds. Default is 30.

    Notes
    -----
    Requires matplotlib to be installed. The animation opens in a new
    window when running in standalone mode.

    Examples
    --------
    >>> run_collisions_3d(n_objects=3, box_size=8.0, n_frames=200)
    """
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    # Create configuration with random initial velocities
    config = CollisionConfig(
        dt=dt,
        integrator="euler",
        dimensions=3,
        n_objects=n_objects,
        box_size=box_size,
    )
    sim = CollisionSimulation(config)

    # Set up the 3D figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(-box_size / 2, box_size / 2)
    ax.set_ylim(-box_size / 2, box_size / 2)
    ax.set_zlim(-box_size / 2, box_size / 2)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Elastic Collisions — 3D Billiard Balls")

    # Color map for objects
    colors = plt.cm.tab10(np.linspace(0, 1, n_objects))  # type: ignore[attr-defined]

    # Initial scatter
    positions = _extract_positions(sim.state, n_objects)
    scatter = ax.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        s=200,
        c=colors,
        depthshade=True,
    )

    half_box = box_size / 2.0

    def _apply_wall_bounces(sim: CollisionSimulation) -> None:
        """Reflect velocities off bounding box walls."""
        state = sim._state
        for i in range(n_objects):
            base = 6 * i
            for dim in range(3):
                pos = state[base + dim]
                vel = state[base + 3 + dim]
                if pos < -half_box:
                    state[base + dim] = -half_box
                    state[base + 3 + dim] = abs(vel)
                elif pos > half_box:
                    state[base + dim] = half_box
                    state[base + 3 + dim] = -abs(vel)

    def update(frame: int) -> tuple:  # type: ignore[type-arg]
        """Update function for animation."""
        sim.step()
        _apply_wall_bounces(sim)

        positions = _extract_positions(sim.state, n_objects)
        scatter._offsets3d = (  # type: ignore[attr-defined]
            positions[:, 0],
            positions[:, 1],
            positions[:, 2],
        )
        return (scatter,)

    _anim = FuncAnimation(  # noqa: F841
        fig, update, frames=n_frames, interval=interval, blit=False
    )
    plt.show()


def _extract_positions(
    state: np.ndarray, n_objects: int
) -> np.ndarray:
    """Extract position data from the flattened state vector.

    Parameters
    ----------
    state : np.ndarray
        1-D state vector of shape ``(n_objects * 6,)``.
    n_objects : int
        Number of objects in the simulation.

    Returns
    -------
    np.ndarray
        Array of shape ``(n_objects, 3)`` with position columns.
    """
    positions = np.zeros((n_objects, 3), dtype=np.float64)
    for i in range(n_objects):
        positions[i] = state[6 * i : 6 * i + 3]
    return positions
