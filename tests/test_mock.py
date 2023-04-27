"""
Tests for the mock implementation
"""

import pytest

from mocks import ReversiMock


def test_create_1():
    """
    Test whether we can correctly create a (non-Othello) 8x8 game
    """
    reversi = ReversiMock(side=8, players=2, othello=False)

    grid = reversi.grid

    assert len(grid) == 8

    for r, row in enumerate(grid):
        assert len(row) == 8
        for c, value in enumerate(row):
            assert value is None, f"Expected grid[{r}][{c}] to be None but got {value}"

    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1


def test_create_2():
    """
    Test whether we can correctly create an 8x8 Othello game
    """
    reversi = ReversiMock(side=8, players=2, othello=True)

    grid = reversi.grid

    assert len(grid) == 8

    othello_pos = [(3, 3, 2), (3, 4, 1), (4, 3, 1), (4, 4, 2)]

    for r, row in enumerate(grid):
        assert len(row) == 8
        for c, value in enumerate(row):
            if r in (3, 4) and c in (3, 4):
                continue
            assert value is None, f"Expected grid[{r}][{c}] to be None but got {value}"

    for r, c, player in othello_pos:
        assert (
            grid[r][c] == player
        ), f"Expected grid[{r}][{c}] to be {player} but got {grid[r][c]}"

    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1


def test_create_3():
    """
    Test whether we can correctly create a 20x20 Othello game
    """
    reversi = ReversiMock(side=20, players=2, othello=True)

    grid = reversi.grid

    assert len(grid) == 20

    othello_pos = [(9, 9, 2), (9, 10, 1), (9, 10, 1), (10, 10, 2)]

    for r, row in enumerate(grid):
        assert len(row) == 20
        for c, value in enumerate(row):
            if r in (9, 10) and c in (9, 10):
                continue
            assert value is None, f"Expected grid[{r}][{c}] to be None but got {value}"

    for r, c, player in othello_pos:
        assert (
            grid[r][c] == player
        ), f"Expected grid[{r}][{c}] to be {player} but got {grid[r][c]}"

    assert not reversi.done
    assert reversi.outcome == []
    assert reversi.turn == 1


def test_parity():
    """
    Test that parity checking works
    """
    with pytest.raises(ValueError):
        reversi = ReversiMock(side=7, players=2, othello=True)


def test_piece_at_1():
    """
    Test that piece_at returns correct values
    in an 8x8 Othello game with no moves made yet
    """
    reversi = ReversiMock(side=8, players=2, othello=True)

    othello_pos = [(3, 3, 2), (3, 4, 1), (4, 3, 1), (4, 4, 2)]

    for r in range(8):
        for c in range(8):
            piece = reversi.piece_at((r, c))
            if r in (3, 4) and c in (3, 4):
                continue
            assert (
                piece is None
            ), f"Expected piece_at(({r},{c})) to return None but got {piece}"

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
        reversi = ReversiMock(side=7, players=2, othello=True)
        reversi.piece_at((-1, -1))

    with pytest.raises(ValueError):
        reversi = ReversiMock(side=7, players=2, othello=True)
        reversi.piece_at((8, 8))


def test_available_moves_1():
    """
    Test that available_moves returns correct values
    in an 8x8 Othello game with no moves made yet
    """
    reversi = ReversiMock(side=8, players=2, othello=True)

    expected = {
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 2),
        (3, 5),
        (4, 2),
        (4, 5),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
    }
    expected.add((0, 0))
    expected.add((7, 7))

    assert set(reversi.available_moves) == expected


def test_legal_move_1():
    """
    Test that legal_move returns correct values
    in an 8x8 Othello game with no moves made yet
    """

    reversi = ReversiMock(side=8, players=2, othello=True)

    legal = {
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 2),
        (3, 5),
        (4, 2),
        (4, 5),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
    }
    legal.add((0, 0))
    legal.add((7, 7))

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
        reversi = ReversiMock(side=7, players=2, othello=True)
        reversi.piece_at((-1, -1))

    with pytest.raises(ValueError):
        reversi = ReversiMock(side=7, players=2, othello=True)
        reversi.piece_at((8, 8))


def test_apply_move_1():
    """
    Test making one move
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
    reversi.apply_move((3, 5))

    assert reversi.legal_move((2, 6))
    assert reversi.legal_move((3, 6))
    assert reversi.legal_move((4, 6))

    assert reversi.piece_at((3, 5)) == 1
    assert reversi.turn == 2
    assert not reversi.done
    assert reversi.outcome == []


def test_apply_move_2():
    """
    Test making two moves
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
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

    reversi = ReversiMock(side=8, players=2, othello=True)
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
        reversi = ReversiMock(side=7, players=2, othello=True)
        reversi.apply_move((-1, -1))

    with pytest.raises(ValueError):
        reversi = ReversiMock(side=7, players=2, othello=True)
        reversi.apply_move((8, 8))


def test_winner_1():
    """
    Test that the game ends correctly in a single move
    (with one winner)
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
    reversi.apply_move((0, 0))

    assert reversi.done
    assert reversi.outcome == [1]


def test_winner_2():
    """
    Test that the game ends correctly in two moves
    (with one winner)
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
    reversi.apply_move((3, 5))
    reversi.apply_move((0, 0))

    assert reversi.done
    assert reversi.outcome == [2]


def test_winner_3():
    """
    Test that the game ends correctly in three moves
    (with one winner)
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
    reversi.apply_move((3, 5))
    reversi.apply_move((3, 6))
    reversi.apply_move((0, 0))

    assert reversi.done
    assert reversi.outcome == [1]


def test_tie_1():
    """
    Test that the game ends correctly in one move
    (ending in a tie)
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
    reversi.apply_move((7, 7))

    assert reversi.done
    assert sorted(reversi.outcome) == [1, 2]


def test_tie_2():
    """
    Test that the game ends correctly in two moves
    (ending in a tie)
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
    reversi.apply_move((3, 5))
    reversi.apply_move((7, 7))

    assert reversi.done
    assert sorted(reversi.outcome) == [1, 2]


def test_tie_3():
    """
    Test that the game ends correctly in three moves
    (ending in a tie)
    """

    reversi = ReversiMock(side=8, players=2, othello=True)
    reversi.apply_move((3, 5))
    reversi.apply_move((3, 6))
    reversi.apply_move((7, 7))

    assert reversi.done
    assert sorted(reversi.outcome) == [1, 2]


def test_simulate_move_1():
    """
    Test simulating a move that doesn't end the game
    """

    reversi = ReversiMock(side=8, players=2, othello=True)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(3, 5)])

    legal = {
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 2),
        (3, 5),
        (4, 2),
        (4, 5),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (0, 0),
        (7, 7),
    }

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned object corresponds to the
    # state after making the move.
    legal.remove((3, 5))
    legal.update({(2, 6), (3, 6), (4, 6)})
    assert future_reversi.grid != grid_orig
    assert future_reversi.turn == 2
    assert set(future_reversi.available_moves) == legal
    assert not future_reversi.done
    assert future_reversi.outcome == []


def test_simulate_move_2():
    """
    Test simulating a move that results in Player 1 winning
    """

    reversi = ReversiMock(side=8, players=2, othello=True)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(0, 0)])

    legal = {
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 2),
        (3, 5),
        (4, 2),
        (4, 5),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (0, 0),
        (7, 7),
    }

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert future_reversi.outcome == [1]


def test_simulate_move_3():
    """
    Test simulating a move that results in a tie
    """

    reversi = ReversiMock(side=8, players=2, othello=True)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(7, 7)])

    legal = {
        (2, 2),
        (2, 3),
        (2, 4),
        (2, 5),
        (3, 2),
        (3, 5),
        (4, 2),
        (4, 5),
        (5, 2),
        (5, 3),
        (5, 4),
        (5, 5),
        (0, 0),
        (7, 7),
    }

    # Check that the original game state has been preserved
    assert reversi.grid == grid_orig
    assert reversi.turn == 1
    assert set(reversi.available_moves) == legal
    assert not reversi.done
    assert reversi.outcome == []

    # Check that the returned values correspond to the
    # state after making the move.
    assert future_reversi.grid != grid_orig
    assert future_reversi.done
    assert sorted(future_reversi.outcome) == [1, 2]


def test_simulate_moves_4():
    """
    Test that calling simulate_moves with an invalid position
    raises a ValueError exception.
    """
    with pytest.raises(ValueError):
        reversi = ReversiMock(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(-1, -1)])

    with pytest.raises(ValueError):
        reversi = ReversiMock(side=7, players=2, othello=True)
        future_reversi = reversi.simulate_moves([(8, 8)])
