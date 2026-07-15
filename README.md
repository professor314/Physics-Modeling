# Modeling Motion — Physics Simulations (2004)

This is original coursework from the **Modeling Motion** program at The Evergreen State College (2004). These are Python simulations I wrote modeling physics phenomena — springs, gravity, epidemics, numerical integration, 3D visualization — using the VPython library. I was learning physics and programming simultaneously, figuring out how to translate equations of motion into running code. Everything here is from that year of exploration.

## The Rubik's Cube

The program I'm proudest of from this course is the Rubik's cube. It wasn't a class assignment — I built it entirely from scratch as an independent project. It renders a full 3D Rubik's cube using VPython and implements face rotations with correct piece tracking. The `original/rubiks-cube/` directory contains every evolutionary stage of the project, from early experiments (`get this box to grow!.py`) to the final working versions (`best_cube.py`, `cube_class.py`). Each file is a snapshot of me figuring out 3D transformations one breakthrough at a time.

## Simulations

| Simulation | Files | Description |
|---|---|---|
| Spring Pendulum | `original/assignments/spring.py`, `springsim.py` | Damped spring-mass system modeled with Euler's method |
| Universe Simulation | `original/assignments/universe.py`, `fountain.py` | Gravitational interactions, bouncing balls, particle fountain |
| Collision Detection | `original/assignments/collision.py` | Billiard ball elastic collisions |
| SIR Epidemic Model | `original/assignments/sir.py` | Susceptible-infected-recovered disease spread simulation |
| Logistic Equation | `original/assignments/logistic.py` | Population growth with carrying capacity |
| Lissajous Figures | `original/assignments/lissajous.py`, `lissa2.py` | Parametric curves rendered in 3D |
| Riemann Sums | `original/assignments/riemann.py` | Numerical integration visualization |
| Rubik's Cube | `original/rubiks-cube/` | 3D visualization and rotation of a Rubik's cube (independent project) |
| Assembly Simulator | `original/extras/assembler.py`, `processor.py`, `simulator.py` | Custom instruction set simulator with its own machine language |

## How to Run

### Prerequisites

- Python 3.7+
- vpython and numpy:

```
pip install vpython numpy
```

### Running Simulations

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
├── original/                    # All original code from 2004
│   ├── rubiks-cube/             # Rubik's cube project (all versions)
│   ├── assignments/             # Course assignments (springs, gravity, etc.)
│   └── extras/                  # Supplementary programs (crypto, assembler, calculus)
├── compat/                      # Compatibility shim for legacy VPython imports
│   └── visual/                  # Maps `from visual import *` to modern vpython
├── references/                  # Third-party material (NOT my original work)
│   └── glowscript-examples/    # GlowScript/VPython example programs
├── docs/
│   ├── journal/                 # Weekly reflections and evaluations
│   │   ├── weeks/               # Journal Week 1–10
│   │   └── evaluations/         # Quarterly self-assessments
│   └── FUTURE_IDEAS.md          # Planned extensions and improvements
├── extensions/                  # Reserved for future new work (empty for now)
├── .gitignore
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

I have ideas for extending this work — adding RK4 integration, numpy optimizations, interactive parameter controls, and new simulation models. See [docs/FUTURE_IDEAS.md](docs/FUTURE_IDEAS.md) for the full list. Any new code will live in the `extensions/` directory, keeping the original coursework untouched.

## Credits

- **The Modeling Motion program** at The Evergreen State College (2004)
- **Barry Tolnas** — instructor (credited in sir.py)
- The GlowScript examples in `references/` are third-party material included for reference, not original work
