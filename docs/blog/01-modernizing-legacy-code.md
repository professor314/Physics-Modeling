# Modernizing Legacy Code: From 2004 VPython to Python 3.14

*Taking old college physics simulations written twenty years ago and getting them running on modern Python.*

## The Time Capsule

In 2004, I was a student at The Evergreen State College in a program called Modeling Motion. We wrote Python simulations of physics phenomena — springs, gravity, epidemics, particle collisions — using a library called VPython. I was learning physics and programming simultaneously, translating equations of motion into running code for the first time.

Twenty years later, I found those files sitting in a folder. Python 2.4 syntax. `from visual import *` at the top of every file. Display windows configured with pixel coordinates. They were a time capsule of a specific moment in my learning journey — and none of them ran.

I wanted to preserve the originals exactly as they were while building something modern on top of them. That meant solving three problems: the VPython compatibility gap, choosing a matplotlib-first approach for the rewrite, and deciding what "preserve the original" actually means.

## The VPython Problem

VPython in 2004 was a standalone desktop application. You wrote `from visual import *`, and it gave you a 3D scene with spheres, boxes, arrows, and real-time animation. It was magical for teaching physics — you could see your differential equations come alive.

Modern vpython (lowercase, post-2016) still exists, but it runs in a browser via a Jupyter-like server. The API changed. The `frame` object was removed entirely. Window positioning like `display(x=4000, y=500)` became meaningless. My spring simulations used `frame` to group objects together for coordinated movement — that concept simply doesn't exist anymore.

I wrote a compatibility shim (`compat/visual/`) that maps the old `from visual import *` imports to modern vpython. It works for the simple cases — spheres, arrows, basic scenes. But anything using `frame` or display positioning is a best-effort approximation. The original visuals can't be perfectly reproduced.

This was the first lesson: preservation has limits. You can keep the code identical, but the runtime environment it was designed for no longer exists.

## The Matplotlib Approach

For the modern rewrite (the `extensions/` directory), I chose matplotlib over vpython entirely. The reasoning:

**Reproducibility.** Matplotlib produces identical output everywhere — laptops, servers, CI pipelines. No browser server, no WebSocket connections, no runtime dependencies beyond numpy and matplotlib itself.

**Testing.** You can't easily test vpython output. But matplotlib figures are data structures. You can verify axes limits, check that lines have the right coordinates, assert that animations produce the expected frames. This matters when you want property-based testing of your physics engine.

**Separation of concerns.** With matplotlib, the simulation engine is pure computation — numpy arrays in, numpy arrays out. The visualization is a separate layer that reads state histories and plots them. This is the architecture I wanted: physics decoupled from rendering.

**Interactive controls.** Matplotlib's widget system (`Slider`, `Button`, `RadioButtons`) gives you parameter adjustment without leaving the figure window. Every simulation in the package has interactive sliders for its physical constants — you can watch the system respond in real time as you drag the spring constant from 5 to 50.

The tradeoff is that matplotlib's 3D support is basic compared to vpython's native 3D scenes. For the spring pendulum and N-body simulations, I use `Axes3D` with `plot3D` and scatter plots. It works, but it's not the smooth real-time rotation you got with vpython. For the 2D simulations (SIR, logistic, Riemann sums), matplotlib is strictly better.

## Preserving the Original Philosophy

The hardest design decision was what to keep from the original code's philosophy versus what to modernize.

The 2004 code was written by someone learning. The variable names are sometimes cryptic (`r` for position, `p` for momentum, but also `r` for radius in the same file). The Euler integration is explicit and inline — no abstraction, no function call, just `velocity = velocity + acceleration * dt` written directly in the loop. Every simulation is a single file that runs top-to-bottom.

For the originals, I kept everything. The `original/` directory is untouched. Those files are the historical record — the actual code I wrote while learning physics, including the dead ends, the incomplete methods, and the inconsistent naming.

For the modern package, I extracted the physics. Each simulation answers the same question the original did — "what happens to this system over time?" — but through a structured `Simulation` base class with `initial_state()` and `derivatives()` methods. The numerical integration is pluggable (Euler, RK4, Verlet). The state is always a numpy array. The visualization is always a separate `_viz.py` file.

The insight: **the physics doesn't change, but the engineering around it does.** The spring force equation is the same as it was in 2004. What changed is how that equation gets evaluated, how the results get stored, and how errors get caught.

## What Running on Python 3.14 Actually Means

Python 3.14 isn't a dramatic breaking change for this kind of code. The real work was:

1. **Type annotations everywhere.** The modern package uses `NDArray[np.float64]`, `float | None` unions, dataclass configs. The original code has zero type information — and that's fine, it stays that way.

2. **Structured packaging.** `pyproject.toml`, entry points, optional dependencies, `py.typed` marker. The package installs cleanly with pip and exposes a CLI.

3. **Property-based testing.** Hypothesis generates random physical configurations and verifies invariants — energy conservation (within integrator tolerance), state vector dimensions, divergence detection. You can't test physics the same way you test a web form.

4. **Linting and formatting.** Ruff catches the kinds of bugs that would have been silent errors in 2004 — unused variables, unreachable code, import ordering.

The original code from 2004 doesn't need any of this. It ran, it taught me physics, it did its job. The modern package exists because I wanted to do the same physics with professional engineering practices — and because twenty years of Python evolution means I can express these simulations more clearly, test them more rigorously, and share them more easily than I ever could as a student.
