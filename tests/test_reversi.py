"""
Tests for the group implementation
"""

import pytest

from reversi import Reversi


def verify_size(expected: int) -> bool:
    """
    Test whether we can correctly create a (non-Othello) 4x4 game
    """
    #reversi = Reversi(side=4, players=2, othello=False)
    pass


def test_create_1():
    """
    Test whether we can correctly create a (non-Othello) 4x4 game
    """
    reversi = Reversi(side=4, players=2, othello=False)

    grid = reversi.grid

    assert len(grid) == 4

    for r, row in enumerate(grid):
        assert len(row) == 4
        for c, value in enumerate(row):
            assert value is None, f"Expected grid[{r}][{c}] to be None but got {value}"

    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1

def test_create_2():
    """
    Test whether we can correctly create an Othello 6x6 game
    """
    reversi = Reversi(side=6, players=2, othello=True)

    grid = reversi.grid

    assert len(grid) == 6

    othello_pos = [(2, 2, 2), (2, 3, 1), (3, 2, 1), (3, 3, 2)]

    for r, row in enumerate(grid):
        assert len(row) == 6
        for c, value in enumerate(row):
            if r in (2, 3) and c in (2, 3):
                continue
            assert value is None, f"Expected grid[{r}][{c}] to be None but got {value}"

    for r, c, player in othello_pos:
        assert (
            grid[r][c] == player
        ), f"Expected grid[{r}][{c}] to be {player} but got {grid[r][c]}"


    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1


def test_othello_size():
    """
    Test whether we can correctly create an 8x8 Othello game
    """
    reversi = Reversi(side=8, players=2, othello=True)

    assert reversi.size == 8



def test_othello_players():
    """
    Test whether we can correctly create a game with 2 players
    """
    reversi = Reversi(side=8, players=2, othello=True)

    assert reversi.num_players == 2

    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1


def test_othello_turn():
    """
    Test whether we can correctly create a game on turn 1
    """
    reversi = Reversi(side=8, players=2, othello=True)

    assert reversi.turn == 1


def test_piece_at_1():
    """
    Test that piece_at returns correct values
    in an 8x8 Othello game with no moves made yet
    """
    reversi = Reversi(side=8, players=2, othello=True)

    othello_pos = [(3, 3, 2), (3, 4, 1), (4, 3, 1), (4, 4, 2)]


    for r, c, expected_piece in othello_pos:
        piece = reversi.piece_at((r, c))
        assert (
            piece == expected_piece
        ), f"Expected piece_at(({r},{c})) to return {expected_piece} but got {piece}"


def test_piece_at_2():
    """
    Test that calling piece_at with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        reversi.piece_at((-1, -1))

    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        reversi.piece_at((8, 8))


def test_available_moves_1():
    """
    Test that available_moves returns correct values
    in an 8x8 Othello game with no moves made yet
    """
    reversi = Reversi(side=8, players=2, othello=True)

    expected = {
        (2, 3),
        (3, 2),
        (5, 4),
        (4, 5),
    }

    assert set(reversi.available_moves) == expected


def test_legal_move_1():
    """
    Test that legal_move returns correct values
    in an 8x8 Othello game with no moves made yet
    """

    reversi = Reversi(side=8, players=2, othello=True)

    legal = {
        (2, 3),
        (3, 2),
        (5, 4),
        (4, 5),
    }

    for r in range(8):
        for c in range(8):
            if (r, c) in legal:
                assert reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"


def test_legal_move_2():
    """
    Test that calling legal_move with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        reversi.piece_at((-1, -1))

    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        reversi.piece_at((8, 8))


def test_apply_move_1():
    """
    Test making one move
    """

    reversi = Reversi(side=8, players=2, othello=True)
    reversi.apply_move((5, 4))

    assert reversi.piece_at((5, 4)) == 1
    assert reversi.turn == 2
    assert not reversi.done
    assert reversi.outcome == []

    assert reversi.legal_move((5, 3))
    assert reversi.legal_move((3, 5))
    assert reversi.legal_move((5, 5))


def test_apply_move_2():
    """
    Test making two moves
    """

    reversi = Reversi(side=8, players=2, othello=True)
    reversi.apply_move((3, 5))
    reversi.apply_move((4, 5))

    assert reversi.legal_move((2, 6))
    assert reversi.legal_move((3, 6))
    assert reversi.legal_move((4, 6))
    assert reversi.legal_move((5, 6))

    assert reversi.piece_at((3, 5)) == 1
    assert reversi.piece_at((4, 5)) == 2
    assert reversi.turn == 1
    assert not reversi.done
    assert reversi.outcome == []


def test_apply_move_3():
    """
    Test making three moves
    """

    reversi = Reversi(side=8, players=2, othello=True)
    reversi.apply_move((3, 5))
    reversi.apply_move((4, 5))
    reversi.apply_move((3, 6))

    assert reversi.legal_move((2, 6))
    assert reversi.legal_move((4, 6))
    assert reversi.legal_move((5, 6))
    assert reversi.legal_move((2, 7))
    assert reversi.legal_move((3, 7))
    assert reversi.legal_move((4, 7))

    assert reversi.piece_at((3, 5)) == 1
    assert reversi.piece_at((4, 5)) == 2
    assert reversi.piece_at((3, 6)) == 1
    assert reversi.turn == 2
    assert not reversi.done
    assert reversi.outcome == []


def test_apply_move_4():
    """
    Test that calling apply_move with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        reversi.apply_move((-1, -1))

    with pytest.raises(ValueError):
        reversi = Reversi(side=7, players=2, othello=True)
        reversi.apply_move((8, 8))


def test_winner_1():
    """
    Test that the game ends correctly in a single move
    (with one winner)
    """

    reversi = Reversi(side=4, players=2, othello=True)
    reversi.apply_move((3, 1))
    reversi.apply_move((3, 0))
    reversi.apply_move((2, 0))
    reversi.apply_move((1, 0))
    reversi.apply_move((0, 0))
    reversi.apply_move((0, 2))
    reversi.apply_move((0, 3))
    reversi.apply_move((3, 3))
    reversi.apply_move((0, 1))
    reversi.apply_move((3, 2))
    reversi.apply_move((1, 3))
    reversi.apply_move((2, 3))

    assert reversi.piece_at((0,0)) == 1
    assert reversi.piece_at(0,1) == 1
    assert reversi.piece_at(0,2) == 1
    assert reversi.piece_at(0,3) == 1
    assert reversi.piece_at(1,2) == 1
    assert reversi.piece_at(1,3) == 1
    assert reversi.piece_at(2,3) == 1

    assert reversi.piece_at(1,0) == 2
    assert reversi.piece_at(1,2) == 2
    assert reversi.piece_at(2,0) == 2
    assert reversi.piece_at(2,0) == 2
    assert reversi.piece_at(2,1) == 2
    assert reversi.piece_at(2,2) == 2
    assert reversi.piece_at(3,0) == 2
    assert reversi.piece_at(3,1) == 2
    assert reversi.piece_at(3,2) == 2
    assert reversi.piece_at(3,3) == 2

    assert reversi.done
    assert reversi.outcome == [2]


def test_othello_size_6x6():
    """
    Test whether we can correctly create an 8x8 Othello game
    """
    reversi = Reversi(side=6, players=2, othello=True)

    assert reversi.size == 6


def test_othello_players_6x6():
    """
    Test whether we can correctly create a game with 2 players
    """
    reversi = Reversi(side=6, players=2, othello=True)

    assert reversi.num_players == 2



def test_othello_turn_6x6():
    """
    Test whether we can correctly create a game on turn 1
    """
    reversi = Reversi(side=6, players=2, othello=True)

    assert reversi.turn == 1


def test_piece_at_6x6():
    """
    Test that piece_at returns correct values
    in an 6x6 Othello game with no moves made yet
    """
    reversi = Reversi(side=6, players=2, othello=True)

    othello_pos = [(2, 2, 2), (2, 3, 1), (3, 2, 1), (3, 3, 2)]


    for r, c, expected_piece in othello_pos:
        piece = reversi.piece_at((r, c))
        assert (
            piece == expected_piece
        ), f"Expected piece_at(({r},{c})) to return {expected_piece} but got {piece}"


def test_available_moves_6x6():
    """
    Test that available_moves returns correct values
    in an 6x6 Othello game with no moves made yet
    """
    reversi = Reversi(side=6, players=2, othello=True)

    expected = {
        (1, 2),
        (2, 1),
        (4, 3),
        (3, 4),
    }

    assert set(reversi.available_moves) == expected


def test_legal_move_6x6():
    """
    Test that legal_move returns correct values
    in an 6x6 Othello game with no moves made yet
    """

    reversi = Reversi(side=6, players=2, othello=True)

    legal = {
        (1, 2),
        (2, 1),
        (4, 3),
        (3, 4),
    }

    for r in range(6):
        for c in range(6):
            if (r, c) in legal:
                assert reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"


def test_othello_size_20x20():
    """
    Test whether we can correctly create an 20x20 Othello game
    """
    reversi = Reversi(side=20, players=2, othello=True)

    assert reversi.size == 20


def test_othello_players_20x20():
    """
    Test whether we can correctly create a game with 2 players
    """
    reversi = Reversi(side=20, players=2, othello=True)

    assert reversi.num_players == 2



def test_othello_turn_20x20():
    """
    Test whether we can correctly create a game on turn 1
    """
    reversi = Reversi(side=20, players=2, othello=True)

    assert reversi.turn == 1


def test_piece_at_20x20():
    """
    Test that piece_at returns correct values
    in an 6x6 Othello game with no moves made yet
    """
    reversi = Reversi(side=20, players=2, othello=True)

    othello_pos = [(9, 9, 2), (9, 10, 1), (10, 9, 1), (10, 10, 2)]


    for r, c, expected_piece in othello_pos:
        piece = reversi.piece_at((r, c))
        assert (
            piece == expected_piece
        ), f"Expected piece_at(({r},{c})) to return {expected_piece} but got {piece}"


def test_available_moves_20x20():
    """
    Test that available_moves returns correct values
    in an 20x20 Othello game with no moves made yet
    """
    reversi = Reversi(side=20, players=2, othello=True)

    expected = {
        (8, 9),
        (9, 8),
        (11, 10),
        (10, 11),
    }

    assert set(reversi.available_moves) == expected


def test_legal_move_20x20():
    """
    Test that legal_move returns correct values
    in an 20x20 Othello game with no moves made yet
    """

    reversi = Reversi(side=20, players=2, othello=True)

    legal = {
        (8, 9),
        (9, 8),
        (11, 10),
        (10, 11),
    }

    for r in range(6):
        for c in range(6):
            if (r, c) in legal:
                assert reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"

    """
    Test that available_moves returns correct values
    in an 20x20 Othello game with no moves made yet
    """
    reversi = Reversi(side=20, players=2, othello=True)

    expected = {
        (8, 9),
        (9, 8),
        (11, 10),
        (10, 11),
    }

    assert set(reversi.available_moves) == expected


def test_available_moves_8x8_non_othello():
    """
    Test that available_moves returns correct values
    in an 8x8 Reversi game with no moves made yet
    """
    reversi = Reversi(side=8, players=2, othello=False)

    assert reversi.first_two
    expected = {
        (3, 3),
        (3, 4),
        (4, 3),
        (4, 4)
    }

    assert set(reversi.available_moves) == expected

def test_legal_move_8x8_non_othello():
    """
    Test that legal_move returns correct values
    in an 8x8 Reversi game with no moves made yet
    """

    reversi = Reversi(side=8, players=2, othello=False)

    legal = {
        (3, 3),
        (3, 4),
        (4, 3),
        (4, 4)
    }

    for r in range(6):
        for c in range(6):
            if (r, c) in legal:
                assert reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is a legal move, but legal_move returned False"
            else:
                assert not reversi.legal_move(
                    (r, c)
                ), f"{(r,c)} is not a legal move, but legal_move returned True"
