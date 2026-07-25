"""Lissajous Figures — 3D Interactive Visualization.

A standalone runnable demo that visualizes Lissajous curves in 3D using
matplotlib with gradient coloring along the curve length. Interactive sliders
allow real-time adjustment of frequency ratios and phase offset.

Run directly::

    py -m physics_modeling.oscillators.lissajous_viz

Or call programmatically::

    from physics_modeling.oscillators.lissajous_viz import run_lissajous_3d
    run_lissajous_3d()
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d.art3d import Line3DCollection  # type: ignore[import-untyped]
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 — registers projection

from physics_modeling.oscillators.lissajous import (
    LissajousConfig,
    generate_lissajous,
    is_closed,
)

__all__ = ["run_lissajous_3d"]


def _build_gradient_segments(
    points: np.ndarray,
) -> tuple[Line3DCollection, np.ndarray]:
    """Build a Line3DCollection with per-segment color mapped to position along the curve.

    Parameters
    ----------
    points : ndarray
        Array of shape ``(n, 3)`` with the curve coordinates.

    Returns
    -------
    tuple[Line3DCollection, ndarray]
        The 3D line collection and the colour values array.
    """
    # Segments: pairs of consecutive points
    segments = np.array(
        [[points[i], points[i + 1]] for i in range(len(points) - 1)]
    )
    # Colour mapped to normalized arc position
    colors = np.linspace(0.0, 1.0, len(segments))
    lc = Line3DCollection(segments, cmap="plasma", linewidths=1.5)
    lc.set_array(colors)
    return lc, colors


def run_lissajous_3d(config: LissajousConfig | None = None) -> None:
    """Launch the interactive 3D Lissajous curve visualization.

    Creates a matplotlib 3D figure with gradient-colored Lissajous curve
    and sliders for frequency ratios (a, b, c) and phase offset (δ).

    When sliders change the curve is regenerated and redrawn immediately.

    Parameters
    ----------
    config : LissajousConfig | None
        Initial curve configuration. Uses defaults if *None*.
    """
    if config is None:
        config = LissajousConfig()

    # --- Figure setup ---
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    fig.subplots_adjust(bottom=0.28)

    # Initial curve
    points = generate_lissajous(config)
    lc, _ = _build_gradient_segments(points)
    ax.add_collection3d(lc)

    # Set axis limits based on amplitudes
    max_amp = max(config.A, config.B, config.C) * 1.2
    ax.set_xlim(-max_amp, max_amp)
    ax.set_ylim(-max_amp, max_amp)
    ax.set_zlim(-max_amp, max_amp)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    closed_str = "closed" if is_closed(config.a, config.b, config.c) else "open"
    ax.set_title(
        f"Lissajous Figure (a={config.a:.2f}, b={config.b:.2f}, "
        f"c={config.c:.2f}) — {closed_str}"
    )

    # --- Slider axes ---
    ax_a = fig.add_axes([0.2, 0.18, 0.6, 0.03])
    ax_b = fig.add_axes([0.2, 0.13, 0.6, 0.03])
    ax_c = fig.add_axes([0.2, 0.08, 0.6, 0.03])
    ax_delta = fig.add_axes([0.2, 0.03, 0.6, 0.03])

    slider_a = Slider(ax_a, "a (freq x)", 0.1, 10.0, valinit=config.a, valstep=0.1)
    slider_b = Slider(ax_b, "b (freq y)", 0.1, 10.0, valinit=config.b, valstep=0.1)
    slider_c = Slider(ax_c, "c (freq z)", 0.1, 10.0, valinit=config.c, valstep=0.1)
    slider_delta = Slider(
        ax_delta, "δ (phase)", 0.0, 2.0 * np.pi, valinit=config.delta
    )

    def _on_slider_change(_val: float) -> None:
        """Regenerate and redraw the curve when any slider changes."""
        nonlocal lc

        new_config = LissajousConfig(
            a=slider_a.val,
            b=slider_b.val,
            c=slider_c.val,
            A=config.A,
            B=config.B,
            C=config.C,
            delta=slider_delta.val,
            n_points=config.n_points,
        )

        # Remove all collections and re-add the new curve
        while ax.collections:
            ax.collections[0].remove()

        # Generate new curve
        new_points = generate_lissajous(new_config)
        lc, _ = _build_gradient_segments(new_points)
        ax.add_collection3d(lc)

        # Update title
        closed_str = (
            "closed"
            if is_closed(new_config.a, new_config.b, new_config.c)
            else "open"
        )
        ax.set_title(
            f"Lissajous Figure (a={new_config.a:.2f}, b={new_config.b:.2f}, "
            f"c={new_config.c:.2f}) — {closed_str}"
        )

        fig.canvas.draw_idle()

    slider_a.on_changed(_on_slider_change)
    slider_b.on_changed(_on_slider_change)
    slider_c.on_changed(_on_slider_change)
    slider_delta.on_changed(_on_slider_change)

    plt.show()


if __name__ == "__main__":
    run_lissajous_3d()
