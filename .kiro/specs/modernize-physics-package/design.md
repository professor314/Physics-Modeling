# Design Document: Modernize Physics Package

## Overview

This design covers the reorganization of a 2004-era college physics modeling project into a clean, portfolio-ready Git repository. The work involves:

1. **Directory restructuring** — moving ~50+ files into a clear hierarchy that separates original coursework from reference material and future extensions
2. **Duplicate resolution** — identifying canonical versions among 5+ copies of cube.py and multiple copies of other files
3. **Minimal Python 3 syntax fixes** — mechanical `print` → `print()`, `xrange` → `range`, etc.
4. **A compatibility shim** — a `compat/visual.py` module that maps legacy `from visual import *` to modern `vpython`
5. **RTF-to-markdown conversion** — extracting readable text from .rtf evaluation documents
6. **Documentation** — README, journal index, and future ideas

The guiding principle is **preservation over modernization**. The original code should feel like the same code the author wrote in 2004, with only the minimum changes needed to run on Python 3 + modern vpython.

## Architecture

```
physics-modeling/                    (new repo root)
├── original/
│   ├── rubiks-cube/                 # Signature project — all cube variants
│   ├── assignments/                 # Course assignments (spring, universe, etc.)
│   ├── extras/                      # Non-assignment code (crypto, assembler, etc.)
│   └── README.md                    # Index of original code with descriptions
├── references/
│   └── glowscript-examples/         # Third-party GlowScript examples (not original work)
├── compat/
│   └── visual.py                    # Compatibility shim for legacy imports
├── extensions/
│   ├── __init__.py
│   └── README.md                    # For future new work
├── docs/
│   ├── journal/
│   │   ├── weeks/                   # Journal Week 1-10 (converted from .wps)
│   │   ├── evaluations/             # Evaluation worksheets (converted from .rtf)
│   │   └── README.md                # Index with links to all entries
│   └── FUTURE_IDEAS.md              # Feature wishlist / roadmap
├── README.md                        # Top-level portfolio introduction
├── .gitignore
└── pyproject.toml                   # Minimal — declares vpython dependency
```

### Key Architectural Decisions

**Why `original/` as the primary directory**: Visitors to the repo should immediately see that this is someone's original work. Putting it front-and-center (not buried in `src/` or `lib/`) communicates "portfolio piece" rather than "production package."

**Why `compat/` is separate from `original/`**: The shim is new code written today. Mixing it into `original/` would violate the preservation boundary. Users add `compat/` to their Python path to make legacy imports work.

**Why `references/` exists**: The GlowScript examples are not the author's code. They need to be in the repo for context, but clearly marked as reference material so visitors don't attribute them to the author.

**Why no `src/` or `lib/`**: This isn't a distributable package. It's a portfolio of educational programs. The flat structure (`original/`, `docs/`, `compat/`) is more honest about what it is.

## Components and Interfaces

### Component 1: Directory Structure and File Placement

The reorganization maps existing files to their new locations based on these rules:

| Source Location | Destination | Rule |
|---|---|---|
| `Modeling Motion/Python Programs/best_cube.py`, `cube_class.py`, `cube.py`, `cube breakthrough!.py`, `cube backup.py`, `cube2.py`, `cube76.py`, `cubel75.py`, `cubetest.py`, `cube tester.py`, `cube(all turning works!).py`, `cube_functions.py`, `backup cube with one function ie right().py` | `original/rubiks-cube/` | All cube-related .py files |
| `quarter 1/Python Programs/cubes/*` (currentcube.py, expiriment.py, etc.) | `original/rubiks-cube/` | Cube sub-experiments |
| `quarter 1/folder from school/currentcube.py` | (duplicate — skip) | Same as cubes/currentcube.py |
| `quarter 1/assignments/spring.py`, `springsim.py`, `universe.py`, `collision.py`, `fountain.py`, `week4.py` | `original/assignments/` | Course assignments |
| `quarter 1/folder from school/sir.py`, `graph-sir.py`, `lissajous.py`, `lissa2.py`, `riemann.py`, `logistic.py`, `aviary.py`, `Bird Test.py` | `original/assignments/` | Course-related programs from school folder |
| `Python Programs/crypto.py`, `Chudnovsky.py`, `calc retest.py`, `calculus problem for test.py`, `calculus problem for test number 2.py` | `original/extras/` | Non-assignment programs |
| `week 4/decoder.py`, `decoder_homework.py`, `digital.py`, `pythonhomework.py` | `original/extras/` | Week 4 homework programs |
| `week 5/assembler.py`, `simulator.py`, `processor.py`, `instructionset.py`, `decoder.py`, `digital.py`, `falling.py` | `original/extras/` | Week 5 computer architecture programs |
| `test/1d.py`, `2d.py`, `aviary.py`, `final test 2c.py`, `LogisticEquation.py` | `original/extras/` | Test/exam programs |
| `Glowscript Examples/*` | `references/glowscript-examples/` | Not original work |
| `.wps` files | Not tracked in Git | Binary; converted externally |
| `.rtf` evaluation files | Kept in repo temporarily for reference during conversion | Readable text format |

### Component 2: Duplicate Resolution Strategy

Duplicates are resolved by this priority:

1. **Most complete version wins** — compare file sizes and content; the version with more code (functions, comments, etc.) is canonical
2. **Named variants are all kept for the cube** — `best_cube.py`, `cube_class.py`, `cube breakthrough!.py` etc. are NOT duplicates; they represent different evolutionary stages of the project. All go into `original/rubiks-cube/`
3. **True duplicates** (identical content in multiple directories) — keep only one copy. The `Modeling Motion/Python Programs/` versions are typically copies of `quarter 1/Python Programs/` files. Keep the `quarter 1/` originals as canonical since that's the natural chronological source.
4. **spring.py in folder from school vs assignments** — both are the same file (spring class definition). Keep the `assignments/` version as canonical.

Files to **definitely remove as duplicates**:
- `Modeling Motion/cube.py` (same as `quarter 1/Python Programs/cube.py` — an early version)
- `Modeling Motion/cube backup.py` (duplicate of `Python Programs/cube backup.py`)
- `Modeling Motion/cube(all turning works!).py` (duplicate of `Python Programs/` version)
- `quarter 1/folder from school/spring.py` (duplicate of `assignments/spring.py`)
- `quarter 1/folder from school/springsim.py` (duplicate of `assignments/springsim.py`)

### Component 3: Compatibility Shim (`compat/visual.py`)

The shim module allows `from visual import *` to resolve without changes to original code.

**Approach**: Create `compat/visual.py` that:
1. Imports everything from `vpython`
2. Re-exports under the `visual` namespace
3. Provides stub/workaround for removed APIs (mainly `frame`)

**Known API differences between legacy `visual` (2004) and modern `vpython`:**

| Legacy API | Modern vpython | Shim Strategy |
|---|---|---|
| `from visual import *` | `from vpython import *` | Shim re-exports all vpython names |
| `from visual.graph import *` | `from vpython import *` (graphs included) | Shim provides `visual/graph.py` submodule |
| `from visual.controls import *` | Removed in modern vpython | Shim provides stubs that warn but don't crash |
| `frame(axis=...)` | Removed — use `compound()` or manual transforms | Shim provides a `frame` class that uses compound or manual pos tracking |
| `display(x=..., y=...)` | `canvas(...)` with different params | Shim aliases `display` → `canvas` |
| `scene.range = N` | `scene.range = N` (same) | No change needed |
| `rate(N)` | `rate(N)` (same) | No change needed |
| `sphere`, `box`, `cylinder`, `curve`, `vector`, `color` | Same names in vpython | No change needed |

**Shim file structure:**
```
compat/
├── visual/
│   ├── __init__.py       # Main shim: from vpython import *; plus frame/display stubs
│   ├── graph.py          # from vpython import graph, gcurve, gdots, etc.
│   └── controls.py       # Stub: warns that controls UI is not available
└── README.md             # Usage instructions
```

**Usage**: Add `compat/` to `PYTHONPATH` or `sys.path` before running programs:
```bash
cd physics-modeling
PYTHONPATH=./compat python original/assignments/springsim.py
```

**Known limitations (document but don't fix)**:
- `best_cube.py` uses `visual.controls` which has no modern equivalent — will display a warning
- Programs using `frame` for composite objects (spring.py) need the shim's `frame` workaround which may have visual differences
- `display(x=4000, y=500)` pixel-positioning of windows isn't supported in modern vpython (browser-based)

### Component 4: RTF Conversion

The .rtf files contain human-readable text wrapped in RTF control codes. The conversion approach:

**Method**: Use Python's `striprtf` library (or manual regex stripping) to extract plain text, then format as markdown.

**RTF structure observed** (from `evalfinal.rtf`):
- Standard RTF header with font tables and stylesheet
- Body text in `\par`-delimited paragraphs
- Unicode escapes like `\u8217` for smart quotes
- Bold markers `{\b text}` for emphasis
- Tab characters `\tab` for indentation

**Conversion steps**:
1. Parse RTF control words to extract plain text
2. Convert `\par` sequences to paragraph breaks
3. Convert `{\b ...}` to markdown `**...**`
4. Replace Unicode escapes with actual characters
5. Add a YAML-like header with title, date, author
6. Add cross-references to code files where mentioned

**Files to convert**:
- `evalfinal.rtf` → `docs/journal/evaluations/final-evaluation.md`
- `Evaluation.rtf` → `docs/journal/evaluations/evaluation-worksheet.md`
- `evalbackup.rtf` → (likely duplicate of evalfinal — compare and keep one)
- `quarter 1/evals/evalfinal.rtf`, `evalbackup.rtf`, `Evaluation.rtf` → (duplicates of root-level ones)
- `quarter 1/folder from school/essay number 1.rtf` → `docs/journal/evaluations/essay-1.md`
- `test/*.rtf` files (1d.rtf, 2d.rtf, aviary.rtf, logistic.rtf, 2c.rtf) → these appear to be test answers; place in `docs/journal/evaluations/` or skip if too short

**WPS files (Journal Week 1-10)**:
- Binary Microsoft Works format — cannot be converted programmatically in this project
- User will convert externally using Microsoft Works 6-9 Converter or Coolutils online tool
- Placeholder markdown files created for each week with instructions on where to paste content

### Component 5: Python 3 Syntax Fixes

Mechanical transformations applied to all .py files in `original/`:

| Pattern | Replacement | Comment Annotation |
|---|---|---|
| `print x` | `print(x)  # Python 3 fix` | All bare print statements |
| `print x, y` | `print(x, y)  # Python 3 fix` | Multi-value prints |
| `print >>f, x` | `print(x, file=f)  # Python 3 fix` | File-directed prints |
| `xrange(...)` | `range(...)  # Python 3 fix` | If found |
| `raw_input(...)` | `input(...)  # Python 3 fix` | If found |
| `except E, e:` | `except E as e:  # Python 3 fix` | If found |

**What NOT to change**:
- Variable names, even if they shadow builtins
- Code structure or indentation style
- Class designs (even unusual ones like `Spring.__setattr__`)
- Comments (even if they have typos)
- Algorithm choices (Euler method stays Euler, no "upgrading" to RK4)

### Component 6: Documentation

**Top-level README.md** structure:
1. Title: "Modeling Motion — Physics Simulations (2004)"
2. One-paragraph introduction: college coursework, Evergreen State, what the project is
3. Highlight: the Rubik's cube as a from-scratch independent project
4. Simulation index: table with name, description, file path
5. How to Run: install vpython, set PYTHONPATH, run examples
6. Project Structure: directory tree with descriptions
7. Known Limitations: which programs work fully vs. need the frame workaround
8. Credits: Modeling Motion program, Barry Tolnas (instructor, based on sir.py attribution)
9. Link to docs/FUTURE_IDEAS.md

**docs/journal/README.md**: Chronological index linking to each week and evaluation.

**docs/FUTURE_IDEAS.md**: Ideas organized by category:
- Numerical methods (RK4, adaptive step size)
- Performance (numpy/scipy)
- Visualization (interactive controls, modern 3D)
- New models (double pendulum, n-body, chaos)
- Testing (unit tests for physics accuracy)

## Data Models

This project doesn't have runtime data models in the traditional sense. The relevant "data" is the file manifest — tracking which source files map to which destination:

```python
# Conceptual structure for the migration script (if automated)
FileMapping = {
    "source": str,          # relative path from current root
    "destination": str,     # relative path in new structure
    "category": str,        # "rubiks-cube" | "assignment" | "extra" | "reference"
    "is_duplicate": bool,   # True if this is a copy to be removed
    "canonical_of": str,    # If duplicate, path to the canonical version
}
```

The RTF conversion produces markdown files with this front matter:

```markdown
---
title: "Final Evaluation Worksheet"
author: Sean Connolly
date: 2004-03-10
course: Modeling Motion
original_file: evalfinal.rtf
---
```

## Error Handling

| Scenario | Handling |
|---|---|
| RTF file has corrupt/unusual control codes | Fall back to best-effort text extraction; note any garbled sections in a comment |
| .wps file cannot be converted | Create placeholder .md with filename and instructions for manual conversion |
| A program uses an API that the shim can't support | Shim logs a clear warning message; program may crash but the error message explains what's missing |
| Duplicate resolution is ambiguous (files differ slightly) | Keep both with a suffix indicating which version, add a note in the file header |
| A .py file has syntax errors even after fixes | Leave as-is with a note; the original code may have been a work-in-progress |

## Testing Strategy

### Why Property-Based Testing Does Not Apply

This project involves file reorganization, text format conversion, and documentation generation. There are no pure functions with meaningful input variation that would benefit from property-based testing:

- **File placement** is a one-time mapping (configuration, not logic)
- **RTF conversion** processes a fixed set of ~5 known files (not arbitrary input)
- **Syntax fixes** are mechanical find/replace patterns on known code
- **The compatibility shim** wraps an external library (vpython) — testing it requires actually running 3D visualizations

### Appropriate Testing Approach

**Manual verification**:
- Run each simulation after migration and confirm it displays correctly
- Compare converted markdown against RTF source text to confirm no content loss
- Verify duplicate removal didn't delete any unique content

**Smoke tests** (can be scripted):
- Import `compat.visual` and confirm it doesn't crash: `python -c "import sys; sys.path.insert(0, 'compat'); from visual import *"`
- Confirm all .py files in `original/` pass `python -m py_compile` (syntax-valid Python 3)
- Confirm no .wps, .xls, .pyc, .nb, .doc files remain tracked in Git

**Integration check**:
- Run `springsim.py` through the shim — the simplest visual program that exercises `frame`, `sphere`, `curve`, `rate`
- Run `sir.py` — pure computation, no visual dependency, easiest to verify

### Test Commands

```bash
# Verify all Python files compile
find original/ -name "*.py" -exec python -m py_compile {} \;

# Verify shim imports cleanly
PYTHONPATH=./compat python -c "from visual import *; print('shim OK')"

# Verify no binary files tracked
git ls-files | grep -E '\.(wps|xls|nb|doc|pyc|mht)$'  # should return nothing
```
