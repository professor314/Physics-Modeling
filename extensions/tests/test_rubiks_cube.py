"""Tests for Rubik's cube state, moves, and validation."""

from __future__ import annotations

import numpy as np
import pytest

from physics_modeling.rubiks_cube import (
    CubeState,
    Move,
    apply_move,
    apply_sequence,
    inverse_move,
    inverse_sequence,
    is_valid_state,
    parse_move_string,
)


class TestCubeState:
    """Tests for CubeState class."""

    def test_solved_state_shape(self) -> None:
        cube = CubeState.solved()
        assert cube.facelets.shape == (6, 3, 3)

    def test_solved_state_is_solved(self) -> None:
        cube = CubeState.solved()
        assert cube.is_solved()

    def test_solved_state_face_values(self) -> None:
        cube = CubeState.solved()
        for i in range(6):
            assert np.all(cube.facelets[i] == i)

    def test_to_kociemba_string_solved(self) -> None:
        cube = CubeState.solved()
        s = cube.to_kociemba_string()
        assert len(s) == 54
        # 9 chars per face in order U R F D L B
        expected = "U" * 9 + "R" * 9 + "F" * 9 + "D" * 9 + "L" * 9 + "B" * 9
        assert s == expected

    def test_from_kociemba_string_solved(self) -> None:
        s = "U" * 9 + "R" * 9 + "F" * 9 + "D" * 9 + "L" * 9 + "B" * 9
        cube = CubeState.from_kociemba_string(s)
        assert cube.is_solved()

    def test_kociemba_roundtrip(self) -> None:
        cube = CubeState.solved()
        # Apply some moves, convert to string, parse back
        scrambled = apply_sequence(cube, [Move.U, Move.R, Move.F])
        s = scrambled.to_kociemba_string()
        restored = CubeState.from_kociemba_string(s)
        assert restored == scrambled

    def test_from_kociemba_string_invalid_length(self) -> None:
        with pytest.raises(ValueError, match="54 characters"):
            CubeState.from_kociemba_string("UUU")

    def test_from_kociemba_string_invalid_char(self) -> None:
        with pytest.raises(ValueError, match="Invalid character"):
            CubeState.from_kociemba_string("X" * 54)

    def test_immutability(self) -> None:
        cube = CubeState.solved()
        with pytest.raises((ValueError, TypeError)):
            cube.facelets[0, 0, 0] = 5

    def test_equality(self) -> None:
        a = CubeState.solved()
        b = CubeState.solved()
        assert a == b

    def test_hash_consistency(self) -> None:
        a = CubeState.solved()
        b = CubeState.solved()
        assert hash(a) == hash(b)


class TestMoves:
    """Tests for move application."""

    def test_u_then_u_prime_is_identity(self) -> None:
        cube = CubeState.solved()
        result = apply_sequence(cube, [Move.U, Move.U_PRIME])
        assert result.is_solved()

    def test_d_then_d_prime_is_identity(self) -> None:
        cube = CubeState.solved()
        result = apply_sequence(cube, [Move.D, Move.D_PRIME])
        assert result.is_solved()

    def test_l_then_l_prime_is_identity(self) -> None:
        cube = CubeState.solved()
        result = apply_sequence(cube, [Move.L, Move.L_PRIME])
        assert result.is_solved()

    def test_r_then_r_prime_is_identity(self) -> None:
        cube = CubeState.solved()
        result = apply_sequence(cube, [Move.R, Move.R_PRIME])
        assert result.is_solved()

    def test_f_then_f_prime_is_identity(self) -> None:
        cube = CubeState.solved()
        result = apply_sequence(cube, [Move.F, Move.F_PRIME])
        assert result.is_solved()

    def test_b_then_b_prime_is_identity(self) -> None:
        cube = CubeState.solved()
        result = apply_sequence(cube, [Move.B, Move.B_PRIME])
        assert result.is_solved()

    def test_u4_is_identity(self) -> None:
        """Applying U four times should return to solved state."""
        cube = CubeState.solved()
        result = apply_sequence(cube, [Move.U] * 4)
        assert result.is_solved()

    def test_all_faces_four_times_identity(self) -> None:
        """X^4 = identity for all face moves."""
        cube = CubeState.solved()
        for move in [Move.U, Move.D, Move.L, Move.R, Move.F, Move.B]:
            result = apply_sequence(cube, [move] * 4)
            assert result.is_solved(), f"{move.value}^4 != identity"

    def test_u2_is_u_applied_twice(self) -> None:
        cube = CubeState.solved()
        result_u2 = apply_move(cube, Move.U2)
        result_uu = apply_sequence(cube, [Move.U, Move.U])
        assert result_u2 == result_uu

    def test_u_prime_is_u_applied_three_times(self) -> None:
        cube = CubeState.solved()
        result_prime = apply_move(cube, Move.U_PRIME)
        result_three = apply_sequence(cube, [Move.U, Move.U, Move.U])
        assert result_prime == result_three

    def test_move_changes_state(self) -> None:
        cube = CubeState.solved()
        moved = apply_move(cube, Move.U)
        assert not moved.is_solved()

    def test_superflip_is_valid(self) -> None:
        """A well-known sequence that flips all edges."""
        cube = CubeState.solved()
        # Apply a known sequence and verify it produces a valid state
        moves = parse_move_string("U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2")
        result = apply_sequence(cube, moves)
        assert is_valid_state(result)

    def test_inverse_sequence_restores(self) -> None:
        """Applying a sequence then its inverse restores the original state."""
        cube = CubeState.solved()
        moves = [Move.U, Move.R, Move.F, Move.D, Move.L, Move.B]
        scrambled = apply_sequence(cube, moves)
        inv = inverse_sequence(moves)
        restored = apply_sequence(scrambled, inv)
        assert restored.is_solved()


class TestInverseMove:
    """Tests for inverse_move function."""

    def test_u_inverse(self) -> None:
        assert inverse_move(Move.U) == Move.U_PRIME

    def test_u_prime_inverse(self) -> None:
        assert inverse_move(Move.U_PRIME) == Move.U

    def test_u2_self_inverse(self) -> None:
        assert inverse_move(Move.U2) == Move.U2

    def test_all_double_moves_self_inverse(self) -> None:
        for move in [Move.U2, Move.D2, Move.L2, Move.R2, Move.F2, Move.B2]:
            assert inverse_move(move) == move


class TestParseMoveString:
    """Tests for parse_move_string function."""

    def test_simple_moves(self) -> None:
        result = parse_move_string("U R F")
        assert result == [Move.U, Move.R, Move.F]

    def test_prime_moves(self) -> None:
        result = parse_move_string("U' R' F'")
        assert result == [Move.U_PRIME, Move.R_PRIME, Move.F_PRIME]

    def test_double_moves(self) -> None:
        result = parse_move_string("U2 R2 F2")
        assert result == [Move.U2, Move.R2, Move.F2]

    def test_empty_string(self) -> None:
        assert parse_move_string("") == []
        assert parse_move_string("   ") == []

    def test_invalid_move_raises(self) -> None:
        with pytest.raises(ValueError, match="Unrecognized"):
            parse_move_string("X")


class TestValidation:
    """Tests for is_valid_state function."""

    def test_solved_is_valid(self) -> None:
        assert is_valid_state(CubeState.solved())

    def test_single_move_is_valid(self) -> None:
        cube = CubeState.solved()
        for move in Move:
            moved = apply_move(cube, move)
            assert is_valid_state(moved), f"State after {move.value} is invalid"

    def test_scrambled_is_valid(self) -> None:
        cube = CubeState.solved()
        moves = parse_move_string("U R' F2 D L' B2 U2 R F D'")
        scrambled = apply_sequence(cube, moves)
        assert is_valid_state(scrambled)

    def test_wrong_color_count_is_invalid(self) -> None:
        """Swapping two stickers from different faces creates invalid state."""
        facelets = np.zeros((6, 3, 3), dtype=np.int8)
        for i in range(6):
            facelets[i] = i
        # Swap one sticker to break color count
        facelets[0, 0, 0] = 1  # Now face 0 has 8 of color 0 and 1 of color 1
        facelets[1, 0, 0] = 0  # And face 1 has 8 of color 1 and 1 of color 0
        # Color counts are still 9 each, but this may violate orientation
        cube = CubeState(facelets=facelets)
        # A single swap of two corner stickers creates an impossible state
        assert not is_valid_state(cube)

    def test_centers_check(self) -> None:
        """Centers must be one per face (each center is unique color)."""
        # In a valid cube, center facelets are always the face index
        cube = CubeState.solved()
        for i in range(6):
            assert cube.facelets[i, 1, 1] == i
