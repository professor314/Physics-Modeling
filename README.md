# Modeling Motion — Physics Simulations (2004)

This is original coursework from the **Modeling Motion** program at The Evergreen State College (2004). These are Python simulations I wrote modeling physics phenomena — springs, gravity, epidemics, numerical integration, 3D visualization — using the VPython library. I was learning physics and programming simultaneously, figuring out how to translate equations of motion into running code. Everything here is from that year of exploration.

The `extensions/` directory contains a modern rewrite: the **physics-modeling** package with 12 interactive simulations, a CLI runner, and property-based tests. The `original/` directory preserves the 2004 code exactly as written.

## The Rubik's Cube

The program I'm proudest of from this course is the Rubik's cube. It wasn't a class assignment — I built it entirely from scratch as an independent project. It renders a full 3D Rubik's cube and implements face rotations with correct piece tracking.

The Rubik's cube has been extracted into its own repository: **[rubiks-cube](https://github.com/seanpoyner/rubiks-cube)**

The `original/rubiks-cube/` directory still contains every evolutionary stage of the original project, from early experiments (`get this box to grow!.py`) to the final working versions (`best_cube.py`, `cube_class.py`).

## Modern Physics Simulations (extensions/)

The `extensions/` directory contains the `physics-modeling` Python package — a full rewrite with 12 simulations available via CLI:

```bash
cd extensions && pip install -e .
physics-modeling list
```

| Simulation | CLI Command | Description |
|---|---|---|
| Spring Pendulum | `spring-pendulum` | 3D spring pendulum with interactive sliders |
| Double Pendulum | `double-pendulum` | 2D double pendulum with chaotic motion and trail |
| Lissajous Figures | `lissajous` | 3D Lissajous figure visualization |
| Bouncing/Gravity | `gravity` | 3D bouncing objects under gravity (fountain mode) |
| N-Body | `nbody` | 3D N-body gravitational simulation (binary star + particles) |
| Elastic Collisions | `collisions` | Elastic collision simulation |
| Hard-Sphere Gas | `gas` | Ideal gas hard-sphere simulation |
| SIR Epidemic | `sir` | SIR epidemic model with parameter sliders |
| SEIR Epidemic | `seir` | SEIR epidemic model with parameter sliders |
| Logistic Equation | `logistic` | Logistic growth equation visualization |
| Riemann Sums | `riemann` | Riemann sum visualization with interactive controls |
| Bouncing (alias) | `bouncing` | Alias for gravity simulation |

See the [extensions README](extensions/README.md) for full installation and usage details.

## Original Simulations (2004)

| Simulation | Files | Description |
|---|---|---|
| Spring Pendulum | `original/assignments/spring.py`, `springsim.py` | Damped spring-mass system modeled with Euler's method |
| Universe Simulation | `original/assignments/universe.py`, `fountain.py` | Gravitational interactions, bouncing balls, particle fountain |
| Collision Detection | `original/assignments/collision.py` | Billiard ball elastic collisions |
| SIR Epidemic Model | `original/assignments/sir.py` | Susceptible-infected-recovered disease spread simulation |
| Logistic Equation | `original/assignments/logistic.py` | Population growth with carrying capacity |
| Lissajous Figures | `original/assignments/lissajous.py`, `lissa2.py` | Parametric curves rendered in 3D |
| Riemann Sums | `original/assignments/riemann.py` | Numerical integration visualization |
| Assembly Simulator | `original/extras/assembler.py`, `processor.py`, `simulator.py` | Custom instruction set simulator with its own machine language |

## How to Run

### Modern Package (recommended)

```bash
cd extensions
pip install -e .
physics-modeling spring-pendulum
```

### Original Code (requires VPython compatibility shim)

Set `PYTHONPATH` to include the compatibility shim so legacy `from visual import *` imports resolve correctly:

**PowerShell:**
```powershell
$env:PYTHONPATH = ".\compat"
python original/assignments/springsim.py
```

**Bash:**
```bash
PYTHONPATH=./compat python original/assignments/springsim.py
```

### Non-Visual Programs

Some programs don't require vpython and run directly:

```bash
python original/assignments/sir.py
python original/assignments/riemann.py
python original/assignments/logistic.py
```

## Project Structure

```
modeling-motion/
├── extensions/                  # Modern physics-modeling package (12 simulations)
│   ├── physics_modeling/        # Source code (core, oscillators, gravity, etc.)
│   ├── tests/                   # Property-based and unit tests
│   ├── notebooks/               # Jupyter training notebooks
│   └── pyproject.toml           # Package configuration
├── original/                    # All original code from 2004 (preserved)
│   ├── rubiks-cube/             # Rubik's cube project (all versions)
│   ├── assignments/             # Course assignments (springs, gravity, etc.)
│   └── extras/                  # Supplementary programs (crypto, assembler, calculus)
├── compat/                      # Compatibility shim for legacy VPython imports
│   └── visual/                  # Maps `from visual import *` to modern vpython
├── rubiks-cube/                 # Standalone Rubik's cube package (separate repo)
├── docs/
│   ├── journal/                 # Weekly reflections and evaluations
│   ├── blog/                    # Technical blog posts
│   └── FUTURE_IDEAS.md          # Planned extensions and improvements
├── .github/workflows/ci.yml     # CI pipeline
└── README.md                    # This file
```

## Known Limitations

- **Programs using `frame`** (spring.py, springsim.py) may have visual positioning issues with modern vpython. The `frame` object was removed from vpython — the compatibility shim provides a workaround, but composite objects may not render identically to the 2004 originals.
- **Assembly simulator programs** (`falling.py`, `.mm1` files) are source code for the custom CPU instruction set, not runnable Python scripts.
- **Some programs were works-in-progress.** `LogisticEquation.py` has incomplete methods. Several cube files are intermediate experiments that may not run cleanly.
- **The cube programs have many evolutionary versions.** `best_cube.py` and `cube_class.py` are the most complete and functional. The others document the journey.
- **Window positioning** (`display(x=4000, y=500)`) doesn't work in modern vpython since it now runs in a browser rather than a native window.

## Journal & Learning Journey

The `docs/journal/` directory contains weekly reflections and evaluation worksheets from the course. These document what I was learning each week, what I struggled with, and how my understanding of physics and programming evolved together. See the [journal index](docs/journal/README.md) for a chronological listing.

## Future Plans

I have ideas for extending this work — adding more simulations, numpy optimizations, interactive parameter controls, and new models. See [docs/FUTURE_IDEAS.md](docs/FUTURE_IDEAS.md) for the full list. New code lives in the `extensions/` directory, keeping the original coursework untouched.

## Credits

- **The Modeling Motion program** at The Evergreen State College (2004)
- **Barry Tolnas** — instructor (credited in sir.py)
- The GlowScript examples in `references/` are third-party material included for reference, not original work
