"""Double Pendulum — 2D Animated Visualization.

A standalone runnable demo that visualizes the :class:`DoublePendulum`
simulation in 2D using matplotlib. Features animated pendulum arms,
bob markers, and a fading trail of the lower bob showing the chaotic
trajectory.

Run directly::

    py -m physics_modeling.oscillators.double_pendulum_viz

Or call programmatically::

    from physics_modeling.oscillators.double_pendulum_viz import run_double_pendulum_2d
    run_double_pendulum_2d()
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.widgets import Slider

from physics_modeling.oscillators.double_pendulum import (
    DoublePendulum,
    DoublePendulumConfig,
)

__all__ = ["run_double_pendulum_2d"]


def run_double_pendulum_2d(config: DoublePendulumConfig | None = None) -> None:
    """Launch the interactive 2D double pendulum visualization.

    Creates a matplotlib 2D figure with FuncAnimation, drawing:
    - Two rigid pendulum arms from pivot to bob1 and bob1 to bob2
    - Colored bob markers at each joint
    - A fading trail showing the lower bob's trajectory history

    Interactive sliders allow real-time adjustment of L1, L2, and gravity.

    Parameters
    ----------
    config : DoublePendulumConfig | None
        Initial simulation configuration. Uses sensible defaults if *None*.
    """
    if config is None:
        config = DoublePendulumConfig()

    # --- Simulation state (mutable via closure) ---
    sim = DoublePendulum(config)
    trail_x: list[float] = []
    trail_y: list[float] = []
    max_trail: int = 500
    sub_steps: int = 4

    # --- Figure setup ---
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")

    total_length = config.L1 + config.L2
    margin = total_length * 0.3
    ax.set_xlim(-total_length - margin, total_length + margin)
    ax.set_ylim(-total_length - margin, total_length + margin)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title("Double Pendulum — Chaotic Motion")
    ax.grid(True, alpha=0.2)

    # Plot elements
    (arm_line,) = ax.plot([], [], "k-", linewidth=2.5)
    (bob1_dot,) = ax.plot([], [], "bo", markersize=12)
    (bob2_dot,) = ax.plot([], [], "ro", markersize=12)
    ax.plot([0], [0], "ks", markersize=10)  # pivot

    # Trail will be rendered as a LineCollection for fading effect
    trail_collection = LineCollection([], cmap="plasma", linewidths=1.5)
    ax.add_collection(trail_collection)

    # --- Make room for sliders ---
    fig.subplots_adjust(bottom=0.22)

    ax_l1 = fig.add_axes([0.2, 0.12, 0.6, 0.03])
    ax_l2 = fig.add_axes([0.2, 0.07, 0.6, 0.03])
    ax_grav = fig.add_axes([0.2, 0.02, 0.6, 0.03])

    slider_l1 = Slider(ax_l1, "L1 (m)", 0.2, 3.0, valinit=config.L1)
    slider_l2 = Slider(ax_l2, "L2 (m)", 0.2, 3.0, valinit=config.L2)
    slider_grav = Slider(ax_grav, "Gravity", 1.0, 20.0, valinit=config.g)

    def _on_slider_change(_val: float) -> None:
        """Reset simulation when any slider changes."""
        nonlocal sim, trail_x, trail_y
        new_config = DoublePendulumConfig(
            L1=slider_l1.val,
            L2=slider_l2.val,
            m1=config.m1,
            m2=config.m2,
            g=slider_grav.val,
            theta1_0=config.theta1_0,
            theta2_0=config.theta2_0,
            omega1_0=config.omega1_0,
            omega2_0=config.omega2_0,
            dt=config.dt,
            integrator=config.integrator,
        )
        sim = DoublePendulum(new_config)
        trail_x = []
        trail_y = []

        # Update axis limits
        new_total = new_config.L1 + new_config.L2
        new_margin = new_total * 0.3
        ax.set_xlim(-new_total - new_margin, new_total + new_margin)
        ax.set_ylim(-new_total - new_margin, new_total + new_margin)

    slider_l1.on_changed(_on_slider_change)
    slider_l2.on_changed(_on_slider_change)
    slider_grav.on_changed(_on_slider_change)

    # --- Animation callback ---
    def _animate(_frame: int) -> Any:
        nonlocal trail_x, trail_y

        # Advance simulation
        for _ in range(sub_steps):
            sim.step()

        # Get Cartesian positions
        (x1, y1), (x2, y2) = sim.cartesian_positions()

        # Pendulum arms: pivot -> bob1 -> bob2
        arm_line.set_data([0, x1, x2], [0, y1, y2])

        # Bob markers
        bob1_dot.set_data([x1], [y1])
        bob2_dot.set_data([x2], [y2])

        # Update trail
        trail_x.append(x2)
        trail_y.append(y2)
        if len(trail_x) > max_trail:
            trail_x.pop(0)
            trail_y.pop(0)

        # Build fading trail segments
        if len(trail_x) > 1:
            points = np.array([trail_x, trail_y]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            trail_collection.set_segments(segments)
            # Alpha fading: older segments are more transparent
            n_seg = len(segments)
            alphas = np.linspace(0.05, 0.9, n_seg)
            trail_collection.set_array(alphas)

        return arm_line, bob1_dot, bob2_dot, trail_collection

    # --- Start animation ---
    _ani = FuncAnimation(  # noqa: F841 — prevent GC
        fig,
        _animate,
        interval=30,
        blit=False,
        cache_frame_data=False,
    )

    plt.show()


if __name__ == "__main__":
    run_double_pendulum_2d()
