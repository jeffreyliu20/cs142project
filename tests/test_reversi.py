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

    print (reversi.available_moves)

    assert reversi.legal_move((5, 2))
    assert reversi.legal_move((5, 3))
    assert reversi.legal_move((5, 4))
    assert reversi.legal_move((5, 5))
    assert reversi.legal_move((5, 6))

    assert reversi.piece_at((3, 3)) == 1
    assert reversi.piece_at((3, 4)) == 1
    assert reversi.piece_at((3, 5)) == 1
    assert reversi.piece_at((4, 3)) == 2
    assert reversi.piece_at((4, 4)) == 2
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

    expected = [[(0,0),(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
                [(1,0),(1,2),(2,0),(2,1),(2,2),(3,0),(3,1),(3,2),(3,3)]]

    for player, piece_list in enumerate(expected):
        for piece in piece_list:
            assert reversi.piece_at(piece) == player + 1


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


def test_available_moves_8x8_non_othello_after4():
    """
    Test that available_moves returns correct values
    in an 8x8 Reversi game with 4 moves made
    """
    reversi = Reversi(side=8, players=2, othello=False)

    assert reversi.first_two
    reversi.apply_move((3,3))
    reversi.apply_move((3,4))
    reversi.apply_move((4,4))
    reversi.apply_move((4,3))
    expected = {
        (2, 4),
        (4, 2),
        (5, 3),
        (3, 5),
    }

    assert set(reversi.available_moves) == expected

def test_legal_move_8x8_non_othello_after4():
    """
    Test that legal_move returns correct values
    in an 8x8 Reversi game with 4 moves made
    """

    reversi = Reversi(side=8, players=2, othello=False)


    reversi.apply_move((3,3))
    reversi.apply_move((3,4))
    reversi.apply_move((4,4))
    reversi.apply_move((4,3))

    legal = {
        (2, 4),
        (4, 2),
        (5, 3),
        (3, 5),
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


def test_available_moves_9x9_non_othello():
    """
    Test that available_moves returns correct values
    in an 9x9 Reversi game with no moves made yet
    """
    reversi = Reversi(side=9, players=3, othello=False)

    assert reversi.first_two
    expected = {
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 3),
        (5, 4),
        (5, 5)
    }

    assert set(reversi.available_moves) == expected

def test_legal_move_9x9_non_othello():
    """
    Test that legal_move returns correct values
    in an 9x9 Reversi game with no moves made yet
    """

    reversi = Reversi(side=9, players=3, othello=False)

    legal = {
        (3, 3),
        (3, 4),
        (3, 5),
        (4, 3),
        (4, 4),
        (4, 5),
        (5, 3),
        (5, 4),
        (5, 5)
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


def test_available_moves_9x9_non_othello_after9():
    """
    Test that available_moves returns correct values
    in an 9x9 Reversi game with 9 moves made 
    """
    reversi = Reversi(side=9, players=3, othello=False)

    assert reversi.first_two
    reversi.apply_move((3,3))
    reversi.apply_move((3,4))
    reversi.apply_move((4,4))
    reversi.apply_move((4,3))
    reversi.apply_move((5,3))
    reversi.apply_move((4,5))
    reversi.apply_move((5,5))
    reversi.apply_move((5,3))
    reversi.apply_move((5,4))
    expected = {
        (2, 2),
        (2, 5),
        (3, 6),
        (4, 6),
        (5, 2),
        (6, 3),
        (6, 6)
    }

    assert set(reversi.available_moves) == expected

def test_legal_move_9x9_non_othello_after9():
    """
    Test that legal_move returns correct values
    in an 9x9 Reversi game with 9 moves made
    """

    reversi = Reversi(side=9, players=3, othello=False)


    reversi.apply_move((3,3))
    reversi.apply_move((3,4))
    reversi.apply_move((4,4))
    reversi.apply_move((4,3))
    reversi.apply_move((5,3))
    reversi.apply_move((4,5))
    reversi.apply_move((5,5))
    reversi.apply_move((5,3))
    reversi.apply_move((5,4))

    legal = {
        (2, 2),
        (2, 5),
        (3, 6),
        (4, 6),
        (5, 2),
        (6, 3),
        (6, 6)
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


def test_winner_2():
    """
    Test that the game ends correctly in a 5x5 game with 3 players
    (with one winner)
    """

    reversi = Reversi(side=5, players=3, othello=False)
    reversi.apply_move((1, 1))
    reversi.apply_move((3, 1))
    reversi.apply_move((2, 2))
    reversi.apply_move((1, 3))
    reversi.apply_move((1, 2))
    reversi.apply_move((2, 3))
    reversi.apply_move((3, 3))
    reversi.apply_move((2, 1))
    reversi.apply_move((3, 2))
    reversi.apply_move((3, 0))
    reversi.apply_move((2, 4)) #player 3 eliminated, turn skip for rest of game
    reversi.apply_move((0, 2))
    reversi.apply_move((4, 1))
    reversi.apply_move((2, 0))
    reversi.apply_move((0, 1))
    reversi.apply_move((4, 2))
    reversi.apply_move((0, 4))
    reversi.apply_move((1, 4))
    reversi.apply_move((3, 4))
    reversi.apply_move((0, 0))
    reversi.apply_move((0, 3))
    reversi.apply_move((1, 0))
    reversi.apply_move((4, 0))
    reversi.apply_move((4, 4))
    reversi.apply_move((4, 3))

    expected = [[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(1,4),(2,0),(3,0),(4,4)],
                [(0,3),(0,4),(1,3),(2,1),(2,2),(2,3),(2,4),(3,1),(3,2),(3,3),(3,4),(4,0),(4,1),(4,2),(4,3)]]

    for player, piece_list in enumerate(expected):
        for piece in piece_list:
            assert reversi.piece_at(piece) == player + 1


    assert reversi.done
    assert reversi.outcome == [2]


def test_load_game_1():
    """
    Test that the game loads correctly in a 8x8 Othello game
    """

    reversi = Reversi(side=8, players=2, othello=True)

    grid = [[None for j in range(8)] for i in range(8)]
    grid [3][3] = 2
    grid [3][4] = 2
    grid [3][2] = 1
    grid [4][3] = 1
    grid [4][4] = 1

    reversi.load_game(2, grid)

    assert reversi.turn == 2
    assert reversi.piece_at((3,3)) == 2
    assert reversi.piece_at((3,4)) == 2
    assert reversi.piece_at((3,2)) == 1
    assert reversi.piece_at((4,3)) == 1
    assert reversi.piece_at((4,4)) == 1


def test_load_game_2():
    """
    Test that the game loads incorrectly with turn error
    """
    grid = [[None for j in range(8)] for i in range(8)]
    grid [3][3] = 2
    grid [3][4] = 2
    grid [3][2] = 1
    grid [4][3] = 1
    grid [4][4] = 1

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.load_game(-1, grid)


def test_load_game_3():
    """
    Test that the game loads incorrectly with size error
    """
    grid = [[None for j in range(6)] for i in range(6)]
    grid [3][3] = 2
    grid [3][4] = 2
    grid [3][2] = 1
    grid [4][3] = 1
    grid [4][4] = 1

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.load_game(2, grid)


def test_load_game_4():
    """
    Test that the game loads incorrectly with grid player error
    """
    grid = [[None for j in range(6)] for i in range(6)]
    grid [3][3] = 2
    grid [3][4] = 4
    grid [3][2] = 3
    grid [4][3] = 1
    grid [4][4] = 1

    with pytest.raises(ValueError):
        reversi = Reversi(side=8, players=2, othello=True)
        reversi.load_game(2, grid)


def test_simulate_move_1():
    """
    Test simulating a move that doesn't end the game
    """

    reversi = Reversi(side=8, players=2, othello=True)

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

    

def test_simulate_move_3():
    """
    Test simulating a move that doesn't end the game
    """

    reversi = Reversi(side=8, players=2, othello=True)

    grid_orig = reversi.grid

    future_reversi = reversi.simulate_moves([(3, 5), (2,5)])

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
