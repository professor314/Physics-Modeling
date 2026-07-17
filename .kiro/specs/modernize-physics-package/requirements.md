# Requirements Document

## Introduction

This document specifies the requirements for organizing and lightly modernizing a college physics modeling project into a portfolio-ready repository. The existing codebase contains physics simulations (spring pendulums, bouncing ball universes, Rubik's cube visualizations, epidemic models, numerical integration, Lissajous figures, and more) written in Python 2 using the legacy `visual` (VPython) package during a "Modeling Motion" course at Evergreen State College circa 2004.

The guiding philosophy is **preservation**: this is the user's original work and should remain front-and-center. Changes are limited to what's necessary to make the code runnable on modern Python. New functionality belongs in a clearly separated area. The weekly journal entries and evaluation worksheets should be compiled into readable documentation that cross-references the code.

## Glossary

- **Original_Code**: The Python source files written by the user during the Modeling Motion course (2004), including assignments, personal projects like the Rubik's cube, and test programs
- **Repository**: The top-level Git repository containing all project files
- **Compatibility_Shim**: A thin Python package that maps legacy `visual` module imports to matplotlib-based equivalents, allowing Original_Code to run on modern Python (3.10+) without vpython
- **Journal_Entry**: A weekly reflection document written during the course (stored as .wps files in Microsoft Works binary format from 2004)
- **Evaluation_Worksheet**: A quarterly self-assessment document (stored as .rtf files) reflecting on learning goals, challenges, and accomplishments
- **VPython**: The legacy Python 3D visualization library used in the original code. The modernized project replaces vpython with matplotlib for compatibility with Python 3.10+
- **Syntax_Fix**: A minimal change to Original_Code that updates Python 2 syntax to Python 3 without altering logic, structure, or style

## Requirements

### Requirement 1: Repository Organization

**User Story:** As a developer showcasing my college work, I want the repository organized with clear separation between my original code and any new additions, so that visitors can immediately see what I built.

#### Acceptance Criteria

1. THE Repository SHALL organize Original_Code into a top-level `original/` directory preserving the existing folder structure (quarter 1, Python Programs, week directories)
2. THE Repository SHALL place the Rubik's cube programs (all variants: cube.py, best_cube.py, cube_class.py, cube breakthrough, etc.) in `original/rubiks-cube/` to highlight the user's signature project
3. THE Repository SHALL place course assignments (spring.py, universe.py, collision.py, fountain.py, springsim.py, etc.) in `original/assignments/`
4. THE Repository SHALL place supplementary programs (crypto.py, Chudnovsky.py, calculus programs, decoder, assembler, etc.) in `original/extras/`
5. THE Repository SHALL place GlowScript examples (the `Glowscript Examples/` folder) in a `references/glowscript-examples/` directory clearly marked as reference material, not original work
6. THE Repository SHALL include a `.gitignore` file excluding .pyc files, `__pycache__/` directories, .xls files, .nb files, .doc files, and build artifacts
7. THE Repository SHALL remove duplicate files where the same code exists in multiple locations, keeping the most complete version in its canonical location

### Requirement 2: Minimal Python 3 Syntax Fixes

**User Story:** As a developer, I want my original code updated with the minimum changes needed to run on Python 3, so that people can actually execute it without altering my original logic or style.

#### Acceptance Criteria

1. WHEN Original_Code contains `print` statements without parentheses, THE Syntax_Fix SHALL add parentheses to make them valid `print()` function calls
2. WHEN Original_Code uses `xrange()`, THE Syntax_Fix SHALL replace it with `range()`
3. WHEN Original_Code uses `raw_input()`, THE Syntax_Fix SHALL replace it with `input()`
4. WHEN Original_Code uses Python 2 integer division where float division is intended, THE Syntax_Fix SHALL add explicit `float()` casts or use `/` as appropriate to preserve original behavior
5. WHEN Original_Code uses Python 2 `except` syntax (comma instead of `as`), THE Syntax_Fix SHALL update to `except ExceptionType as e` syntax
6. THE Syntax_Fix SHALL NOT refactor, restructure, rename, add type annotations, or change the coding style of Original_Code
7. THE Syntax_Fix SHALL add a comment `# Python 3 fix` on any line that was modified, so the original author can see exactly what changed

### Requirement 3: Visualization Compatibility

**User Story:** As a developer, I want my VPython simulations to work on modern Python (3.10+) using matplotlib for visualization, so that anyone can run them without installing deprecated or version-incompatible libraries.

#### Acceptance Criteria

1. WHEN Original_Code uses `from visual import *` or `from visual.graph import *`, THE Compatibility_Shim SHALL allow those imports to resolve to a matplotlib-based rendering backend instead of vpython
2. THE Repository SHALL provide a `compat/visual/` shim package that re-exports common VPython object names (`sphere`, `box`, `cylinder`, `curve`, `vector`, `color`, `rate`, `scene`) as matplotlib 3D equivalents
3. THE Compatibility_Shim SHALL provide a `compat/visual/graph.py` module that maps `gdisplay`, `gcurve`, and `gvbars` to matplotlib 2D plotting equivalents
4. THE Compatibility_Shim SHALL render 3D simulations using matplotlib's `mpl_toolkits.mplot3d` with animation support (rotatable, zoomable view)
5. THE Compatibility_Shim SHALL render 2D graph-based simulations using standard matplotlib figures with real-time updates
6. WHEN a legacy VPython API has no matplotlib equivalent (e.g., `frame` object grouping), THE Compatibility_Shim SHALL provide a stub that tracks position/axis without crashing, and document the limitation
7. THE Compatibility_Shim SHALL NOT require vpython as a dependency; it SHALL depend only on matplotlib and numpy
8. THE Repository SHALL NOT require users to install vpython or use a specific Python version older than 3.10

### Requirement 4: Journal and Evaluation Compilation

**User Story:** As a developer presenting my portfolio, I want my weekly journal entries and evaluation worksheets compiled into readable markdown documents, so that visitors can understand my learning journey alongside the code.

#### Acceptance Criteria

1. THE Repository SHALL include a `docs/journal/` directory containing compiled journal and evaluation content
2. WHEN an .rtf evaluation file exists (evalfinal.rtf, Evaluation.rtf, evalbackup.rtf), THE Repository SHALL convert its content to a markdown file in `docs/journal/evaluations/`
3. WHEN a .wps journal file exists (Journal Week 1.wps through Journal Week 10.wps), THE Repository SHALL convert its content to markdown using the Microsoft Works 6-9 Converter or an online conversion tool (e.g., Coolutils), then place the resulting markdown in `docs/journal/weeks/`
4. IF a .wps file cannot be converted (corrupted or tool unavailable), THEN THE Repository SHALL provide a placeholder markdown file noting the issue and the original filename
5. THE compiled journal documents SHALL include cross-references to relevant code files (e.g., "Week 3: see `original/assignments/spring.py`")
6. THE Repository SHALL include a `docs/journal/README.md` index file linking to all weekly entries and evaluations in chronological order

### Requirement 5: Repository Hygiene

**User Story:** As a developer, I want a clean repository without binary files, duplicates, or clutter, so that it presents professionally on GitHub.

#### Acceptance Criteria

1. THE Repository SHALL NOT track binary files (.wps, .xls, .nb, .doc, .mht, .pyc) in Git after reorganization
2. THE .gitignore SHALL exclude: `*.pyc`, `__pycache__/`, `*.wps`, `*.xls`, `*.nb`, `*.doc`, `*.mht`, `*.jpg`, and common IDE/OS files (.DS_Store, Thumbs.db, .idea/, .vscode/)
3. WHEN the same Python file exists in multiple locations (e.g., cube.py duplicated across directories), THE Repository SHALL keep one canonical copy and remove duplicates
4. THE Repository SHALL preserve the .rtf evaluation files in the repository since they contain readable text content that has been converted to markdown
5. WHEN a `.pyc` or byte-compiled file exists without purpose, THE Repository SHALL remove it from tracking

### Requirement 6: Portfolio Documentation

**User Story:** As a developer, I want a README and supporting documentation that presents this project as my personal portfolio piece, so that visitors understand what each simulation does and how to run them.

#### Acceptance Criteria

1. THE Repository SHALL include a top-level README.md that introduces the project as original college coursework from the Modeling Motion program (2004)
2. THE README SHALL list each simulation with a one-line description of what it models (spring pendulum, bouncing ball universe, Rubik's cube, SIR epidemic, Lissajous figures, etc.)
3. THE README SHALL include a "How to Run" section with instructions for installing vpython and running the simulations
4. THE README SHALL include a "Project Structure" section showing the directory layout and what each folder contains
5. THE README SHALL credit the Modeling Motion program and note that the Rubik's cube program was an independent project built from scratch
6. WHEN a simulation requires special setup or has known limitations with modern vpython, THE README SHALL note this in the simulation listing

### Requirement 7: Future Extensibility Boundary

**User Story:** As a developer who may add new work later, I want a clear boundary between my original code and any future extensions, so that the original work is never confused with later additions.

#### Acceptance Criteria

1. THE Repository SHALL include an `extensions/` top-level directory designated for any new code written after the original coursework
2. THE `extensions/` directory SHALL include a README.md explaining its purpose: new experiments, modernized rewrites, or additional features built on the original work
3. WHEN new code is added to the repository in the future, THE Repository structure SHALL make it obvious through directory placement whether code is original (2004) or new work
4. THE Repository SHALL NOT place any new code inside the `original/` directory tree
5. THE `extensions/` directory SHALL include an `__init__.py` so it can function as a Python package if needed for future development

### Requirement 8: Feature Wishlist as GitHub Issues

**User Story:** As a developer planning future improvements, I want a documented list of logical extensions and enhancements tracked as GitHub issues, so that I have a clear roadmap for new features without cluttering the original codebase.

#### Acceptance Criteria

1. THE Repository SHALL include a `docs/FUTURE_IDEAS.md` file listing potential extensions to the codebase organized by category
2. THE feature list SHALL include ideas such as: adding RK4 numerical integration, numpy/scipy optimization, interactive parameter controls, unit tests for physics accuracy, additional simulation models, and modern 3D visualization improvements
3. EACH feature idea SHALL include a one-line description and a reference to which original code it extends or builds upon
4. THE README SHALL reference the FUTURE_IDEAS.md document and explain that these represent planned extensions, not original coursework
5. WHEN the repository is pushed to GitHub, THE feature ideas SHALL be suitable for creating as GitHub Issues for tracking and discussion
