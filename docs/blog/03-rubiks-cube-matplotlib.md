# Rendering a 3D Rubik's Cube with Matplotlib

*How to draw a fully interactive Rubik's cube using Poly3DCollection, handle keyboard events for face rotations, and integrate the Kociemba two-phase solver.*

## Why Matplotlib for a Rubik's Cube?

Rubik's cube visualizations typically use OpenGL, Three.js, or a game engine. Using matplotlib's `mpl_toolkits.mplot3d` is unconventional — it's designed for scientific plotting, not real-time 3D interaction. But it has one huge advantage: zero dependencies beyond what you already have for data visualization. No WebGL, no GPU shaders, no build pipeline. Just `pip install matplotlib` and you have a working 3D cube.

The tradeoff is performance. Matplotlib redraws the entire figure on every move rather than updating a GPU buffer. For a Rubik's cube — where you're making one move at a time and waiting for human input — this is perfectly fine. The redraw takes maybe 50ms. You'd never build a first-person game this way, but for an interactive puzzle it works beautifully.

## Facelet Coordinate Math

A standard Rubik's cube has 6 faces, each with 9 facelets (3x3 grid). That's 54 colored squares to position in 3D space. The cube spans from (-1.5, -1.5, -1.5) to (1.5, 1.5, 1.5) — each cubie occupies a 1x1x1 unit.

Each facelet is a quadrilateral (4 vertices) lying on one of the six axis-aligned planes:

```python
# Face planes:
# U (top):    y = +1.5
# D (bottom): y = -1.5
# F (front):  z = +1.5
# B (back):   z = -1.5
# R (right):  x = +1.5
# L (left):   x = -1.5
```

For a facelet at grid position (row, col) on a given face, you compute the four corners on that face's plane. The tricky part is getting the orientation right — "row 0, col 0" needs to correspond to the visually correct top-left position when you're looking at that face from outside the cube.

For the front face (z = 1.5 plane):

```python
def _facelet_vertices_front(row, col):
    GAP = 0.05  # visual gap between facelets
    lo, hi = GAP, 1.0 - GAP
    x0 = -1.5 + col + lo
    x1 = -1.5 + col + hi
    y0 = 1.5 - (row + hi)   # row 0 is at the top
    y1 = 1.5 - (row + lo)
    return np.array([
        [x0, y0, 1.5],
        [x1, y0, 1.5],
        [x1, y1, 1.5],
        [x0, y1, 1.5],
    ])
```

The `GAP` constant creates a thin black border between facelets — without it, adjacent same-colored facelets merge visually and you lose the grid structure.

The back face is the subtlest case. It's mirrored relative to the front: when you look at the back face from behind the cube, "left" is actually "right" in world coordinates. The x-coordinates run in reverse:

```python
# B face (z = -1.5): mirrored x
x0 = 1.5 - (col + hi)
x1 = 1.5 - (col + lo)
```

Getting this wrong produces a cube that looks correct from the front but has mirrored colors on the back — a bug that's surprisingly hard to spot until you try solving it and the solver says the state is invalid.

## Drawing with Poly3DCollection

Once you have the 54 sets of 4 vertices, rendering is a single call:

```python
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

verts_list = []
colors_list = []
for face_idx in range(6):
    for row in range(3):
        for col in range(3):
            verts_list.append(facelet_vertices(face_idx, row, col))
            colors_list.append(COLOR_MAP[state.facelets[face_idx, row, col]])

collection = Poly3DCollection(
    verts_list, facecolors=colors_list,
    edgecolors="black", linewidths=0.5
)
ax.add_collection3d(collection)
```

The `edgecolors="black"` gives each facelet a distinct border. Without it, the cube looks like six solid colored planes with no grid structure.

On each move, you clear the axes and redraw everything. Matplotlib's 3D system doesn't support efficiently updating individual polygons in a collection, so full redraws are the way to go. Setting `ax.set_box_aspect([1, 1, 1])` ensures the cube isn't distorted by the figure's aspect ratio, and `ax.view_init(elev=25, azim=-50)` gives a nice default viewing angle showing three faces.

## The Tricky Move Cycle Definitions

A face rotation affects two things: the 9 facelets on the face itself (which rotate like a 2D grid), and the 12 facelets on adjacent faces that form a ring around the rotating face.

The face rotation is a numpy array rotation:

```python
# CW from outside the cube
facelets[face] = np.rot90(facelets[face], k=-1)
```

The edge ring is harder. Each face turn cycles 3 groups of 4 facelets. For example, a U (top) clockwise rotation moves:

```python
# F-top row -> R-top row -> B-top row -> L-top row
[(F, 0, 0), (R, 0, 0), (B, 0, 0), (L, 0, 0)],
[(F, 0, 1), (R, 0, 1), (B, 0, 1), (L, 0, 1)],
[(F, 0, 2), (R, 0, 2), (B, 0, 2), (L, 0, 2)],
```

That's the easy one — all top rows, all in the same direction. The R (right) face is where it gets interesting:

```python
# R face CW: F-right col -> U-right col -> B-left col (REVERSED) -> D-right col
[(F, 0, 2), (U, 0, 2), (B, 2, 0), (D, 0, 2)],
[(F, 1, 2), (U, 1, 2), (B, 1, 0), (D, 1, 2)],
[(F, 2, 2), (U, 2, 2), (B, 0, 0), (D, 2, 2)],
```

Notice how the B face indices are reversed: `(B, 2, 0), (B, 1, 0), (B, 0, 0)`. That's because the back face's "left column" runs top-to-bottom from behind, but the stickers that cycle into it come from the right column of the U face which runs top-to-bottom from front. The orientations are opposite.

I defined all six faces' cycles manually in a dictionary. Getting them wrong produces a cube that scrambles fine but can never be solved — the permutation doesn't correspond to any physical rotation. The validation test is simple: apply each move 4 times and verify you return to the solved state.

## Keyboard Events

Matplotlib's `mpl_connect("key_press_event", callback)` gives you keyboard input in the figure window. The mapping is compact:

```python
key_map = {
    "u": Move.U,  "d": Move.D,  "l": Move.L,
    "r": Move.R,  "f": Move.F,  "b": Move.B,
    "i": Move.U_PRIME, "k": Move.D_PRIME, "j": Move.L_PRIME,
    ";": Move.R_PRIME, "h": Move.F_PRIME, "n": Move.B_PRIME,
}
```

The CW keys are the face initials. The CCW keys are arranged around the keyboard for ergonomic one-handed use. The `s` key generates a random 20-move scramble and starts a timer. Space triggers the solver.

One gotcha: matplotlib's key events don't fire when the mouse is outside the figure window. This confused me initially — the cube seemed to stop responding to input until I clicked back on the figure.

## Kociemba Solver Integration

The Kociemba two-phase algorithm solves any valid Rubik's cube in at most 20 moves (provably). The `kociemba` Python package wraps this algorithm and accepts a 54-character string where each character represents a facelet's color.

The conversion from the internal `(6, 3, 3)` array to Kociemba format requires careful face ordering. Kociemba expects faces in the order U, R, F, D, L, B — reading each face left-to-right, top-to-bottom:

```python
def to_kociemba_string(self) -> str:
    chars = []
    for face_idx in [U, R, F, D, L, B]:  # Kociemba order
        face = self.facelets[face_idx]
        for row in range(3):
            for col in range(3):
                color = face[row, col]
                chars.append(face_char_for_color(color))
    return "".join(chars)
```

The solver returns a move string like `"U R2 F' D B2 L"` which gets parsed back into `Move` enums and applied to the state. The entire solve path animates in one frame — you see the cube jump from scrambled to solved, with the solution printed to the console.

The solver is an optional dependency (`pip install kociemba`). If it's not installed, pressing space prints a helpful message rather than crashing. This keeps the base package lightweight while giving power users a one-command solve.

## The Result

A fully interactive 3D Rubik's cube in about 300 lines of Python, with no dependencies beyond matplotlib and numpy (plus optional kociemba). You can scramble it, solve it by hand with keyboard controls, or let the algorithm solve it for you. The rendering is simple, the code is readable, and the whole thing installs with `pip install -e .`.

It's not as smooth as a WebGL implementation, but it runs anywhere Python runs — including SSH sessions with X forwarding, which is where I actually use it most.
