"""2D SIR epidemic model visualization with interactive sliders.

This module provides a standalone real-time visualization of the SIR
compartmental model, plotting Susceptible, Infected, and Recovered
populations over time with interactive parameter sliders.

Functions
---------
run_sir_2d
    Launch an animated 2D visualization of the SIR model.

Examples
--------
>>> from physics_modeling.epidemics.sir_viz import run_sir_2d
>>> run_sir_2d()  # doctest: +SKIP
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

from physics_modeling.epidemics.sir import SIRConfig, SIRSimulation

__all__ = ["run_sir_2d"]


def run_sir_2d(config: SIRConfig | None = None) -> None:
    """Launch a 2D animated visualization of the SIR epidemic model.

    Creates an SIR simulation and plots S, I, R curves in real time.
    Interactive sliders for beta and gamma allow restarting the
    simulation with new parameters.

    Parameters
    ----------
    config : SIRConfig | None
        Optional configuration. If ``None``, default SIR parameters
        are used (S0=45400, I0=2100, R0=2500, beta=0.00001, gamma=1/14).

    Notes
    -----
    This function calls ``plt.show()`` which blocks until the user
    closes the figure window.

    The sliders control:
    - beta: transmission rate (range 0.000001 to 0.0001)
    - gamma: recovery rate (range 0.01 to 0.5)

    When a slider value changes, the simulation restarts from initial
    conditions with the new parameter values.
    """
    if config is None:
        config = SIRConfig()

    # Run the full simulation to pre-compute the curves
    sim = SIRSimulation(config)
    total_time = 200.0  # simulate 200 days
    dt = config.dt

    def _run_simulation(beta: float, gamma: float) -> tuple[
        list[float], list[float], list[float], list[float]
    ]:
        """Run SIR simulation with given parameters and return time series."""
        cfg = SIRConfig(
            S0=config.S0,
            I0=config.I0,
            R0=config.R0,
            beta=beta,
            gamma=gamma,
            dt=dt,
            integrator=config.integrator,
        )
        local_sim = SIRSimulation(cfg)

        t_data: list[float] = [0.0]
        s_data: list[float] = [cfg.S0]
        i_data: list[float] = [cfg.I0]
        r_data: list[float] = [cfg.R0]

        steps = int(total_time / dt)
        for _ in range(steps):
            local_sim.step()
            t_data.append(local_sim.t)
            state = local_sim.state
            s_data.append(float(state[0]))
            i_data.append(float(state[1]))
            r_data.append(float(state[2]))

        return t_data, s_data, i_data, r_data

    # Initial computation
    t_data, s_data, i_data, r_data = _run_simulation(config.beta, config.gamma)

    # Set up figure with room for sliders
    fig: Figure = plt.figure(figsize=(10, 7))
    ax: Axes = fig.add_axes([0.1, 0.25, 0.8, 0.65])

    ax.set_title("SIR Epidemic Model")
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Population")

    # Plot the initial curves
    (line_s,) = ax.plot(t_data, s_data, "b-", linewidth=2, label="Susceptible (S)")
    (line_i,) = ax.plot(t_data, i_data, "r-", linewidth=2, label="Infected (I)")
    (line_r,) = ax.plot(t_data, r_data, "g-", linewidth=2, label="Recovered (R)")

    ax.legend(loc="upper right")
    ax.set_xlim(0, total_time)
    total_pop = config.S0 + config.I0 + config.R0
    ax.set_ylim(0, total_pop * 1.05)
    ax.grid(True, alpha=0.3)

    # Add sliders for beta and gamma
    ax_beta = fig.add_axes([0.2, 0.10, 0.6, 0.03])
    ax_gamma = fig.add_axes([0.2, 0.04, 0.6, 0.03])

    slider_beta = Slider(
        ax_beta,
        "β (transmission)",
        valmin=0.000001,
        valmax=0.0001,
        valinit=config.beta,
        valfmt="%.7f",
    )
    slider_gamma = Slider(
        ax_gamma,
        "γ (recovery)",
        valmin=0.01,
        valmax=0.5,
        valinit=config.gamma,
        valfmt="%.4f",
    )

    def _on_slider_changed(val: float) -> None:
        """Restart simulation with new slider parameters and redraw."""
        beta = slider_beta.val
        gamma = slider_gamma.val

        new_t, new_s, new_i, new_r = _run_simulation(beta, gamma)

        line_s.set_data(new_t, new_s)
        line_i.set_data(new_t, new_i)
        line_r.set_data(new_t, new_r)

        # Update R0 in title
        n = config.S0 + config.I0 + config.R0
        r0 = beta * n / gamma
        ax.set_title(f"SIR Epidemic Model (R₀ = {r0:.2f})")

        fig.canvas.draw_idle()

    slider_beta.on_changed(_on_slider_changed)
    slider_gamma.on_changed(_on_slider_changed)

    plt.show()


if __name__ == "__main__":
    run_sir_2d()
