"""Rubik's cube random scramble generator.

Generates WCA-style scrambles: random move sequences where no two consecutive
moves operate on the same face. This module does *not* depend on the
``kociemba`` package.
"""

from __future__ import annotations

import random

from .moves import Move


# Group moves by face for constraint checking
_FACE_MOVES: dict[str, list[Move]] = {
    "U": [Move.U, Move.U_PRIME, Move.U2],
    "D": [Move.D, Move.D_PRIME, Move.D2],
    "L": [Move.L, Move.L_PRIME, Move.L2],
    "R": [Move.R, Move.R_PRIME, Move.R2],
    "F": [Move.F, Move.F_PRIME, Move.F2],
    "B": [Move.B, Move.B_PRIME, Move.B2],
}

_FACES = list(_FACE_MOVES.keys())

# Flat list of all 18 moves
_ALL_MOVES: list[Move] = [m for group in _FACE_MOVES.values() for m in group]


def _face_of(move: Move) -> str:
    """Return the face letter that a move operates on.

    Parameters
    ----------
    move : Move
        Any standard cube move.

    Returns
    -------
    str
        Single character face identifier ('U', 'D', 'L', 'R', 'F', 'B').
    """
    return move.value[0]


def generate_scramble(length: int = 20) -> list[Move]:
    """Generate a random scramble sequence.

    Produces a sequence of random moves where no two consecutive moves
    operate on the same face (e.g., U followed by U' is not allowed).

    Parameters
    ----------
    length : int, optional
        Number of moves in the scramble, by default 20.
        Must be between 1 and 100 (inclusive).

    Returns
    -------
    list[Move]
        A list of ``length`` random Move objects.

    Raises
    ------
    ValueError
        If length is less than 1 or greater than 100.

    Examples
    --------
    >>> scramble = generate_scramble(20)
    >>> len(scramble)
    20
    >>> all(
    ...     scramble[i].value[0] != scramble[i+1].value[0]
    ...     for i in range(len(scramble) - 1)
    ... )
    True
    """
    if length < 1 or length > 100:
        raise ValueError(f"Scramble length must be between 1 and 100, got {length}")

    moves: list[Move] = []
    last_face: str | None = None

    for _ in range(length):
        # Pick a face different from the last move's face
        available_faces = [f for f in _FACES if f != last_face]
        chosen_face = random.choice(available_faces)
        # Pick a random move variant on that face (CW, CCW, or double)
        chosen_move = random.choice(_FACE_MOVES[chosen_face])
        moves.append(chosen_move)
        last_face = chosen_face

    return moves


def scramble_to_string(moves: list[Move]) -> str:
    """Convert a list of moves to standard notation string.

    Parameters
    ----------
    moves : list[Move]
        The move sequence to convert.

    Returns
    -------
    str
        Space-separated move notation, e.g. ``"U R' F2 D L2"``.

    Examples
    --------
    >>> from physics_modeling.rubiks_cube.moves import Move
    >>> scramble_to_string([Move.U, Move.R_PRIME, Move.F2])
    "U R' F2"
    """
    return " ".join(m.value for m in moves)
