"""2D SEIR epidemic model visualization with interactive sliders.

This module provides a standalone real-time visualization of the SEIR
compartmental model, plotting Susceptible, Exposed, Infected, and Recovered
populations over time with interactive parameter sliders.

Functions
---------
run_seir_2d
    Launch an animated 2D visualization of the SEIR model.

Examples
--------
>>> from physics_modeling.epidemics.seir_viz import run_seir_2d
>>> run_seir_2d()  # doctest: +SKIP
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

from physics_modeling.epidemics.seir import SEIRConfig, SEIRSimulation

__all__ = ["run_seir_2d"]


def run_seir_2d(config: SEIRConfig | None = None) -> None:
    """Launch a 2D visualization of the SEIR epidemic model.

    Creates an SEIR simulation and plots S, E, I, R curves as a
    time-series. Interactive sliders for beta, sigma, and gamma allow
    restarting the simulation with new parameters.

    Parameters
    ----------
    config : SEIRConfig | None
        Optional configuration. If ``None``, default SEIR parameters
        are used (S0=999, E0=0, I0=1, R0=0, beta=0.5, sigma=1/5,
        gamma=1/14).

    Notes
    -----
    This function calls ``plt.show()`` which blocks until the user
    closes the figure window.

    The sliders control:
    - β (beta): transmission rate (range 0.01 to 2.0)
    - σ (sigma): incubation rate (range 0.01 to 1.0)
    - γ (gamma): recovery rate (range 0.01 to 1.0)
    """
    if config is None:
        config = SEIRConfig()

    total_time: float = 200.0
    dt = config.dt

    def _run_simulation(
        beta: float, sigma: float, gamma: float
    ) -> tuple[list[float], list[float], list[float], list[float], list[float]]:
        """Run SEIR simulation with given parameters and return time series.

        Parameters
        ----------
        beta : float
            Transmission rate.
        sigma : float
            Incubation rate.
        gamma : float
            Recovery rate.

        Returns
        -------
        tuple
            ``(t_data, s_data, e_data, i_data, r_data)`` lists.
        """
        cfg = SEIRConfig(
            S0=config.S0,
            E0=config.E0,
            I0=config.I0,
            R0=config.R0,
            beta=beta,
            sigma=sigma,
            gamma=gamma,
            dt=dt,
            integrator=config.integrator,
        )
        local_sim = SEIRSimulation(cfg)

        t_data: list[float] = [0.0]
        s_data: list[float] = [cfg.S0]
        e_data: list[float] = [cfg.E0]
        i_data: list[float] = [cfg.I0]
        r_data: list[float] = [cfg.R0]

        steps = int(total_time / dt)
        for _ in range(steps):
            local_sim.step()
            t_data.append(local_sim.t)
            state = local_sim.state
            s_data.append(float(state[0]))
            e_data.append(float(state[1]))
            i_data.append(float(state[2]))
            r_data.append(float(state[3]))

        return t_data, s_data, e_data, i_data, r_data

    # Initial computation
    t_data, s_data, e_data, i_data, r_data = _run_simulation(
        config.beta, config.sigma, config.gamma
    )

    # Set up figure with room for sliders
    fig: Figure = plt.figure(figsize=(10, 7))
    ax: Axes = fig.add_axes([0.1, 0.28, 0.8, 0.62])

    ax.set_title(
        f"SEIR Epidemic Model (R₀ = {config.beta / config.gamma:.2f})"
    )
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Population")

    # Plot the initial curves
    (line_s,) = ax.plot(
        t_data, s_data, "b-", linewidth=2, label="Susceptible (S)"
    )
    (line_e,) = ax.plot(
        t_data, e_data, "m-", linewidth=2, label="Exposed (E)"
    )
    (line_i,) = ax.plot(
        t_data, i_data, "r-", linewidth=2, label="Infected (I)"
    )
    (line_r,) = ax.plot(
        t_data, r_data, "g-", linewidth=2, label="Recovered (R)"
    )

    ax.legend(loc="upper right")
    ax.set_xlim(0, total_time)
    total_pop = config.S0 + config.E0 + config.I0 + config.R0
    ax.set_ylim(0, total_pop * 1.05)
    ax.grid(True, alpha=0.3)

    # Add sliders for beta, sigma, gamma
    ax_beta = fig.add_axes([0.2, 0.16, 0.6, 0.03])
    ax_sigma = fig.add_axes([0.2, 0.10, 0.6, 0.03])
    ax_gamma = fig.add_axes([0.2, 0.04, 0.6, 0.03])

    slider_beta = Slider(
        ax_beta,
        "β (transmission)",
        valmin=0.01,
        valmax=2.0,
        valinit=config.beta,
        valfmt="%.3f",
    )
    slider_sigma = Slider(
        ax_sigma,
        "σ (incubation)",
        valmin=0.01,
        valmax=1.0,
        valinit=config.sigma,
        valfmt="%.3f",
    )
    slider_gamma = Slider(
        ax_gamma,
        "γ (recovery)",
        valmin=0.01,
        valmax=1.0,
        valinit=config.gamma,
        valfmt="%.3f",
    )

    def _on_slider_changed(_val: float) -> None:
        """Restart simulation with new slider parameters and redraw."""
        beta = slider_beta.val
        sigma = slider_sigma.val
        gamma = slider_gamma.val

        new_t, new_s, new_e, new_i, new_r = _run_simulation(
            beta, sigma, gamma
        )

        line_s.set_data(new_t, new_s)
        line_e.set_data(new_t, new_e)
        line_i.set_data(new_t, new_i)
        line_r.set_data(new_t, new_r)

        # Update R0 in title
        r0 = beta / gamma
        ax.set_title(f"SEIR Epidemic Model (R₀ = {r0:.2f})")

        fig.canvas.draw_idle()

    slider_beta.on_changed(_on_slider_changed)
    slider_sigma.on_changed(_on_slider_changed)
    slider_gamma.on_changed(_on_slider_changed)

    plt.show()


if __name__ == "__main__":
    run_seir_2d()
