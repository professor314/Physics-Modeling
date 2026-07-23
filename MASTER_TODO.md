# Master TODO — All Projects

A single place to see what's next across all active projects. Ask "what can we work on?" and reference this file.

---

## Physics Modeling (professor314/Physics-Modeling)

**Status:** All phases complete. Future work is enhancements.

**Next items** (from `extensions/FUTURE.md`):

- [ ] **Dual-mode visualization** — wire existing Renderer protocol into viz files, build Plotly backend for Jupyter inline mode, auto-detect environment. Every sim works standalone AND in notebooks.
- [ ] **Lorenz attractor** — easy new sim, classic chaos demo. Extends core/ integrators.
- [ ] **Wave equation (1D)** — string vibration with boundary conditions. Medium difficulty.
- [ ] **Damped driven oscillator** — forced oscillation with resonance. Easy, extends oscillators/.
- [ ] **Property-based tests** — 8 optional Hypothesis tests are defined but not yet written (energy conservation, dimension checks, round-trip properties).
- [ ] **NumPy vectorization** — replace inner loops in gas and N-body with vectorized operations for speed.
- [ ] **State serialization** — save/load simulation snapshots (npz + JSON).

Full list: `extensions/FUTURE.md`

---

## Rubik's Cube (professor314/rubiks-cube)

**Status:** Complete and functional.

**Next items:**

- [ ] **Smooth rotation animation** — currently snaps to new state. Animate the face rotation over 200ms.
- [ ] **Solve playback** — show solution moves one at a time with a delay between each.
- [ ] **Timer with splits** — track cross/F2L/OLL/PLL phase times.
- [ ] **Scramble history** — save and replay past scrambles.
- [ ] **Cube state import** — input colors manually to solve a physical cube.
- [ ] **Different puzzle sizes** — 2x2, 4x4 variants.

---

## 6502 Simulator (professor314/6502-simulator)

**Status:** Core complete (CPU, assembler, LCD, debugger). Needs more programs and polish.

**Next items:**

- [ ] **More example programs** — fibonacci, multiply subroutine, string reversal, snake game.
- [ ] **Undocumented opcodes** — add the ~105 "illegal" opcodes used by some NES games.
- [ ] **Cycle-accurate timing** — track exact cycle counts for each instruction + page-crossing penalties.
- [ ] **Interrupt support** — wire up NMI (non-maskable interrupt) for timer-based events.
- [ ] **Keyboard I/O peripheral** — memory-mapped input so programs can read keypresses.
- [ ] **Visual debugger (matplotlib)** — TUI or GUI showing registers, memory hex dump, LCD, and disassembly in one window.
- [ ] **Unit tests** — test each opcode against known results from a 6502 test ROM.
- [ ] **Ben Eater compatible programs** — port his "Hello World" and LCD programs directly.

---

## Original Code Preservation (same repo as Physics Modeling)

**Status:** Complete. `.wps` journal files still need manual conversion.

**Next items:**

- [ ] **Convert .wps journal files** — open with Microsoft Works converter or Coolutils, paste into `docs/journal/weeks/week-XX.md` placeholders.
- [ ] **Rewrite compat shim** — update `compat/visual/` to use matplotlib instead of vpython (per updated spec).

---

## How to Use This File

When starting a session, ask: "What should we work on?" and I'll check this file and suggest the highest-value next item based on what you're in the mood for:
- **Quick win** → Add a new easy simulation (Lorenz, driven oscillator)
- **Deep work** → Dual-mode visualization, 6502 programs, property tests
- **Polish** → Convert journals, smooth cube animation, visual debugger
- **Writing** → New blog posts for any completed work
