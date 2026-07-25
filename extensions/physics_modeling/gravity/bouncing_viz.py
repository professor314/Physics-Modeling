"""3D bouncing gravity visualization using matplotlib.

This module provides a standalone visualization of the bouncing simulation
in fountain mode, displaying colorful spheres falling under gravity and
bouncing off a floor plane. Interactive sliders control gravity, restitution,
and number of objects.

Functions
---------
run_bouncing_3d
    Launch an animated 3D visualization of bouncing objects.

Examples
--------
>>> from physics_modeling.gravity.bouncing_viz import run_bouncing_3d
>>> run_bouncing_3d()  # doctest: +SKIP
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers 3D projection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from physics_modeling.gravity.bouncing import (
    BouncingSimulation,
    GravityConfig,
    create_fountain_config,
)

__all__ = ["run_bouncing_3d"]


def run_bouncing_3d(config: GravityConfig | None = None) -> None:
    """Launch a 3D animated visualization of bouncing objects.

    Creates a BouncingSimulation with objects in fountain mode and
    renders them as colored scatter points in a 3D matplotlib figure.
    A grey floor plane is shown at the configured boundary_y level.

    Interactive sliders allow real-time adjustment of:
    - Gravity (m/s²)
    - Restitution (bounciness, 0-1)
    - Number of objects (resets simulation)

    Parameters
    ----------
    config : GravityConfig | None
        Optional configuration. If ``None``, a fountain configuration
        with 20 objects is used.

    Notes
    -----
    This function calls ``plt.show()`` which blocks until the user
    closes the figure window.
    """
    if config is None:
        config = create_fountain_config(n_objects=20)

    # Mutable simulation state
    sim = BouncingSimulation(config)
    current_n = config.n_objects

    # Set up the figure and 3D axes
    fig = plt.figure(figsize=(10, 9))
    ax: Any = fig.add_subplot(111, projection="3d")

    half_extent = config.extent / 2.0

    def _setup_axes() -> None:
        ax.set_title("Bouncing Objects - Fountain Mode")
        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.set_zlabel("Y (height)")
        ax.set_xlim(-half_extent, half_extent)
        ax.set_ylim(-half_extent, half_extent)
        ax.set_zlim(config.boundary_y, config.boundary_y + 30.0)

    _setup_axes()

    # Floor plane
    floor_size = half_extent * 0.8
    floor_verts = [
        [
            (-floor_size, -floor_size, config.boundary_y),
            (floor_size, -floor_size, config.boundary_y),
            (floor_size, floor_size, config.boundary_y),
            (-floor_size, floor_size, config.boundary_y),
        ]
    ]

    # --- Sliders ---
    fig.subplots_adjust(bottom=0.20)

    ax_grav = fig.add_axes([0.2, 0.12, 0.6, 0.03])
    ax_rest = fig.add_axes([0.2, 0.07, 0.6, 0.03])
    ax_num = fig.add_axes([0.2, 0.02, 0.6, 0.03])

    slider_grav = Slider(ax_grav, "Gravity", 1.0, 30.0, valinit=config.g)
    slider_rest = Slider(ax_rest, "Restitution", 0.0, 1.0, valinit=config.restitution)
    slider_num = Slider(ax_num, "# Objects", 2, 50, valinit=current_n, valstep=1, valfmt="%d")

    def _on_slider_change(_val: float) -> None:
        """Reset simulation when any slider changes."""
        nonlocal sim, current_n
        new_n = int(slider_num.val)
        new_config = create_fountain_config(n_objects=new_n)
        # Override g and restitution
        new_config.g = slider_grav.val
        new_config.restitution = slider_rest.val
        sim = BouncingSimulation(new_config)
        current_n = new_n

    slider_grav.on_changed(_on_slider_change)
    slider_rest.on_changed(_on_slider_change)
    slider_num.on_changed(_on_slider_change)

    # Generate colors (enough for max objects)
    cmap = plt.cm.hsv  # type: ignore[attr-defined]
    max_colors = 50
    all_colors = [cmap(i / max_colors) for i in range(max_colors)]

    # --- Animation callback ---
    def _animate(_frame: int) -> Any:
        n = current_n
        for _ in range(3):
            sim.step()

        state = sim.state
        xs = []
        ys = []
        zs = []
        cs = []

        for i in range(n):
            base = 6 * i
            if base + 2 >= len(state):
                break
            x = state[base]
            y = state[base + 1]
            z = state[base + 2]

            if abs(x) < config.extent and abs(z) < config.extent:
                xs.append(x)
                ys.append(z)  # swap z to matplotlib y-axis
                zs.append(y)  # height on matplotlib z-axis
                cs.append(all_colors[i % max_colors])

        ax.cla()
        _setup_axes()

        # Re-draw floor
        floor_patch = Poly3DCollection(
            floor_verts, alpha=0.3, facecolor="grey", edgecolor="darkgrey"
        )
        ax.add_collection3d(floor_patch)

        # Draw spheres
        if xs:
            ax.scatter(xs, ys, zs, s=80, c=cs, depthshade=True, alpha=0.9)

        return []

    _anim = FuncAnimation(  # noqa: F841
        fig, _animate, interval=33, cache_frame_data=False
    )

    fig._anim = _anim  # type: ignore[attr-defined]  # prevent GC
    plt.show()


if __name__ == "__main__":
    run_bouncing_3d()
