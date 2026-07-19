"""Spring Pendulum — 3D Animated Visualization.

A standalone runnable demo that visualizes the :class:`SpringPendulum`
simulation in 3D using matplotlib. Features a helix spring coil, red bob
marker, cyan trail, and interactive sliders for spring constant, damping,
and gravity.

Run directly::

    py -m physics_modeling.oscillators.spring_pendulum_viz

Or call programmatically::

    from physics_modeling.oscillators.spring_pendulum_viz import run_spring_pendulum_3d
    run_spring_pendulum_3d()
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers projection

from physics_modeling.oscillators.spring_pendulum import (
    SpringPendulum,
    SpringPendulumConfig,
)

__all__ = ["run_spring_pendulum_3d"]


def _generate_helix(
    start: np.ndarray,
    end: np.ndarray,
    n_coils: int = 10,
    radius: float = 0.08,
) -> np.ndarray:
    """Generate 3D helix points between *start* and *end* for spring visual.

    Parameters
    ----------
    start : ndarray
        Origin point of the spring (shape ``(3,)``).
    end : ndarray
        Endpoint of the spring / bob position (shape ``(3,)``).
    n_coils : int
        Number of coil turns to draw.
    radius : float
        Radius of each coil.

    Returns
    -------
    ndarray
        Array of shape ``(n_points, 3)`` representing the helix path.
    """
    direction = end - start
    length = np.linalg.norm(direction)
    if length < 1e-10:
        return np.array([[0.0, 0.0, 0.0]])

    # Build local coordinate frame
    z_axis = direction / length

    # Choose a reference vector not parallel to z_axis
    if abs(z_axis[0]) < 0.9:
        ref = np.array([1.0, 0.0, 0.0])
    else:
        ref = np.array([0.0, 1.0, 0.0])

    x_axis = np.cross(z_axis, ref)
    x_axis = x_axis / np.linalg.norm(x_axis)
    y_axis = np.cross(z_axis, x_axis)

    n_points = n_coils * 20
    t = np.linspace(0, 1, n_points)
    theta = np.linspace(0, n_coils * 2 * np.pi, n_points)

    points = np.zeros((n_points, 3))
    for i in range(n_points):
        center = start + t[i] * direction
        offset = radius * (np.cos(theta[i]) * x_axis + np.sin(theta[i]) * y_axis)
        points[i] = center + offset

    return points


def run_spring_pendulum_3d(config: SpringPendulumConfig | None = None) -> None:
    """Launch the interactive 3D spring pendulum visualization.

    Creates a matplotlib 3D figure with FuncAnimation, drawing:
    - A helix spring coil from the origin (pivot) to the bob
    - A red bob marker at the current position
    - A cyan trail showing the bob's trajectory history

    Interactive sliders allow real-time adjustment of spring constant *k*,
    damping coefficient, and gravitational acceleration *g*.

    Parameters
    ----------
    config : SpringPendulumConfig | None
        Initial simulation configuration. Uses sensible defaults if *None*.
    """
    if config is None:
        config = SpringPendulumConfig()

    # --- Simulation state (mutable via closure) ---
    sim = SpringPendulum(config)
    trail: list[np.ndarray] = []
    max_trail = 600
    sub_steps = 4  # sub-steps per frame for smoother physics

    # --- Figure setup ---
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim(-3, 3)
    ax.set_ylim(-4, 1)
    ax.set_zlim(-3, 3)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Spring Pendulum — 3D\n(drag to rotate, scroll to zoom)")

    # Plot elements
    (spring_line,) = ax.plot([], [], [], "b-", linewidth=1.2)
    (bob_dot,) = ax.plot([], [], [], "ro", markersize=12)
    (trail_line,) = ax.plot([], [], [], "c-", linewidth=0.8, alpha=0.5)
    ax.plot([0], [0], [0], "ks", markersize=8)  # pivot

    # --- Make room for sliders ---
    fig.subplots_adjust(bottom=0.25)

    # Slider axes
    ax_k = fig.add_axes([0.2, 0.14, 0.6, 0.03])
    ax_damp = fig.add_axes([0.2, 0.09, 0.6, 0.03])
    ax_grav = fig.add_axes([0.2, 0.04, 0.6, 0.03])

    slider_k = Slider(ax_k, "k (N/m)", 1.0, 50.0, valinit=config.k)
    slider_damp = Slider(ax_damp, "Damping", 0.0, 1.0, valinit=config.damping)
    slider_grav = Slider(ax_grav, "Gravity", 0.0, 20.0, valinit=config.g)

    def _on_slider_change(_val: float) -> None:
        """Reset simulation when any slider changes."""
        nonlocal sim, trail
        new_config = SpringPendulumConfig(
            k=slider_k.val,
            damping=slider_damp.val,
            mass=config.mass,
            rest_length=config.rest_length,
            g=slider_grav.val,
            air_resistance=config.air_resistance,
            initial_angle=config.initial_angle,
            initial_velocity=config.initial_velocity,
            dt=config.dt,
            integrator=config.integrator,
        )
        sim = SpringPendulum(new_config)
        trail = []

    slider_k.on_changed(_on_slider_change)
    slider_damp.on_changed(_on_slider_change)
    slider_grav.on_changed(_on_slider_change)

    # --- Animation callback ---
    def _animate(_frame: int) -> tuple:
        nonlocal trail

        # Advance simulation by several sub-steps per frame
        for _ in range(sub_steps):
            sim.step()

        pos = sim.state[:3]

        # Spring helix from origin to bob
        origin = np.array([0.0, 0.0, 0.0])
        helix = _generate_helix(origin, pos)
        spring_line.set_data(helix[:, 0], helix[:, 1])
        spring_line.set_3d_properties(helix[:, 2])

        # Bob
        bob_dot.set_data([pos[0]], [pos[1]])
        bob_dot.set_3d_properties([pos[2]])

        # Trail
        trail.append(pos.copy())
        if len(trail) > max_trail:
            trail.pop(0)

        if trail:
            t_arr = np.array(trail)
            trail_line.set_data(t_arr[:, 0], t_arr[:, 1])
            trail_line.set_3d_properties(t_arr[:, 2])

        return spring_line, bob_dot, trail_line

    # --- Start animation ---
    _ani = animation.FuncAnimation(  # noqa: F841 — prevent GC
        fig,
        _animate,
        interval=30,  # ~33 fps
        blit=False,
        cache_frame_data=False,
    )

    plt.show()


if __name__ == "__main__":
    run_spring_pendulum_3d()
