"""Rubik's cube solver using the Kociemba two-phase algorithm.

Provides a ``solve`` function that finds a near-optimal solution (≤20 moves)
for any valid cube state by delegating to the ``kociemba`` package.

If the ``kociemba`` package is not installed, importing this module still
succeeds — the error is deferred until ``solve()`` is actually called.
"""

from __future__ import annotations

from .cube_state import CubeState
from .moves import Move, parse_move_string
from .validation import is_valid_state


def solve(state: CubeState) -> list[Move]:
    """Find a near-optimal solution for the given cube state.

    Uses the Kociemba two-phase algorithm which guarantees solutions of at
    most 20 moves in half-turn metric.

    Parameters
    ----------
    state : CubeState
        The cube state to solve. Must be a valid, solvable configuration.

    Returns
    -------
    list[Move]
        Sequence of moves that brings the cube to the solved state.
        Returns an empty list if the cube is already solved.

    Raises
    ------
    ImportError
        If the ``kociemba`` package is not installed.
    ValueError
        If the state is not a valid solvable cube configuration.

    Examples
    --------
    >>> from physics_modeling.rubiks_cube import CubeState, solve
    >>> cube = CubeState.solved()
    >>> solve(cube)
    []
    """
    if state.is_solved():
        return []

    if not is_valid_state(state):
        raise ValueError(
            "Invalid cube state: the configuration is not solvable. "
            "Check that all facelets are correctly assigned."
        )

    try:
        import kociemba  # type: ignore[import-untyped]
    except ImportError as exc:
        raise ImportError(
            "The 'kociemba' package is required for the solver. "
            "Install with: pip install physics-modeling[rubiks]"
        ) from exc

    kociemba_str = state.to_kociemba_string()
    solution_str: str = kociemba.solve(kociemba_str)
    return parse_move_string(solution_str)
