"""Physics Modeling Launcher — GUI for selecting and running simulations.

A simple tkinter window with buttons for each simulation. Click a button
to launch the visualization. Close the viz window and you're back at
the launcher to pick another one.

Run directly::

    py -m physics_modeling.launcher

Or double-click the launcher shortcut if one has been created.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


# Simulation registry: (display_name, description, launch_function_path)
SIMULATIONS = [
    (
        "Spring Pendulum",
        "3D spring with helix coil, bob, and trail.\nSliders: spring constant, damping, gravity.",
        "physics_modeling.oscillators.spring_pendulum_viz",
        "run_spring_pendulum_3d",
    ),
    (
        "Double Pendulum",
        "2D chaotic double pendulum with fading trail.\nSliders: arm lengths, masses, gravity.",
        "physics_modeling.oscillators.double_pendulum_viz",
        "run_double_pendulum_2d",
    ),
    (
        "Lissajous Figures",
        "3D Lissajous curves — beautiful harmonic patterns.",
        "physics_modeling.oscillators.lissajous_viz",
        "run_lissajous_3d",
    ),
    (
        "Bouncing Objects",
        "3D fountain of balls bouncing off a floor.\nSliders: gravity, bounciness, # objects.",
        "physics_modeling.gravity.bouncing_viz",
        "run_bouncing_3d",
    ),
    (
        "N-Body Gravity",
        "Binary star system with orbiting particles.\nSliders: G, star mass, # particles.",
        "physics_modeling.gravity.nbody_viz",
        "run_nbody_3d",
    ),
    (
        "Elastic Collisions",
        "Billiard balls bouncing in a 3D box.\nSliders: # balls, box size, speed.",
        "physics_modeling.collisions.collisions_viz",
        "run_collisions_3d",
    ),
    (
        "Ideal Gas",
        "Hard-sphere gas particles in a container.",
        "physics_modeling.gas.gas_viz",
        "run_gas_3d",
    ),
    (
        "SIR Epidemic",
        "Susceptible-Infected-Recovered disease model.\nSliders: infection rate, recovery rate.",
        "physics_modeling.epidemics.sir_viz",
        "run_sir_2d",
    ),
    (
        "SEIR Epidemic",
        "SIR with Exposed compartment added.\nSliders: rates and incubation period.",
        "physics_modeling.epidemics.seir_viz",
        "run_seir_2d",
    ),
    (
        "Logistic Growth",
        "Population growth with carrying capacity.",
        "physics_modeling.calculus.logistic_viz",
        "run_logistic_2d",
    ),
    (
        "Riemann Sums",
        "Interactive area-under-curve approximation.\nSlider: # rectangles. Radio: method.",
        "physics_modeling.calculus.riemann_viz",
        "run_riemann_2d",
    ),
]


def _launch_sim(module_path: str, func_name: str) -> None:
    """Import and run a simulation function by module path."""
    import importlib

    mod = importlib.import_module(module_path)
    func = getattr(mod, func_name)
    func()


def main() -> None:
    """Launch the simulation picker GUI."""
    root = tk.Tk()
    root.title("Physics Modeling — Simulation Launcher")
    root.geometry("520x640")
    root.resizable(False, False)

    # Style
    style = ttk.Style()
    style.theme_use("clam")

    # Header
    header = ttk.Label(
        root,
        text="Physics Simulations",
        font=("Segoe UI", 18, "bold"),
        anchor="center",
    )
    header.pack(pady=(18, 4))

    subtitle = ttk.Label(
        root,
        text="Click a simulation to launch it.\nClose the plot window to return here.",
        font=("Segoe UI", 10),
        anchor="center",
        justify="center",
    )
    subtitle.pack(pady=(0, 12))

    # Scrollable frame for buttons
    canvas = tk.Canvas(root, highlightthickness=0)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scroll_frame = ttk.Frame(canvas)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10)
    scrollbar.pack(side="right", fill="y")

    # Mouse wheel scrolling
    def _on_mousewheel(event: tk.Event) -> None:  # type: ignore[type-arg]
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # Create a card-style button for each simulation
    for name, description, module_path, func_name in SIMULATIONS:
        frame = ttk.Frame(scroll_frame, relief="groove", borderwidth=1)
        frame.pack(fill="x", padx=8, pady=4)

        btn = ttk.Button(
            frame,
            text=f"▶  {name}",
            command=lambda m=module_path, f=func_name: _launch_sim(m, f),
        )
        btn.pack(fill="x", padx=6, pady=(6, 2))

        desc_label = ttk.Label(
            frame,
            text=description,
            font=("Segoe UI", 9),
            foreground="#555555",
            wraplength=450,
            justify="left",
        )
        desc_label.pack(fill="x", padx=10, pady=(0, 6))

    # Footer
    footer = ttk.Label(
        root,
        text="physics-modeling v0.1.0",
        font=("Segoe UI", 8),
        foreground="#999999",
        anchor="center",
    )
    footer.pack(side="bottom", pady=6)

    root.mainloop()


if __name__ == "__main__":
    main()
