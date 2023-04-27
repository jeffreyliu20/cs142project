"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional

BoardGridType = List[List[Optional[int]]]
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
