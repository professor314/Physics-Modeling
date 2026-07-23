"""Visualization for the hard sphere gas simulation.

Provides an animated 3D scatter plot with velocity-dependent particle colouring
(blue=slow, red=fast) and a live speed histogram subplot.

Functions
---------
run_gas_3d
    Launch an animated 3D matplotlib visualization of the gas simulation.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from physics_modeling.gas.hard_sphere import GasConfig

__all__ = ["run_gas_3d"]


def run_gas_3d(
    config: GasConfig | None = None,
    n_steps: int = 5,
    interval: int = 50,
) -> None:
    """Run an animated 3D scatter visualization of the hard sphere gas.

    Displays a two-panel figure:
    - Left: 3D scatter plot of particle positions, coloured by speed
      (blue = slow, red = fast).
    - Right: Live histogram of the speed distribution.

    Parameters
    ----------
    config : GasConfig | None
        Gas simulation configuration. If ``None``, uses default GasConfig.
    n_steps : int
        Number of simulation steps per animation frame.
    interval : int
        Delay between animation frames in milliseconds.

    Notes
    -----
    Requires matplotlib to be installed. This function blocks until the
    animation window is closed.

    Examples
    --------
    >>> from physics_modeling.gas.gas_viz import run_gas_3d
    >>> from physics_modeling.gas.hard_sphere import GasConfig
    >>> run_gas_3d(GasConfig(n_particles=100, dt=0.001))  # doctest: +SKIP
    """
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    from physics_modeling.gas.hard_sphere import GasConfig, HardSphereGas

    if config is None:
        config = GasConfig(n_particles=50, dt=0.005, particle_radius=0.2)

    gas = HardSphereGas(config)

    fig = plt.figure(figsize=(14, 6))

    # 3D scatter plot
    ax3d = fig.add_subplot(121, projection="3d")
    ax3d.set_xlim(0, config.container_size[0])
    ax3d.set_ylim(0, config.container_size[1])
    ax3d.set_zlim(0, config.container_size[2])
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Z")
    ax3d.set_title("Hard Sphere Gas — 3D View")

    # Speed histogram
    ax_hist = fig.add_subplot(122)
    ax_hist.set_xlabel("Speed")
    ax_hist.set_ylabel("Count")
    ax_hist.set_title("Speed Distribution")

    # Initial scatter
    positions = gas.positions
    speeds = gas.speeds
    speed_max = np.max(speeds) if np.max(speeds) > 0 else 1.0
    colours = plt.cm.coolwarm(speeds / speed_max)  # type: ignore[attr-defined]

    scatter = ax3d.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        c=colours,
        s=10,
        alpha=0.7,
    )

    def update(frame: int) -> None:
        """Update function for each animation frame.

        Parameters
        ----------
        frame : int
            Frame index (unused — simulation advances internally).
        """
        # Advance simulation
        for _ in range(n_steps):
            gas.step()

        # Update 3D scatter
        positions = gas.positions
        speeds = gas.speeds
        speed_max = np.max(speeds) if np.max(speeds) > 0 else 1.0
        colours = plt.cm.coolwarm(speeds / speed_max)  # type: ignore[attr-defined]

        # Clear and re-draw scatter (mpl 3D scatter doesn't support set_offsets)
        ax3d.cla()
        ax3d.set_xlim(0, config.container_size[0])
        ax3d.set_ylim(0, config.container_size[1])
        ax3d.set_zlim(0, config.container_size[2])
        ax3d.set_xlabel("X")
        ax3d.set_ylabel("Y")
        ax3d.set_zlabel("Z")
        ax3d.set_title(f"Hard Sphere Gas — T={gas.temperature:.1f} K")
        ax3d.scatter(
            positions[:, 0],
            positions[:, 1],
            positions[:, 2],
            c=colours,
            s=10,
            alpha=0.7,
        )

        # Update histogram
        ax_hist.cla()
        ax_hist.set_xlabel("Speed")
        ax_hist.set_ylabel("Count")
        ax_hist.set_title("Speed Distribution")
        bin_centres, counts = gas.speed_distribution
        ax_hist.bar(
            bin_centres,
            counts,
            width=bin_centres[1] - bin_centres[0] if len(bin_centres) > 1 else 1.0,
            color="steelblue",
            alpha=0.7,
        )
        ax_hist.set_xlim(0, speed_max * 1.5)

    _anim = FuncAnimation(  # noqa: F841
        fig,
        update,
        interval=interval,
        cache_frame_data=False,
    )

    plt.tight_layout()
    fig._anim = _anim  # prevent garbage collection  # type: ignore[attr-defined]
    plt.show()
