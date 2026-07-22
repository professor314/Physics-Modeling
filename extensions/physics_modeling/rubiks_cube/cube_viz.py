"""3D Rubik's cube visualization using matplotlib.

A standalone interactive visualization that renders a 3×3×3 Rubik's cube
in 3D using matplotlib's Poly3DCollection. Supports keyboard controls for
moves, scrambling, and solving (if kociemba is installed).

Controls:
    u → U move, i → U' move
    d → D move, k → D' move
    l → L move, j → L' move
    r → R move, ; → R' move
    f → F move, h → F' move
    b → B move, n → B' move
    s → scramble (random 20-move scramble)
    space → solve (requires kociemba)

Mouse: Click and drag to rotate the 3D view (built-in matplotlib behavior).

Validates: Requirements 14.6, 14.7, 14.8
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np
from numpy.typing import NDArray

from .cube_state import CubeState, U, D, L, R, F, B
from .moves import Move, apply_move, apply_sequence, move_to_string
from .scrambler import generate_scramble


# Standard Rubik's cube color scheme
# 0(U)=white, 1(D)=yellow, 2(L)=green, 3(R)=blue, 4(F)=red, 5(B)=orange
COLOR_MAP: dict[int, str] = {
    0: "#FFFFFF",  # White (U)
    1: "#FFFF00",  # Yellow (D)
    2: "#00FF00",  # Green (L)
    3: "#0000FF",  # Blue (R)
    4: "#FF0000",  # Red (F)
    5: "#FF8C00",  # Orange (B)
}

# Gap between facelets (fraction of cubie size)
_GAP: float = 0.05


def _facelet_vertices(
    face: int, row: int, col: int
) -> NDArray[np.float64]:
    """Compute the 4 corner vertices of a single facelet in 3D space.

    The cube spans from (-1.5, -1.5, -1.5) to (1.5, 1.5, 1.5).
    Each cubie is 1×1×1. Facelets are inset by _GAP on each side.

    Parameters
    ----------
    face : int
        Face index (U=0, D=1, L=2, R=3, F=4, B=5).
    row : int
        Row index on the face (0-2).
    col : int
        Column index on the face (0-2).

    Returns
    -------
    NDArray[np.float64]
        Shape (4, 3) array of vertex positions.
    """
    gap = _GAP
    # Compute inset square corners in a 2D local frame [0,1]×[0,1]
    lo = gap
    hi = 1.0 - gap

    if face == U:
        # U face: y = 1.5, x varies with col, z varies with row
        # row=0 is back (z=-1.5 side), row=2 is front (z=1.5 side)
        x0 = -1.5 + col + lo
        x1 = -1.5 + col + hi
        z0 = -1.5 + (2 - row) + lo
        z1 = -1.5 + (2 - row) + hi
        y = 1.5
        return np.array([
            [x0, y, z0],
            [x1, y, z0],
            [x1, y, z1],
            [x0, y, z1],
        ], dtype=np.float64)

    elif face == D:
        # D face: y = -1.5, x varies with col, z varies with row
        # row=0 is front (z=1.5 side), row=2 is back (z=-1.5 side)
        x0 = -1.5 + col + lo
        x1 = -1.5 + col + hi
        z0 = -1.5 + row + lo
        z1 = -1.5 + row + hi
        y = -1.5
        return np.array([
            [x0, y, z0],
            [x1, y, z0],
            [x1, y, z1],
            [x0, y, z1],
        ], dtype=np.float64)

    elif face == L:
        # L face: x = -1.5, z varies with col, y varies with row
        # row=0 is top (y=1.5), row=2 is bottom (y=-1.5)
        # col=0 is back (z=-1.5), col=2 is front (z=1.5)
        x = -1.5
        z0 = -1.5 + col + lo
        z1 = -1.5 + col + hi
        y0 = 1.5 - (row + hi)
        y1 = 1.5 - (row + lo)
        return np.array([
            [x, y0, z0],
            [x, y0, z1],
            [x, y1, z1],
            [x, y1, z0],
        ], dtype=np.float64)

    elif face == R:
        # R face: x = 1.5, z varies inversely with col, y varies with row
        # row=0 is top, col=0 is front (z=1.5), col=2 is back (z=-1.5)
        x = 1.5
        z0 = 1.5 - (col + hi)
        z1 = 1.5 - (col + lo)
        y0 = 1.5 - (row + hi)
        y1 = 1.5 - (row + lo)
        return np.array([
            [x, y0, z0],
            [x, y0, z1],
            [x, y1, z1],
            [x, y1, z0],
        ], dtype=np.float64)

    elif face == F:
        # F face: z = 1.5, x varies with col, y varies with row
        # row=0 is top (y=1.5), row=2 is bottom
        z = 1.5
        x0 = -1.5 + col + lo
        x1 = -1.5 + col + hi
        y0 = 1.5 - (row + hi)
        y1 = 1.5 - (row + lo)
        return np.array([
            [x0, y0, z],
            [x1, y0, z],
            [x1, y1, z],
            [x0, y1, z],
        ], dtype=np.float64)

    elif face == B:
        # B face: z = -1.5, x varies inversely with col, y varies with row
        # row=0 is top, col=0 is right (x=1.5), col=2 is left (x=-1.5)
        z = -1.5
        x0 = 1.5 - (col + hi)
        x1 = 1.5 - (col + lo)
        y0 = 1.5 - (row + hi)
        y1 = 1.5 - (row + lo)
        return np.array([
            [x0, y0, z],
            [x1, y0, z],
            [x1, y1, z],
            [x0, y1, z],
        ], dtype=np.float64)

    else:
        raise ValueError(f"Invalid face index: {face}")


class RubiksCubeViz:
    """Interactive 3D Rubik's cube visualization.

    Renders the cube state using matplotlib Poly3DCollection and handles
    keyboard events for move input, scrambling, and solving.

    Parameters
    ----------
    initial_state : CubeState | None
        Starting cube state. Defaults to solved.
    """

    def __init__(self, initial_state: CubeState | None = None) -> None:
        self._state: CubeState = initial_state or CubeState.solved()
        self._move_count: int = 0
        self._last_move: str = "None"
        self._status: str = "Solved" if self._state.is_solved() else "Scrambled"
        self._timer_start: float | None = None
        self._fig: Any = None
        self._ax: Any = None
        self._status_text: Any = None

    @property
    def state(self) -> CubeState:
        """Current cube state."""
        return self._state

    def _draw_cube(self) -> None:
        """Clear and redraw all 54 facelets on the 3D axes."""
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection

        self._ax.cla()

        vertices_list: list[NDArray[np.float64]] = []
        colors_list: list[str] = []

        for face_idx in range(6):
            for row in range(3):
                for col in range(3):
                    verts = _facelet_vertices(face_idx, row, col)
                    vertices_list.append(verts)
                    color_idx = int(self._state.facelets[face_idx, row, col])
                    colors_list.append(COLOR_MAP[color_idx])

        collection = Poly3DCollection(
            vertices_list,
            facecolors=colors_list,
            edgecolors="black",
            linewidths=0.5,
        )
        self._ax.add_collection3d(collection)

        # Set axes limits and appearance
        self._ax.set_xlim(-2, 2)
        self._ax.set_ylim(-2, 2)
        self._ax.set_zlim(-2, 2)
        self._ax.set_box_aspect([1, 1, 1])
        self._ax.set_axis_off()

        # Set a nice viewing angle
        self._ax.view_init(elev=25, azim=-50)

        self._update_status_text()

    def _update_status_text(self) -> None:
        """Update the status text below the figure."""
        timer_str = ""
        if self._timer_start is not None:
            elapsed = time.perf_counter() - self._timer_start
            timer_str = f" | Timer: {elapsed:.1f}s"

        text = (
            f"State: {self._status} | "
            f"Last move: {self._last_move} | "
            f"Moves: {self._move_count}"
            f"{timer_str}"
        )

        if self._status_text is not None:
            self._status_text.set_text(text)
        else:
            self._status_text = self._fig.text(
                0.5, 0.02, text,
                ha="center", va="bottom",
                fontsize=10, fontfamily="monospace",
            )

    def _apply_and_redraw(self, move: Move) -> None:
        """Apply a move, update state, and redraw.

        Parameters
        ----------
        move : Move
            The move to apply.
        """
        self._state = apply_move(self._state, move)
        self._move_count += 1
        self._last_move = move.value
        self._status = "Solved" if self._state.is_solved() else "Scrambled"

        if self._state.is_solved() and self._timer_start is not None:
            elapsed = time.perf_counter() - self._timer_start
            self._timer_start = None
            print(f"Solved! Time: {elapsed:.2f}s")

        print(f"Move: {move.value} (total: {self._move_count})")
        self._draw_cube()
        self._fig.canvas.draw_idle()

    def _on_key_press(self, event: Any) -> None:
        """Handle keyboard events for cube moves and commands.

        Parameters
        ----------
        event : matplotlib key_press_event
            The keyboard event.
        """
        if event.key is None:
            return

        key = event.key

        # Move mappings: key -> Move
        move_map: dict[str, Move] = {
            # CW moves (lowercase)
            "u": Move.U,
            "d": Move.D,
            "l": Move.L,
            "r": Move.R,
            "f": Move.F,
            "b": Move.B,
            # CCW moves (various keys)
            "i": Move.U_PRIME,
            "k": Move.D_PRIME,
            "j": Move.L_PRIME,
            ";": Move.R_PRIME,
            "h": Move.F_PRIME,
            "n": Move.B_PRIME,
            # Shift variants for CCW
            "U": Move.U_PRIME,
            "D": Move.D_PRIME,
            "L": Move.L_PRIME,
            "R": Move.R_PRIME,
            "F": Move.F_PRIME,
            "B": Move.B_PRIME,
            "shift+u": Move.U_PRIME,
            "shift+d": Move.D_PRIME,
            "shift+l": Move.L_PRIME,
            "shift+r": Move.R_PRIME,
            "shift+f": Move.F_PRIME,
            "shift+b": Move.B_PRIME,
        }

        if key in move_map:
            self._apply_and_redraw(move_map[key])
            return

        if key == "s":
            self._scramble()
            return

        if key == " ":
            self._solve()
            return

    def _scramble(self) -> None:
        """Generate and apply a random 20-move scramble."""
        scramble = generate_scramble(20)
        self._state = apply_sequence(self._state, scramble)
        self._move_count = 0
        self._last_move = "Scramble"
        self._status = "Scrambled"
        self._timer_start = time.perf_counter()

        scramble_str = move_to_string(scramble)
        print(f"Scramble: {scramble_str}")
        print("Timer started!")

        self._draw_cube()
        self._fig.canvas.draw_idle()

    def _solve(self) -> None:
        """Attempt to solve the cube using kociemba."""
        if self._state.is_solved():
            print("Already solved!")
            return

        try:
            from .solver import solve

            solution = solve(self._state)
            if not solution:
                print("Already solved!")
                return

            solution_str = move_to_string(solution)
            print(f"Solution ({len(solution)} moves): {solution_str}")

            # Apply solution moves one by one (snap, no animation)
            for move in solution:
                self._state = apply_move(self._state, move)
                self._move_count += 1
                self._last_move = move.value

            self._status = "Solved"
            if self._timer_start is not None:
                elapsed = time.perf_counter() - self._timer_start
                self._timer_start = None
                print(f"Solve time: {elapsed:.2f}s")

            self._draw_cube()
            self._fig.canvas.draw_idle()

        except ImportError:
            print(
                "kociemba not installed. "
                "Install with: pip install kociemba"
            )
        except Exception as exc:
            print(f"Solve failed: {exc}")

    def show(self) -> None:
        """Create the matplotlib figure and display the interactive cube."""
        import matplotlib.pyplot as plt

        self._fig = plt.figure(
            figsize=(8, 7),
            num="Rubik's Cube - Interactive 3D",
        )
        self._ax = self._fig.add_subplot(111, projection="3d")

        # Connect keyboard handler
        self._fig.canvas.mpl_connect("key_press_event", self._on_key_press)

        # Initial draw
        self._draw_cube()

        # Print help to console
        print("=" * 50)
        print("  Rubik's Cube - Interactive 3D Visualization")
        print("=" * 50)
        print("Controls:")
        print("  u/d/l/r/f/b    → CW face moves")
        print("  i/k/j/;/h/n    → CCW face moves (U'/D'/L'/R'/F'/B')")
        print("  Shift+letter   → CCW face moves (alternative)")
        print("  s              → Scramble (20 random moves)")
        print("  Space          → Solve (requires kociemba)")
        print("  Mouse drag     → Rotate view")
        print("=" * 50)

        plt.tight_layout()
        plt.subplots_adjust(bottom=0.08)
        plt.show()


def run_rubiks_cube() -> None:
    """Launch the interactive 3D Rubik's cube visualization.

    Entry point for standalone execution. Creates a solved cube and opens
    the matplotlib interactive window.

    Examples
    --------
    >>> run_rubiks_cube()  # doctest: +SKIP
    """
    viz = RubiksCubeViz()
    viz.show()


if __name__ == "__main__":
    run_rubiks_cube()
