"""Visualization for elastic collision simulations.

This module provides an animated 3D scatter visualization showing
billiard-ball style elastic collisions in a bounded box. Interactive
sliders control number of objects, box size, and ball speed.

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
    interval: int = 30,
) -> None:
    """Launch an animated 3D scatter showing elastic sphere collisions.

    Creates a bounded box with ``n_objects`` spheres of random initial
    velocities. Spheres bounce off each other elastically and reflect
    off the box walls.

    Interactive sliders allow real-time adjustment of:
    - Number of objects (resets simulation)
    - Box size (resets simulation)
    - Ball speed multiplier (resets simulation)

    Parameters
    ----------
    n_objects : int
        Number of spheres to simulate. Default is 5.
    box_size : float
        Side length of the cubic bounding box. Default is 10.0.
    dt : float
        Time step for the simulation. Default is 0.02.
    interval : int
        Delay between frames in milliseconds. Default is 30.

    Notes
    -----
    Requires matplotlib to be installed. The animation opens in a new
    window when running in standalone mode.
    """
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.widgets import Slider
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    # Mutable state via closure
    current_n = n_objects
    current_box = box_size
    current_speed = 1.0

    def _create_sim(n: int, box: float) -> CollisionSimulation:
        config = CollisionConfig(
            dt=dt,
            integrator="euler",
            dimensions=3,
            n_objects=n,
            box_size=box,
        )
        return CollisionSimulation(config)

    sim = _create_sim(current_n, current_box)

    # Set up the 3D figure
    fig = plt.figure(figsize=(10, 9))
    ax = fig.add_subplot(111, projection="3d")

    def _setup_axes() -> None:
        half = current_box / 2
        ax.set_xlim(-half, half)
        ax.set_ylim(-half, half)
        ax.set_zlim(-half, half)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title(f"Elastic Collisions — {current_n} Balls in Box")

    _setup_axes()

    # --- Sliders ---
    fig.subplots_adjust(bottom=0.20)

    ax_n = fig.add_axes([0.2, 0.12, 0.6, 0.03])
    ax_box = fig.add_axes([0.2, 0.07, 0.6, 0.03])
    ax_speed = fig.add_axes([0.2, 0.02, 0.6, 0.03])

    slider_n = Slider(ax_n, "# Balls", 2, 20, valinit=n_objects, valstep=1, valfmt="%d")
    slider_box = Slider(ax_box, "Box Size", 4.0, 20.0, valinit=box_size)
    slider_speed = Slider(ax_speed, "Speed", 0.2, 3.0, valinit=1.0)

    def _on_slider_change(_val: float) -> None:
        """Reset simulation when any slider changes."""
        nonlocal sim, current_n, current_box, current_speed
        current_n = int(slider_n.val)
        current_box = slider_box.val
        current_speed = slider_speed.val
        sim = _create_sim(current_n, current_box)
        # Scale initial velocities by speed multiplier
        state = sim._state.copy()
        for i in range(current_n):
            base = 6 * i
            state[base + 3 : base + 6] *= current_speed
        sim._state = state

    slider_n.on_changed(_on_slider_change)
    slider_box.on_changed(_on_slider_change)
    slider_speed.on_changed(_on_slider_change)

    # Color map
    max_colors = 20
    all_colors = plt.cm.tab10(np.linspace(0, 1, max_colors))  # type: ignore[attr-defined]

    def _apply_wall_bounces() -> None:
        """Reflect velocities off bounding box walls."""
        half = current_box / 2.0
        state = sim._state
        for i in range(current_n):
            base = 6 * i
            for dim in range(3):
                pos = state[base + dim]
                vel = state[base + 3 + dim]
                if pos < -half:
                    state[base + dim] = -half
                    state[base + 3 + dim] = abs(vel)
                elif pos > half:
                    state[base + dim] = half
                    state[base + 3 + dim] = -abs(vel)

    def _animate(_frame: int) -> list:
        sim.step()
        _apply_wall_bounces()

        positions = _extract_positions(sim.state, current_n)

        ax.cla()
        _setup_axes()

        colors = [all_colors[i % max_colors] for i in range(current_n)]
        ax.scatter(
            positions[:, 0],
            positions[:, 1],
            positions[:, 2],
            s=200,
            c=colors,
            depthshade=True,
            alpha=0.9,
            edgecolors="k",
            linewidths=0.5,
        )

        return []

    _anim = FuncAnimation(  # noqa: F841
        fig, _animate, interval=interval, cache_frame_data=False
    )
    fig._anim = _anim  # type: ignore[attr-defined]  # prevent GC
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


if __name__ == "__main__":
    run_collisions_3d()
