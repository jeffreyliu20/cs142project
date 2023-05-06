"""
Mock implementations of ReversiBase.

We provide a ReversiStub implementation, and you must
implement a ReversiMock implementation.
"""
from typing import List, Tuple, Optional
from copy import deepcopy

from reversi import ReversiBase, BoardGridType, ListMovesType

DIRECTION_LIST = ((1, 1), (0, 1), (1, 0), (-1, -1), (0, -1), (-1, 0), (1, -1),
                  (-1, 1))

class Board:
    """
    Class to contain a board.
    The board is a grid where each square in the grid is mapped to "None" if no
    move has been made there or a piece otherwise.
    """

    _grid: BoardGridType
    _pieces: List["Piece"]
    _edgepieces: List["Piece"]

    def __init__(self, side: int):
        self._grid = [[None]*side for _ in range(side)]
        self._pieces = []
        self._edgepieces = []


    @property
    def grid(self) -> BoardGridType:
        """
        Returns a copy of the board's grid
        
        Parameters: none beyond self
        Returns[BoardGridType]: a grid
        """
        return self._grid
    
    @property
    def pieces(self) -> List["Piece"]:
        """
        Returns a copy of the board's piece list
        
        Parameters: none beyond self
        Returns[List[Piece]]: a list of the pieces in the board
        """
        return self._pieces
    
    @property
    def edge_pieces(self) -> List["Piece"]:
        """
        Returns a list of the pieces on a board that are not completely
        surrounded by other pieces
        
        Parameters: none beyond self
        Returns[List[Piece]]: a list of pieces on the edge of the board
        """
        self.update_edge_pieces()
        return self._edgepieces
    

    def update_edge_pieces(self) -> None:
        """
        Removes pieces that are not on the edge from the list of edge pieces
        
        Parameters: none beyond self
        Returns: None
        """
        final_list = self._edgepieces
        for piece in self._edgepieces:
            if len(piece.adjacent) == 8:
                final_list.remove(piece)
        self._edgepieces = final_list
    
    def add_piece(self, player: int, pos: Tuple[int, int]) -> None:
        """
        Adds a piece to a specified position on the board
        Parameters:
            player [int]: the integer associated with the player adding the piece
            pos [Tuple[int]]: coordinates within the grid
        Returns: nothing
        """
        r, c = pos
        new_piece = Piece(player, pos)
        for direction in DIRECTION_LIST:
            y, x = direction
            if self._grid[r + y][c + x]:
                new_piece.adjacent[r + y][c + x] = self.get_piece((r + y, c + x))
                self.get_piece((r + y, c + x)).adjacent[r][c] = new_piece
                
        self._grid[r][c] = player
        self._pieces.append(new_piece)
        self._edgepieces.append(new_piece)
    
    def update_piece(self, pos: Tuple[int, int], player: int):
        """
        Changes the piece at a given point in the grid to a different player
        """
        r, c = pos
        if self._grid[r][c]:
            self._grid[r][c] = player
        else:
            print("No piece at that position")

    def get_piece(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Finds the piece at a specified point in the board
        Parameters:
            pos[Tuple[int]]: coordinates within the grid
        Returns: a piece if there is one at the coordinates, None if not
        """
        r, c = pos
        return self._grid[r][c]
    
    def update_grid(self, grid: BoardGridType) -> None:
        """
        Gets rid of the old version of the grid and loads a new one
        Parameters:
            grid[BoardGridType]: a valid grid with the same side length as the board
        Returns: nothing
        """
        if len(grid) != len(self._grid):
            raise ValueError("Cannot change board size")
        
        self._pieces = []
        for r, row in enumerate(grid):
            for c, square in enumerate(row):
                if square:
                    self._pieces.append(Piece(square, (r, c)))
        self._grid = grid
        

class Piece:
    """
    Class to contain a piece
    """

    _player: int
    _pos: Tuple[int, int]
    adjacent: dict[Tuple[int, int], "Piece"]

    def __init__(self, player: int, pos: Tuple[int, int]):
        self._player = player
        self._pos = pos
        self.adjacent = {}

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

class ReversiMock(ReversiBase):
    """
    Mock implementation of ReversiBase

    -Supports exactly two players and square boards of size 4x4 or more
    -Supports the Othello variant of Reversi
    -Raises a ValueError if the side length of the board is odd
    -Allows players to move at the northwest or southeast corners of the board,
      or at any empty space in the board adjacent to another piece
    -A player who places a piece at the northwest corner wins
    -A player who places a piece at the southwest corner causes the game to end
    -Supports simulating a single move with simulate_moves
    """
    
    _board: Board
    _turn: int
    _done: bool
    _outcome: List[int]

    def __init__(self, side: int, players: int, othello: bool):
        super().__init__(side, players, othello)

        if side <= players:
            raise ValueError("Side length must be greater than number of players.")
        if side % 2 == 1:
            raise ValueError("Odd side lengths not permitted.")
        
        self._board = Board(side)
        self._turn = 1
        self._done = False
        self._outcome = []

        if othello:
            self._board.add_piece(2, (side // 2 - 1, side // 2 - 1))
            self._board.add_piece(2, (side // 2, side // 2))
            self._board.add_piece(1, (side // 2, side // 2 - 1))
            self._board.add_piece(1, (side // 2 - 1, side // 2))

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players
    
    @property
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        return self._board.grid
    
    @property
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        return self._turn
    
    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        if self.done:
            return []
        move_list = [(0, 0), (self.size - 1, self.size - 1)]
        for piece in self._board.pieces:
            r, c = piece.pos
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if not (self.grid[r + x][c + y] or 
                            (r + x, c + y) in move_list):
                        move_list.append((r + x, c + y))
        return move_list
    
    @property
    def piece_list(self) -> List["Piece"]:
        """
        Returns the set of pieces associated with the board
        Parameters: none other than self
        Returns: set of pieces
        """
        return self._board.pieces

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        return self._done
    
    @property
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        return self._outcome
    
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        return self._board.get_piece(pos)
    
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        return pos in self.available_moves
    
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        self._board.add_piece(self.turn, pos)
        if pos == (0, 0):
            self.end_game([self.turn])
        if pos == (self.size - 1, self.size - 1):
            self.end_game([i for i in range(1, self.num_players + 1)])
        if self._turn < self.num_players:
            self._turn += 1
        else:
            self._turn = 1

    def end_game(self, player_list: List[int]) -> None:
        """
        Ends the game with the specified players designated as winners by adding
        Parameters:
            player_list [List[int]]: list of players who won the game (or tied
              for the win)
            
        Returns: nothing
        """
        self._done = True
        self._outcome = player_list
        self._turn = 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        if turn < 1 or turn > self.num_players:
            raise ValueError("No such player exists")
        
        new_side = len(grid)
        if new_side != self.size:
            raise ValueError("Input is not the same size as the current board")
        new_board = Board(new_side)
        new_board.update_grid(grid)
        for row in grid:
            for square in row:
                if square is not None and (square < 1 or 
                                           square > self.num_players):
                    raise ValueError("Grid contains invalid player")
        self._board = new_board
        self._done = False
        self._outcome = []
        

    def simulate_moves(self, moves: ListMovesType) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        if type(moves) == Tuple[int, int]:
            raise ValueError("Submitted a single tuple instead of a list")
        
        new_game = deepcopy(self)
        for move in moves:
            new_game.apply_move(move)
        return new_game
    

class ReversiBotMock(ReversiMock):
    """
    revision of the mock that allows for better bot testing
    """

    @property
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        return len(self._board.pieces) == self.size ** 2
    
    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        if self.done:
            return []
        move_list = []
        for piece in self._board.pieces:
            r, c = piece.pos
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if not (self.grid[r + x][c + y] or 
                            (r + x, c + y) in move_list):
                        move_list.append((r + x, c + y))
        return move_list
    
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        self._board.add_piece(self.turn, pos)
        for dir in DIRECTION_LIST:
            r, c = pos
            y, x = dir
            if self._board.grid[r + y][c + x]:
                self._board.update_piece((r + y, c + x), self.turn)
        if pos == (0, 0):
            self.end_game([self.turn])
        if pos == (self.size - 1, self.size - 1):
            self.end_game([i for i in range(1, self.num_players + 1)])
        if self._turn < self.num_players:
            self._turn += 1
        else:
            self._turn = 1