"""
Mock implementations of ReversiBase.

We provide a ReversiStub implementation, and you must
implement a ReversiMock implementation.
"""
from typing import List, Tuple, Optional
from copy import deepcopy

from reversi import ReversiBase, BoardGridType, ListMovesType

class Board:
    """
    Class to contain a board.
    The board is a grid where each square in the grid is mapped to "None" if no
    move has been made there or a piece otherwise.
    """

    _grid: BoardGridType

    def __init__(self, side: int):
        self._grid = [[None]*side for _ in range(side)]

    @property
    def grid(self) -> BoardGridType:
        """
        Returns the current state of the grid.
        Parameters:
            none beyond self
        Returns: the grid
        """
        return self._grid
    
    def add_piece(self, player: int, pos: Tuple[int]) -> None:
        """
        Adds a piece to a specified position on the board
        Parameters:
            player [int]: the integer associated with the player adding the piece
            pos [Tuple[int]]: coordinates within the grid
        Returns: nothing
        """
        r, c = pos
        self._grid[r][c] = Piece(player, pos)

    def get_piece(self, pos: Tuple[int]) -> Optional["Piece"]:
        """
        Finds the piece at a specified point in the board
        Parameters:
            pos[Tuple[int]]: coordinates within the grid
        Returns: a piece if there is one at the coordinates, None if not
        """
        r, c = pos
        return self._grid[r][c]
    

class Piece:
    """
    Class to contain a piece
    """
    def __init__(self, player: int, pos: Tuple[int]):
        self._player = player
        self._pos = pos

    @property
    def player(self):
        """
        Which player played this piece
        Paramters: None beyond self
        Returns [int]: player name
        """
        return self._player
    
    @property
    def pos(self):
        """
        Where on its board the piece is located
        """
        return self._pos


class ReversiStub(ReversiBase):
    """
    Stub implementation of ReversiBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.
    - The board is always initialized with four pieces in the four corners
      of the board. Player 1 has pieces in the northeast and southwest
      corners of the board, and Player 2 has pieces in the southeast and
      northwest corners of the board.
    - All moves are legal, even if there is already a piece in a given position.
    - The game ends after four moves. Whatever player has a piece in position
      (0,1) wins. If there is no piece in that position, the game ends in a tie.
    - It does not validate board positions. If a method
      is called with a position outside the board, the method will likely cause
      an exception.
    - It does not implement the ``load_game`` or ``simulate_moves`` method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The stub implementation "
                             "only supports two players")

        super().__init__(side, players, othello)

        self._grid = [[None]*side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        return self._num_moves == 4

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [0, 1]
        else:
            return [self._grid[0][1]]

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        self._grid[r][c] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        raise NotImplementedError()

