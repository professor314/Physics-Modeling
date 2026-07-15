# Compatibility Shim for Legacy VPython

This directory provides a compatibility layer that allows code written for the legacy `visual` module (circa 2004) to run against modern `vpython` without modifying the original source files.

## How to Use

Add `compat/` to your Python path before running legacy programs:

```bash
# Linux/Mac
PYTHONPATH=./compat python original/assignments/springsim.py

# Windows (PowerShell)
$env:PYTHONPATH = ".\compat"
python original\assignments\springsim.py

# Windows (CMD)
set PYTHONPATH=.\compat
python original\assignments\springsim.py
```

## Prerequisites

Install modern vpython and numpy:

```bash
pip install vpython numpy
```

## What the Shim Provides

| Legacy Import | What Happens |
|---|---|
| `from visual import *` | Re-exports all of `vpython` plus `frame`, `display`, `gdisplay`, `arange` |
| `from visual.graph import *` | Re-exports vpython's graph objects (`graph`, `gcurve`, `gdots`, etc.) |
| `from visual.controls import *` | Provides no-op stubs that warn but don't crash |

## Known Limitations

1. **`frame` objects** — In legacy VPython, `frame` grouped objects so they could be moved/rotated together. The shim provides a stub that tracks `pos` and `axis` attributes but does NOT actually group child objects. Programs using `frame` (like `spring.py`) may have visual positioning issues.

2. **`display(x=..., y=...)` pixel positioning** — Legacy code could position the VPython window at specific screen coordinates. Modern vpython runs in a browser and doesn't support this. The shim maps `display` to `canvas` and ignores pixel-position parameters.

3. **`visual.controls`** — Legacy VPython had a separate UI controls system (buttons, sliders, toggles). This has no modern equivalent. The shim provides stubs that print a warning and do nothing.

4. **`gdisplay`** — Maps to vpython's `graph`. The API is largely compatible but some parameters (like `x`, `y` pixel positioning) are silently ignored.

## Programs Affected by Limitations

| Program | Issue | Severity |
|---|---|---|
| `spring.py` / `springsim.py` | Uses `frame` for composite object grouping | Visual differences — physics still runs |
| `cube*.py` | Uses `from visual import *` for 3D | Works if no `frame` usage |
| `logistic.py`, `2d.py`, `final test 2c.py` | Uses `from visual.graph import *` | Should work fine via graph.py shim |
| `sir.py`, `riemann.py`, `1d.py` | No visual imports (pure computation) | No shim needed |
