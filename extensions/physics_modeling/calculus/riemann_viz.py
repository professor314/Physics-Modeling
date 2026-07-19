"""2D Riemann sum visualization with interactive slider.

This module provides a standalone visualization of Riemann sums, plotting
the target function curve overlaid with colored rectangles representing
subdivisions. An interactive slider for *n* (number of rectangles) updates
the display in real time, and the computed sum and error are shown.

Functions
---------
run_riemann_2d
    Launch an interactive 2D visualization of Riemann sums.

Examples
--------
>>> from physics_modeling.calculus.riemann_viz import run_riemann_2d
>>> run_riemann_2d()  # doctest: +SKIP
"""

from __future__ import annotations

from math import sin
from typing import Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider

from physics_modeling.calculus.riemann import riemann_sum

__all__ = ["run_riemann_2d"]


def run_riemann_2d(
    f: Callable[[float], float] | None = None,
    a: float = 0.0,
    b: float = 2.0 * np.pi,
    initial_n: int = 10,
    method: str = "midpoint",
) -> None:
    """Launch an interactive 2D visualization of Riemann sums.

    Plots the function curve overlaid with colored rectangles for each
    subdivision. A slider for *n* updates the rectangles in real time.
    The computed sum value and relative error are displayed on the plot.

    Parameters
    ----------
    f : Callable[[float], float] | None
        Function to integrate. If ``None``, defaults to ``sin(x) + 1``
        (shifted so it is positive on [0, 2π]).
    a : float
        Left endpoint of the interval. Default ``0.0``.
    b : float
        Right endpoint of the interval. Default ``2π``.
    initial_n : int
        Initial number of subdivisions. Default ``10``.
    method : str
        Riemann sum method: ``"left"``, ``"right"``, ``"midpoint"``, or
        ``"trapezoid"``. Default ``"midpoint"``.

    Notes
    -----
    This function calls ``plt.show()`` which blocks until the user
    closes the figure window.

    The slider controls:
    - n: number of rectangles (range 1 to 200)

    The display shows:
    - Function curve in black
    - Colored rectangles (blue for positive height, red for negative)
    - Text showing the current sum and relative error
    """
    if f is None:

        def f(x: float) -> float:
            return sin(x) + 1.0

    # Fine curve for the function
    x_curve = np.linspace(a, b, 1000)
    y_curve = np.array([f(x) for x in x_curve], dtype=np.float64)

    # Set up figure with room for slider
    fig: Figure = plt.figure(figsize=(10, 7))
    ax: Axes = fig.add_axes([0.1, 0.22, 0.8, 0.68])

    ax.set_title(f"Riemann Sum ({method})")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")

    # Plot the function curve
    (line_curve,) = ax.plot(
        x_curve, y_curve, "k-", linewidth=2, label="f(x)", zorder=10
    )

    # Initial Riemann sum computation
    result = riemann_sum(f, a, b, initial_n, method)  # type: ignore[arg-type]

    # Draw rectangles
    def _make_patches(
        rectangles: np.ndarray,
    ) -> list[Rectangle]:
        """Create matplotlib Rectangle patches from rectangle data.

        Parameters
        ----------
        rectangles : np.ndarray
            Array of shape (n, 4) with [x_left, width, height, x_sample].

        Returns
        -------
        list[Rectangle]
            List of matplotlib Rectangle patches.
        """
        patches: list[Rectangle] = []
        for row in rectangles:
            x_left, width, height, _x_sample = row
            # For negative heights, draw rectangle below x-axis
            y_base = min(0.0, height)
            rect_height = abs(height)
            patch = Rectangle(
                (x_left, y_base), width, rect_height,
            )
            patches.append(patch)
        return patches

    patches = _make_patches(result.rectangles)
    colors = [
        (0.3, 0.6, 0.9, 0.4) if row[2] >= 0 else (0.9, 0.3, 0.3, 0.4)
        for row in result.rectangles
    ]
    collection = PatchCollection(
        patches, facecolors=colors, edgecolors="steelblue", linewidths=0.8
    )
    ax.add_collection(collection)

    # Add text annotation for sum value and error
    info_text = ax.text(
        0.02,
        0.95,
        f"Sum = {result.sum_value:.6f}\n"
        f"Reference = {result.reference_integral:.6f}\n"
        f"Error = {result.relative_error:.2e}",
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=10,
        fontfamily="monospace",
        bbox={"boxstyle": "round", "facecolor": "wheat", "alpha": 0.8},
    )

    ax.set_xlim(a - 0.1 * (b - a), b + 0.1 * (b - a))
    y_min = float(np.min(y_curve))
    y_max = float(np.max(y_curve))
    y_margin = 0.15 * (y_max - y_min) if y_max > y_min else 1.0
    ax.set_ylim(y_min - y_margin, y_max + y_margin)
    ax.axhline(0, color="gray", linewidth=0.5, linestyle="-")
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right")

    # Slider for n
    ax_n = fig.add_axes([0.2, 0.06, 0.6, 0.03])
    slider_n = Slider(
        ax_n,
        "n (subdivisions)",
        valmin=1,
        valmax=200,
        valinit=initial_n,
        valstep=1,
        valfmt="%d",
    )

    def _on_slider_changed(val: float) -> None:
        """Recompute Riemann sum and redraw rectangles when n changes."""
        n = int(slider_n.val)
        new_result = riemann_sum(f, a, b, n, method)  # type: ignore[arg-type]

        # Remove old collection and create new one
        ax.collections.clear()
        new_patches = _make_patches(new_result.rectangles)
        new_colors = [
            (0.3, 0.6, 0.9, 0.4) if row[2] >= 0 else (0.9, 0.3, 0.3, 0.4)
            for row in new_result.rectangles
        ]
        new_collection = PatchCollection(
            new_patches,
            facecolors=new_colors,
            edgecolors="steelblue",
            linewidths=0.8,
        )
        ax.add_collection(new_collection)

        # Update info text
        info_text.set_text(
            f"Sum = {new_result.sum_value:.6f}\n"
            f"Reference = {new_result.reference_integral:.6f}\n"
            f"Error = {new_result.relative_error:.2e}"
        )

        fig.canvas.draw_idle()

    slider_n.on_changed(_on_slider_changed)

    plt.show()


if __name__ == "__main__":
    run_riemann_2d()
