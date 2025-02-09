"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from copy import deepcopy
import numpy as np

BoardGridType = np.ndarray
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""

DIRECTION_LIST = ((1, 1), (0, 1), (1, 0), (-1, -1), (0, -1), (-1, 0), (1, -1),
                  (-1, 1))

class Board:
    """
    Class to contain a board.
    The board is a grid where each square in the grid is mapped to "None" if no
    move has been made there or a piece otherwise.
    """

    _grid: BoardGridType
    _pieces: List[List[Optional["Piece"]]]

    def __init__(self, side: int):
        self._grid = np.zeros((side, side), dtype=np.int_)
        self._pieces = [[None]*side for _ in range(side)]


    @property
    def grid(self) -> BoardGridType:
        """
        Returns a copy of the board's grid
        
        Parameters: none beyond self
        Returns[BoardGridType]: a grid
        """
        return self._grid
    
    @property
    def piece_grid(self) -> List[List[Optional["Piece"]]]:
        """
        Returns a copy of the board's piece grid
        
        Parameters: none beyond self
        Returns[List[List[Optional[Piece]]]]: a grid of pieces
        """
        return self._pieces
    
    @property
    def size(self) -> int:
        """
        Returns the side length of the grid
        
        Parameters: none beyond self
        Returns[int]: grid size
        """
        return len(self._grid)
    
    @property
    def pieces(self) -> List["Piece"]:
        """
        Returns a copy of the board's piece list
        
        Parameters: none beyond self
        Returns[List[Piece]]: a list of the pieces in the board
        """
        final_list = []
        for row in self._pieces:
            final_list += row
        return list(filter(lambda x: x is not None, final_list)) # type: ignore
    
    
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
                
        self._grid[r][c] = player
        self._pieces[r][c] = new_piece

    def remove_piece(self, pos: Tuple[int, int]) -> None:
        """
        Removes a piece from the board
        
        Parameters: none beyond self
        Returns: nothing
        """
        r, c = pos
        self._grid[r][c] = 0
        self._pieces[r][c] = None

    def update_piece(self, pos: Tuple[int, int], player: int) -> None:
        """
        Changes the piece at a given point in the grid to a different player
        """
        r, c = pos
        if self._grid[r][c]:
            self._grid[r][c] = player
            self._pieces[r][c].update_player(player) # type: ignore
        else:
            raise ValueError("No piece at that position")

    def get_piece(self, pos: Tuple[int, int]) -> Optional["Piece"]:
        """
        Finds the piece at a specified point in the board
        Parameters:
            pos[Tuple[int]]: coordinates within the grid
        Returns: piece at the coordinates
        """
        r, c = pos
        return self._pieces[r][c]
    
    def update_grid(self, grid: BoardGridType) -> None:
        """
        Gets rid of the old version of the grid and loads a new one
        Parameters:
            grid[BoardGridType]: a valid grid with the same side length as the board
        Returns: nothing
        """
        if len(grid) != len(self._grid):
            raise ValueError("Cannot change board size")
        
        self._pieces = [[None]*self.size for _ in range(self.size)]
        for r, row in enumerate(grid):
            for c, square in enumerate(row):
                if square:
                    self._pieces[r][c] = Piece(square, (r, c))
        self._grid = grid
        

class Piece:
    """
    Class to contain a piece
    """

    _player: int
    _pos: Tuple[int, int]

    def __init__(self, player: int, pos: Tuple[int, int]):
        self._player = player
        self._pos = pos

    @property
    def player(self) -> int:
        """
        Which player played this piece
        Paramters: None beyond self
        Returns [int]: player name
        """
        return self._player
    
    @property
    def pos(self) -> Tuple[int, int]:
        """
        Where on its board the piece is located
        """
        return self._pos
    
    def update_player(self, player: int) -> None:
        """
        Changes the player attribute to a new value
        
        Parameters:
            player[int]: a player in the game
            
        Returns: nothing
        """
        self._player = player

class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """

    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

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
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
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
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
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
        raise NotImplementedError


class Reversi(ReversiBase):

    _board: Board
    _turn: int
    _done: bool
    first_two: bool
    _outcome: List[int]
    _moves: List[Tuple[int, List[Tuple[Tuple[int, int], int]]]]

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        super().__init__(side, players, othello)

        if players > 2 and othello:
            raise ValueError("Othello is not allowed for more than 2 players.")
        if players < 2 or players > 9:
            raise ValueError("Player count must be 2-9.")
        if side < 3:
            raise ValueError("Side length must be greater than 3.")
        if side <= players:
            raise ValueError("Side length must be greater than number of players.")
        if side % 2 != players % 2:
            raise ValueError("Parity of players and side length must match.")
        
        self._board = Board(side)
        self._turn = 1
        self._done = False
        self._outcome = []
        self.first_two = True
        self._moves = []

        if othello:
            self._board.add_piece(2, (side // 2 - 1, side // 2 - 1))
            self._board.add_piece(2, (side // 2, side // 2))
            self._board.add_piece(1, (side // 2, side // 2 - 1))
            self._board.add_piece(1, (side // 2 - 1, side // 2))
            self.first_two = False

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
        Each entry can either be a positive integer (meaning there is a
        piece at that location for that player) or 0,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        return self._board.grid
    
    @property
    def pieces(self) -> List["Piece"]:
        """
        Returns a list of pieces on the board
        """
        return self._board.pieces

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

    def move_works(self, piece: "Piece", 
                    dir: Tuple[int, int],
                    rec: int=1) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinate of a move if there is one a certain direction
        adjacent to a certain piece
        
        Parameters:
            piece[Piece]: a piece on the board
            dir[Tuple[int, int]]: coordinates indicating a direction
            rec[int]: number of pieces that the function has checked
            
        Returns: coordinates if the move works, None if not
        """

        r, c = piece.pos
        y, x = dir

        # The following conditional first checks to make sure the piece is not 
        # on the edge of the board such that checking the space in or opposite 
        # the specified direction will produce an error. This code is built 
        # around checking whether pieces can be flipped, so it then checks to 
        # make sure the specified piece was placed by a different player than 
        # the one whose turn it is. Then, it checks to make sure there's a 
        # piece in the given direction, because if a player doesn't have a 
        # piece somewhere in the given direction, there's no way they can flip 
        # pieces. Finally, it makes sure that either a piece could be placed 
        # opposite the given direction (i.e. the given piece is on the end) 
        # or the function has already called itself.

        if  ((0 <= r - y < self.size and 0 <= c - x < self.size 
             and 0 <= r + y < self.size and 0 <= c + x < self.size)
             and self.grid[r][c] != self.turn and self.grid[r + y][c + x] 
             and (not self.grid[r - y][c - x] or rec > 1)):
            
            if self.grid[r + y][c + x] == self.turn:
                return (r - rec * y, c - rec * x)
            else:
                return self.move_works(self._board.piece_grid[r + y][c + x], # type: ignore
                                       dir, rec + 1) 
        else:
            return None
        
    def find_moves(self) -> dict[Tuple[int, int], List[Tuple[int, int]]]:
        """
        Finds all valid moves in a board
        
        Parameters: none beyond self
        Returns[dict]: A dictionary that maps a direction in which the move can 
        flip pieces to a list of possible moves dependent on that direction 
        (Note that the direction is not meaningful for the first two moves)
        """

        if self.done:
            return {}
        
        move_list = {}

        if self.first_two:
            center_filled = True
            middle = self.size // 2
            lower_bound = middle - self.num_players // 2
            upper_bound = middle + self.num_players // 2
            upper_bound += self.size % 2

            for r in range(lower_bound, upper_bound):
                for c in range(lower_bound, upper_bound):
                    if not self.grid[r][c]:
                        move_list[(r, c)] = [(r, c)]
                        center_filled = False
                
            if center_filled:
                self.first_two = False

        if not self.first_two:
            for piece in self.pieces:
                if piece.player != self.turn:
                    for dir in DIRECTION_LIST:

                        r, c = piece.pos
                        y, x = dir

                        if ((0 <= r - y < self.size and 0 <= c - x < self.size) 
                            and (not self.grid[r - y][c - x] and 
                            self.move_works(piece, dir))):
                            if dir in move_list:
                                move_list[dir].append((r - y, c - x))
                            else:
                                move_list[dir] = [(r - y, c - x)]

        return move_list
    
    @property
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        move_list = []

        for dir_moves in list(self.find_moves().values()):
            for move in dir_moves:
                if move not in move_list:
                    move_list.append(move)
            
        return move_list


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

    #
    # METHODS
    #

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
        r, c = pos
        if 0 <= r < self.size and 0 <= c < self.size:
            if self.grid[r][c]:
                return self.grid[r][c]
            return None
        else:
            raise ValueError("Specified position outside board")

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
        r, c = pos

        if 0 <= r < self.size and 0 <= c < self.size:
            return pos in self.available_moves
        else:
            raise ValueError("Specified position outside the board")

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
        r, c = pos
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise ValueError("Specified position outside board")
        
        move_dict = self.find_moves()
        
        self._board.add_piece(self.turn, pos)
        mv = [(pos, 0)]

        for dir in DIRECTION_LIST:
            if dir in move_dict:
                if pos in move_dict[dir]:

                    y, x = dir

                    new_y = r + y
                    new_x = c + x

                    while True:
                        if ((0 <= new_y < self.size 
                            and 0 <= new_x < self.size)
                            and self.grid[new_y][new_x] != self.turn):

                            mv.append(((new_y, new_x), 
                                        self.grid[new_y][new_x]))
                            self._board.update_piece((new_y, new_x), 
                                                        self.turn)
                            new_y += y
                            new_x += x
                        else:
                            break

        self._moves.append((self.turn, mv))   

        self.skip_turn()
        
        if (not self.first_two and len(np.unique(self.grid)) in [1, 2]
            or len(self.pieces) == self.size ** 2):
            self.end_game()
        
    def check_for_dead_moves(self) -> None:
        """
        Skips at least one turn. If the player to which it skips doesn't have 
        any moves to make, it will keep skipping turns until someone has a move 
        or the game is over.
        
        Parameters: None beyond self
        Returns: nothing
        """

        n = 0
        while True:
            if n == self.num_players:
                self.end_game()
                break

            if len(self.available_moves) == 0:
                n += 1
            else:
                break

            self.skip_turn()

    def skip_turn(self) -> None:
        """
        skips a turn
        Parameters: None
        
        Returns: nothing
        """
        if self._turn < self.num_players:
            self._turn += 1
        else:
            self._turn = 1

    def end_game(self) -> None:
        """
        Ends the game
        Parameters: None
            
        Returns: nothing
        """
        final_dict = {}
        highest_pieces = 0

        for i in range(1, self.num_players + 1):
            final_dict[i] = 0

        for piece in self.pieces:
            final_dict[piece.player] += 1

        for player in final_dict:
            if final_dict[player] > highest_pieces:
                self._outcome = [player]
                highest_pieces = final_dict[player]
            elif final_dict[player] == highest_pieces:
                self._outcome.append(player)

        self._done = True
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
                if square is not None:
                    if square > self.num_players or square < 0:
                        raise ValueError("Grid contains invalid player")
                
        self._board = new_board
        self._done = False
        self._outcome = []
        self._turn = turn

    def roll_back(self) -> None:
        """
        Undoes the most recent move
        
        Parameters: none beyond self
        Returns: nothing
        """
        recent_move = self._moves.pop()

        trn, mv = recent_move
        self._turn = trn
        
        if self._done:
            self._done = False
            self._outcome = []


        if len(mv) == 1:
            self.first_two = True


        for square in mv:
            pos, player = square
            if player > 0:
                self._board.update_piece(pos, player)
            else:
                self._board.remove_piece(pos)


    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "Reversi":
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