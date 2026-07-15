# Implementation Plan: Modernize Physics Package

## Overview

This plan reorganizes a 2004-era college physics project into a clean, portfolio-ready repository. Tasks are ordered: gitignore → directory scaffolding → file moves → duplicate removal → Python 3 fixes → compatibility shim → RTF conversion → documentation. Each task is a self-contained unit of work.

## Tasks

- [x] 1. Create .gitignore and clean tracked binary files
  - Create `.gitignore` at the repository root with exclusions for: `*.pyc`, `__pycache__/`, `*.wps`, `*.xls`, `*.nb`, `*.doc`, `*.mht`, `*.jpg`, `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/`
  - Remove any currently tracked `.pyc` files from Git tracking (e.g., `week 4/digital.pyc`, `week 4/pythonhomework.pyc`, `week 5/assembler.pyc`, `week 5/instructionset.pyc`, `week 5/processor.pyc`, `quarter 1/assignments/billiards.pyc`, `quarter 1/assignments/spring.pyc`, `quarter 1/assignments/universe.pyc`, `quarter 1/folder from school/aviary.pyc`, `quarter 1/folder from school/spring.pyc`, `quarter 1/Python Programs/cube_class.pyc`, `quarter 1/Python Programs/cube_functions.pyc`)
  - _Requirements: 5.2, 5.5, 1.6_

- [x] 2. Create directory scaffolding
  - Create the following empty directories with placeholder files where needed:
    - `original/rubiks-cube/`
    - `original/assignments/`
    - `original/extras/`
    - `references/glowscript-examples/`
    - `compat/visual/` (will contain shim files)
    - `extensions/` (with `__init__.py` and `README.md`)
    - `docs/journal/weeks/`
    - `docs/journal/evaluations/`
  - Create `extensions/__init__.py` (empty file)
  - Create `extensions/README.md` explaining this directory is for new code added after the original 2004 coursework
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 7.1, 7.2, 7.5_

- [x] 3. Move Rubik's cube files to original/rubiks-cube/
  - Copy these files from `Modeling Motion/quarter 1/Python Programs/` to `original/rubiks-cube/`:
    - `best_cube.py`, `cube_class.py`, `cube_functions.py`, `cube.py`, `cube2.py`, `cube76.py`, `cubel75.py`, `cubetest.py`, `cube tester.py`, `cube backup.py`, `cube breakthrough!.py`, `cube(all turning works!).py`, `backup cube with one function ie right().py`
  - Copy from `Modeling Motion/quarter 1/Python Programs/cubes/`:
    - `currentcube.py`, `expiriment.py`, `get this box to grow!.py`, `this cube works!.py`
  - Copy from `Modeling Motion/quarter 1/folder from school/`:
    - `cube backup1.py`
  - Do NOT copy duplicates from `Modeling Motion/Python Programs/` or `Modeling Motion/` root (those are copies of the quarter 1 versions)
  - Delete the source files from their old locations after confirming the copies are in place
  - _Requirements: 1.2, 5.3, 1.7_

- [x] 4. Move assignment files to original/assignments/
  - Copy from `Modeling Motion/quarter 1/assignments/`:
    - `spring.py`, `springsim.py`, `universe.py`, `collision.py`, `fountain.py`, `week4.py`
  - Copy from `Modeling Motion/quarter 1/folder from school/` (NOT duplicates of assignments/):
    - `sir.py`, `graph-sir.py`, `lissajous.py`, `lissa2.py`, `riemann.py`, `logistic.py`, `aviary.py`, `Bird Test.py`
  - Skip `quarter 1/folder from school/spring.py` and `springsim.py` (duplicates of the assignments/ versions)
  - Delete old source files after confirming copies are placed
  - _Requirements: 1.3, 5.3, 1.7_

- [x] 5. Move extras files to original/extras/
  - Copy from `Modeling Motion/quarter 1/Python Programs/`:
    - `crypto.py`, `Chudnovsky.py`, `calc retest.py`, `calculus problem for test.py`, `calculus problem for test number 2.py`, `easy pi.py`
  - Copy from `Modeling Motion/week 4/`:
    - `decoder.py`, `decoder_homework.py`, `digital.py`, `pythonhomework.py`
  - Copy from `Modeling Motion/week 5/`:
    - `assembler.py`, `simulator.py`, `processor.py`, `instructionset.py`, `decoder.py` (rename to `decoder_week5.py` to avoid collision with week 4 version), `digital.py` (rename to `digital_week5.py`), `falling.py`
  - Copy from `Modeling Motion/test/` (or `quarter 1/test/`):
    - `1d.py`, `2d.py`, `aviary.py` (rename to `aviary_test.py` to avoid collision), `final test 2c.py`, `LogisticEquation.py`
  - Copy from `Modeling Motion/quarter 1/folder from school/`:
    - `sir-limit.py`, `normalize.py`, `for-loop.py`, `function.py`, `while-loop.py`
  - Copy `Modeling Motion/Simple Graph.py` to `original/extras/`
  - Also include the `.mm1.txt` assembly files from week 5 (add.mm1.txt, divide.mm1.txt, factorial.mm1.txt, if.mm1.txt, loop.mm1.txt) as they are source code for the assembler/simulator
  - Delete old source files after confirming copies
  - _Requirements: 1.4, 5.3, 1.7_

- [x] 6. Move GlowScript examples to references/glowscript-examples/
  - Copy all 31 .py files from `Glowscript Examples/` to `references/glowscript-examples/`
  - Delete the old `Glowscript Examples/` directory
  - _Requirements: 1.5_

- [x] 7. Checkpoint - Verify file moves
  - Confirm all .py source files are accounted for in `original/` or `references/`
  - Confirm no duplicate .py files remain in the old directory structure
  - Confirm the `Modeling Motion/` directory can be removed (all useful content has been moved)
  - Remove the now-empty `Modeling Motion/` directory tree (excluding files that are handled in later tasks like .rtf files — move those to a temp location first or handle in task 11)
  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Apply Python 3 syntax fixes to original/ files
  - For every .py file in `original/rubiks-cube/`, `original/assignments/`, and `original/extras/`:
    - Replace `print x` with `print(x)  # Python 3 fix`
    - Replace `print x, y` with `print(x, y)  # Python 3 fix`
    - Replace `xrange(...)` with `range(...)  # Python 3 fix`
    - Replace `raw_input(...)` with `input(...)  # Python 3 fix`
    - Replace `except E, e:` with `except E as e:  # Python 3 fix`
  - Do NOT change variable names, indentation style, algorithm logic, or comments
  - Add `# Python 3 fix` comment on every modified line
  - _Requirements: 2.1, 2.2, 2.3, 2.5, 2.6, 2.7_

- [x] 9. Write compatibility shim (compat/visual/)
  - [x] 9.1 Create `compat/visual/__init__.py`
    - Import everything from `vpython` and re-export
    - Alias `display` to `canvas`
    - Provide a `frame` class stub that warns about limited support but doesn't crash
    - Provide `controls` attribute that warns when accessed
    - _Requirements: 3.1, 3.2, 3.3, 3.5_
  - [x] 9.2 Create `compat/visual/graph.py`
    - Import graph-related objects from vpython (`graph`, `gcurve`, `gdots`, `gvbars`, `ghbars`)
    - Re-export them for `from visual.graph import *` compatibility
    - _Requirements: 3.1, 3.2_
  - [x] 9.3 Create `compat/visual/controls.py`
    - Provide stub functions/classes that print a warning: "visual.controls is not available in modern vpython"
    - Should not crash — just warn and no-op
    - _Requirements: 3.3_
  - [x] 9.4 Create `compat/README.md`
    - Document how to use the shim: add `compat/` to PYTHONPATH
    - List known limitations (frame, controls, display positioning)
    - _Requirements: 3.4_

- [x] 10. Checkpoint - Verify Python 3 compilation and shim
  - Run `python -m py_compile` on all .py files in `original/` to confirm they are valid Python 3 syntax
  - Run `python -c "import sys; sys.path.insert(0, 'compat'); from visual import *; print('shim OK')"` to verify the shim imports
  - Fix any remaining syntax issues found
  - Ensure all tests pass, ask the user if questions arise.

- [x] 11. Convert RTF evaluation files to markdown
  - Convert `evalfinal.rtf` → `docs/journal/evaluations/final-evaluation.md`
  - Convert `Evaluation.rtf` → `docs/journal/evaluations/evaluation-worksheet.md`
  - Compare `evalbackup.rtf` to `evalfinal.rtf` — if different, convert to `docs/journal/evaluations/evaluation-backup.md`; if identical, skip
  - Convert `quarter 1/folder from school/essay number 1.rtf` → `docs/journal/evaluations/essay-1.md`
  - Each converted file should have a YAML-style header: title, author (Sean Connolly), date (2004), course (Modeling Motion), original_file
  - Strip RTF control codes, convert `\par` to paragraph breaks, `{\b ...}` to `**...**`
  - Keep the original .rtf files in the repo for reference
  - _Requirements: 4.2, 5.4_

- [x] 12. Create placeholder files for .wps journal entries
  - For each of Journal Week 1 through Journal Week 10, create a placeholder markdown file in `docs/journal/weeks/`:
    - `docs/journal/weeks/week-01.md` through `docs/journal/weeks/week-10.md`
  - Each placeholder should contain:
    - YAML header with title, week number, original filename
    - A note: "Content pending conversion from Microsoft Works (.wps) format. Use Microsoft Works 6-9 Converter or Coolutils online tool to extract text, then paste here."
    - A cross-reference hint: suggested links to related code files for that week (based on week number)
  - _Requirements: 4.3, 4.4, 4.5_

- [x] 13. Create docs/journal/README.md index
  - Create a chronological index linking to all weekly entries (week-01.md through week-10.md)
  - Link to all evaluation documents in evaluations/
  - Include brief one-line description of each entry where known
  - _Requirements: 4.6_

- [x] 14. Create docs/FUTURE_IDEAS.md
  - Organize by category: Numerical Methods, Performance, Visualization, New Models, Testing
  - Each idea gets: title, one-line description, reference to which original code it extends
  - Ideas to include: RK4 integration (extends springsim.py), numpy/scipy optimization (extends universe.py), interactive parameter controls, unit tests for physics accuracy, double pendulum model, n-body simulation, modern 3D visualization, chaos/Lorenz attractor
  - _Requirements: 8.1, 8.2, 8.3_

- [x] 15. Create top-level README.md
  - Title: "Modeling Motion — Physics Simulations (2004)"
  - Introduction paragraph: Evergreen State College, Modeling Motion program, original coursework
  - Highlight the Rubik's cube as an independent from-scratch project
  - Simulation index: table with name, description, file path for each major simulation
  - "How to Run" section: install vpython (`pip install vpython`), set PYTHONPATH to include compat/, run examples
  - "Project Structure" section: directory tree with descriptions
  - "Known Limitations" section: which programs need the frame workaround, which use controls (won't work)
  - Credits: Modeling Motion program, instructor (Barry Tolnas, based on sir.py attribution)
  - Link to docs/FUTURE_IDEAS.md
  - Link to docs/journal/README.md
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 8.4_

- [x] 16. Create original/README.md index
  - Brief description of the original/ directory structure
  - List each subdirectory (rubiks-cube, assignments, extras) with what it contains
  - Note that all code is from 2004 with only minimal Python 3 syntax fixes applied
  - _Requirements: 1.1_

- [x] 17. Create pyproject.toml
  - Minimal project metadata: name, description, author, Python version requirement (>=3.7)
  - Declare `vpython` as the only dependency
  - This is NOT a distributable package — just documents the runtime requirement
  - _Requirements: 3.2_

- [-] 18. Final cleanup and verification
  - Verify no .pyc, .wps, .xls, .nb, .doc, .mht files are tracked in Git
  - Verify the old `Modeling Motion/` directory is fully removed (all content relocated)
  - Verify `temp_clone/` directory is removed if present
  - Verify directory structure matches the design document architecture diagram
  - Run `git ls-files` to confirm only intended files are tracked
  - Ensure all tests pass, ask the user if questions arise.

## Task Dependency Graph

```json
{
  "waves": [
    { "tasks": [1] },
    { "tasks": [2] },
    { "tasks": [3, 4, 5, 6] },
    { "tasks": [7] },
    { "tasks": [8, 9, 11, 12, 16] },
    { "tasks": [10, 13] },
    { "tasks": [14] },
    { "tasks": [15] },
    { "tasks": [17] },
    { "tasks": [18] }
  ]
}
```

## Notes

- No property-based testing applies — this is file reorganization and format conversion, not algorithmic code
- Tasks are ordered for logical dependency: structure first, then content moves, then code fixes, then documentation
- The .wps files cannot be converted programmatically — placeholders are created for manual paste-in later
- Original .rtf files are kept in the repo alongside their markdown conversions for reference
- Checkpoints at tasks 7, 10, and 18 allow verification of each major phase
