"""2D logistic growth visualization with interactive sliders.

This module provides a standalone visualization of the logistic equation,
plotting population growth curves with multiple step-count overlays and
the analytical solution. An interactive slider controls the growth rate *r*.

Functions
---------
run_logistic_2d
    Launch an animated 2D visualization of the logistic growth model.

Examples
--------
>>> from physics_modeling.calculus.logistic_viz import run_logistic_2d
>>> run_logistic_2d()  # doctest: +SKIP
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

from physics_modeling.calculus.logistic import LogisticConfig, LogisticSimulation

__all__ = ["run_logistic_2d"]


def run_logistic_2d(config: LogisticConfig | None = None) -> None:
    """Launch a 2D visualization of the logistic growth equation.

    Plots the logistic equation solution with multiple step counts overlaid
    (10, 50, 200, 1000 steps) alongside the exact analytical solution.
    An interactive slider lets the user modify the growth rate *r* in
    real time.

    Parameters
    ----------
    config : LogisticConfig | None
        Optional configuration. If ``None``, default parameters are used
        (y0=100, r=0.1, K=1000, t_end=75).

    Notes
    -----
    This function calls ``plt.show()`` which blocks until the user
    closes the figure window.

    The slider controls:
    - r: growth rate (range 0.01 to 1.0)

    When the slider value changes, all curves are recomputed and redrawn.
    """
    if config is None:
        config = LogisticConfig()

    step_counts: list[int] = [10, 50, 200, 1000]
    step_colors: list[str] = ["#e74c3c", "#f39c12", "#27ae60", "#2980b9"]
    step_styles: list[str] = ["--", "-.", ":", "-"]

    def _compute_curves(
        r: float,
    ) -> tuple[
        list[tuple[np.ndarray, np.ndarray]],
        tuple[np.ndarray, np.ndarray],
    ]:
        """Compute numerical and analytical curves for given r.

        Parameters
        ----------
        r : float
            Growth rate parameter.

        Returns
        -------
        tuple
            (numerical_results, analytical_curve) where numerical_results
            is a list of (t, y) arrays and analytical_curve is (t, y).
        """
        cfg = LogisticConfig(
            y0=config.y0,
            r=r,
            K=config.K,
            t_end=config.t_end,
            integrator=config.integrator,
        )
        sim = LogisticSimulation(cfg)
        numerical_results = sim.run_multiple_step_counts(step_counts)

        # Analytical solution on a fine grid
        t_analytical = np.linspace(0.0, config.t_end, 500)
        y_analytical = np.array(
            [sim.analytical_solution(t) for t in t_analytical],
            dtype=np.float64,
        )
        return numerical_results, (t_analytical, y_analytical)

    # Initial computation
    numerical, (t_ana, y_ana) = _compute_curves(config.r)

    # Set up figure with room for sliders
    fig: Figure = plt.figure(figsize=(10, 7))
    ax: Axes = fig.add_axes([0.1, 0.20, 0.8, 0.70])

    ax.set_title(f"Logistic Growth (r={config.r:.3f}, K={config.K:.0f})")
    ax.set_xlabel("Time")
    ax.set_ylabel("Population")

    # Plot analytical solution
    (line_analytical,) = ax.plot(
        t_ana, y_ana, "k-", linewidth=2.5, label="Analytical", zorder=10
    )

    # Plot numerical curves for each step count
    lines_numerical = []
    for idx, (t_arr, y_arr) in enumerate(numerical):
        (line,) = ax.plot(
            t_arr,
            y_arr,
            color=step_colors[idx],
            linestyle=step_styles[idx],
            linewidth=1.5,
            marker="o" if step_counts[idx] <= 50 else "",
            markersize=3,
            label=f"n={step_counts[idx]} steps",
        )
        lines_numerical.append(line)

    ax.legend(loc="lower right")
    ax.set_xlim(0, config.t_end)
    ax.set_ylim(0, config.K * 1.1)
    ax.grid(True, alpha=0.3)

    # Add slider for growth rate r
    ax_r = fig.add_axes([0.2, 0.06, 0.6, 0.03])
    slider_r = Slider(
        ax_r,
        "r (growth rate)",
        valmin=0.01,
        valmax=1.0,
        valinit=config.r,
        valfmt="%.3f",
    )

    def _on_slider_changed(val: float) -> None:
        """Recompute and redraw all curves when slider changes."""
        r = slider_r.val
        new_numerical, (new_t_ana, new_y_ana) = _compute_curves(r)

        # Update analytical
        line_analytical.set_data(new_t_ana, new_y_ana)

        # Update numerical curves
        for idx, (t_arr, y_arr) in enumerate(new_numerical):
            lines_numerical[idx].set_data(t_arr, y_arr)

        ax.set_title(f"Logistic Growth (r={r:.3f}, K={config.K:.0f})")
        fig.canvas.draw_idle()

    slider_r.on_changed(_on_slider_changed)

    plt.show()


if __name__ == "__main__":
    run_logistic_2d()
