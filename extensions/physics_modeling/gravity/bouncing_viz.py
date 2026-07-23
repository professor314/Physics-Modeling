"""3D bouncing gravity visualization using matplotlib.

This module provides a standalone visualization of the bouncing simulation
in fountain mode, displaying colorful spheres falling under gravity and
bouncing off a floor plane.

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

    Creates a BouncingSimulation with 20 objects in fountain mode and
    renders them as colored scatter points in a 3D matplotlib figure.
    A grey floor plane is shown at the configured boundary_y level.

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

    sim = BouncingSimulation(config)

    # Set up the figure and 3D axes
    fig = plt.figure(figsize=(10, 8))
    ax: Any = fig.add_subplot(111, projection="3d")

    ax.set_title("Bouncing Objects - Fountain Mode")
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    ax.set_zlabel("Y (height)")

    half_extent = config.extent / 2.0
    ax.set_xlim(-half_extent, half_extent)
    ax.set_ylim(-half_extent, half_extent)
    ax.set_zlim(config.boundary_y, config.boundary_y + 30.0)

    # Draw the floor plane as a grey patch at boundary_y
    floor_size = half_extent * 0.8
    floor_verts = [
        [
            (-floor_size, -floor_size, config.boundary_y),
            (floor_size, -floor_size, config.boundary_y),
            (floor_size, floor_size, config.boundary_y),
            (-floor_size, floor_size, config.boundary_y),
        ]
    ]
    floor_patch = Poly3DCollection(
        floor_verts, alpha=0.3, facecolor="grey", edgecolor="darkgrey"
    )
    ax.add_collection3d(floor_patch)

    # Generate distinct colors for each object
    n = config.n_objects
    cmap = plt.cm.hsv  # type: ignore[attr-defined]
    colors = [cmap(i / n) for i in range(n)]

    # Initial scatter (empty positions, will be filled on first frame)
    scatter = ax.scatter([], [], [], s=80, c=[], depthshade=True)

    def _update(frame: int) -> Any:
        """Advance simulation and update scatter positions."""
        # Step multiple times per frame for smoother motion
        for _ in range(3):
            sim.step()

        state = sim.state
        xs = []
        ys = []
        zs = []
        cs = []

        for i in range(n):
            base = 6 * i
            x = state[base]
            y = state[base + 1]
            z = state[base + 2]

            # Only plot active objects (non-zero position or still within bounds)
            if abs(x) < config.extent and abs(z) < config.extent:
                xs.append(x)
                ys.append(z)  # swap z to matplotlib y-axis
                zs.append(y)  # height on matplotlib z-axis
                cs.append(colors[i])

        # Clear and re-draw scatter for updated positions
        ax.collections.remove(scatter)
        new_scatter = ax.scatter(
            xs, ys, zs, s=80, c=cs, depthshade=True, alpha=0.9
        )
        # Replace reference for next frame removal
        ax.collections.append(new_scatter)

        return (new_scatter,)

    # Use a workaround: directly manage scatter updates
    def _init() -> Any:
        return (scatter,)

    def _animate(frame: int) -> Any:
        """Advance simulation and update scatter positions."""
        for _ in range(3):
            sim.step()

        state = sim.state
        xs = []
        ys = []
        zs = []
        cs = []

        for i in range(n):
            base = 6 * i
            x = state[base]
            y = state[base + 1]
            z = state[base + 2]

            if abs(x) < config.extent and abs(z) < config.extent:
                xs.append(x)
                ys.append(z)
                zs.append(y)
                cs.append(colors[i])

        ax.cla()
        ax.set_title("Bouncing Objects - Fountain Mode")
        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.set_zlabel("Y (height)")
        ax.set_xlim(-half_extent, half_extent)
        ax.set_ylim(-half_extent, half_extent)
        ax.set_zlim(config.boundary_y, config.boundary_y + 30.0)

        # Re-draw floor
        floor_patch_new = Poly3DCollection(
            floor_verts, alpha=0.3, facecolor="grey", edgecolor="darkgrey"
        )
        ax.add_collection3d(floor_patch_new)

        # Draw spheres
        if xs:
            ax.scatter(xs, ys, zs, s=80, c=cs, depthshade=True, alpha=0.9)

        return []

    _anim = FuncAnimation(  # noqa: F841
        fig, _animate, interval=33, cache_frame_data=False
    )

    plt.tight_layout()
    fig._anim = _anim  # type: ignore[attr-defined]  # prevent GC
    plt.show()


if __name__ == "__main__":
    run_bouncing_3d()
