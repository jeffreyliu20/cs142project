"""
One Note: I do not use the check_for_dead_moves method because I want to notify
the player if their turn is skipped, which I can't do using that method
"""


from typing import List, Tuple
from reversi import BoardGridType, Reversi, ListMovesType
from bot import choose_random_move, choose_high_n_move, choose_high_m_move

import click

WALL_CHARS = {
    "H_WALL": "─", "V_WALL": "│", "HV_WALL": "┼",
    "NW_CORNER": "┌", "NE_CORNER": "┐", "SW_CORNER": "└", "SE_CORNER": "┘",
    "VE_WALL": "├", "VW_WALL": "┤", "HS_WALL": "┬", "HN_WALL": "┴",
    "N_WALL": "╵", "E_WALL": "╶", "S_WALL": "╷", "W_WALL": "╴"
}

CLOCK_CHARS = {
    (False, False, False, False): " ",
    (False, False, False, True): WALL_CHARS["W_WALL"],
    (False, False, True, False): WALL_CHARS["S_WALL"],
    (False, False, True, True): WALL_CHARS["NE_CORNER"],
    (False, True, False, False): WALL_CHARS["E_WALL"],
    (False, True, False, True): WALL_CHARS["H_WALL"],
    (False, True, True, False): WALL_CHARS["NW_CORNER"],
    (False, True, True, True): WALL_CHARS["HS_WALL"],
    (True, False, False, False): WALL_CHARS["N_WALL"],
    (True, False, False, True): WALL_CHARS["SE_CORNER"],
    (True, False, True, False): WALL_CHARS["V_WALL"],
    (True, False, True, True): WALL_CHARS["VW_WALL"],
    (True, True, False, False): WALL_CHARS["SW_CORNER"],
    (True, True, False, True): WALL_CHARS["HN_WALL"],
    (True, True, True, False): WALL_CHARS["VE_WALL"],
    (True, True, True, True): WALL_CHARS["HV_WALL"]
}

@click.command()
@click.option('-n', '--num_players', default=2, show_default=True, type=int,
              help="Number of Players in the game")
@click.option('-s', '--board_size', default=8, show_default=True, type=int,
              help="Length of the sides of the board")
@click.option('--othello/--non-othello', default=False, show_default=True,
              help="Whether or not the game is othello or not othello")
@click.option('--bot', default='none', show_default=True,
              type=click.Choice(['none', "random", "smart", "very-smart"]),
              help="What type of bot strategy you want to use")

def play_game(num_players: int, board_size: int, othello: bool, bot: str):
    """
    Runs the reversi game in a textual user interface after taking in some
    command line arguments.
    """

    if board_size < 3:
        print("Board size must be 3 or greater. Please try again.")
    elif not 2 <= num_players <= 9:
        print("Number of players must be between 2 & 9")
    elif num_players % 2 != board_size % 2:
        print("Board size and number of players must both be odd or both be " +
              "even. Please try again")
    else:
        game: Reversi = Reversi(board_size, num_players, othello)

        bot_in_game: bool = bot != "none"

        grid_size: int = 2 * board_size + 1
        board: List[List[str]] = []

        board_str, board = make_board_str(grid_size, game.grid, board, True)
        print(board_str)

        if bot_in_game:
            print()
            print(f"The bot will be Player {num_players}")

        players_skipped: int = 0

        while not game.done and players_skipped < num_players:

            moves: ListMovesType = game.available_moves
            turn: int = game.turn

            if len(moves) == 0:
                print()
                print(f"Player {turn} has no available moves")
                print(f"Skipping Player {turn}'s turn")
                print()
                game.skip_turn()
                players_skipped += 1
            else:
                move_r, move_c = (-1,-1)

                if bot_in_game and turn == num_players:
                    bot_move = None
                    if bot == "random":
                        bot_move = choose_random_move(game)
                    elif bot == "smart":
                        bot_move = choose_high_n_move(game)
                    else:
                        bot_move = choose_high_m_move(game)
                    move_r, move_c = bot_move
                    print()
                    print()
                    print(f"Bot is making the move ({move_r}, {move_c})")
                    print()
                else:
                    print()
                    print()
                    print(f"It is Player {turn}'s turn to make a move.")
                    print("Choose one of the following move options:")
                    print()

                    players_skipped = 0

                    for k, move in enumerate(moves):
                        i, j = move
                        print(f"{k+1}) ({i}, {j})")

                    print()
                    print("If you want to exit the game, type 'quit', " +
                        "then press Enter")
                    choice = input("Enter your choice, then press Enter: ")
                    print()

                    while True:
                        if choice == "quit":
                            break
                        if choice.isdigit() and 0 < int(choice) <= len(moves):
                            break
                        print("You must input an integer that is the same as " +
                            "one of the options")
                        choice = input("Enter your choice, then press Enter: ")

                    if choice == "quit":
                        break

                    move_r, move_c = moves[int(choice)-1]

                if not game.legal_move((move_r, move_c)):
                    print("Not a legal move, please try again")
                    continue

                game.apply_move((move_r, move_c))

                board_str, board = make_board_str(grid_size, game.grid, board,
                                                  False)
                print(board_str)

        game.end_game()
        winners = game.outcome
        if len(winners) == 1:
            print(f"Congrats for Player {winners[0]} for a nice victory")
        else:
            print("We have a tie between the following players:")
            for person in winners:
                print(f"Player {person}")


def make_board_str(grid_size: int, grid: BoardGridType, board: List[List[str]],
                   first_time) -> Tuple[str, List[List[str]]]:
    """
    Creates a string object representing the board that will be printed given
    a certain 2x2 matrix of strings. If it is the first time this method is
    called, it builds the board as well. Otherwise, it updates the board as the
    moves are made

    Inputs:
        grid_size: side lengths of the string representation
        grid: the reversi game grid that has where the board pieces are
        board: the string matrix that is used to create the string representation
        first_time: a boolean indicating whether or not this is the first_time
        this method has been called

    Returns:
        Returns a tuple containing the string representation and the matrix
        used to create that string representation
    """

    if first_time:
        for _ in range(grid_size):
            board_row: List[str] = []
            for _ in range(grid_size):
                board_row.append("")
            board.append(board_row)

        for r in range(grid_size):
            for c in range(grid_size):
                grid_dir = [True] * 4

                if r % 2 != 0:
                    grid_dir[1] = False
                    grid_dir[3] = False
                elif r == 0:
                    grid_dir[0] = False
                elif r == len(board) - 1:
                    grid_dir[2] = False

                if c % 2 != 0:
                    grid_dir[0] = False
                    grid_dir[2] = False
                elif c == 0:
                    grid_dir[3] = False
                elif c == len(board) - 1:
                    grid_dir[1] = False

                tup = (grid_dir[0], grid_dir[1], grid_dir[2], grid_dir[3])
                board[r][c] = CLOCK_CHARS[tup]

    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if grid[x][y] != 0:
                board[2 * x + 1][2 * y + 1] = f"{cell}"

    board_row = [" "]
    bottom_row = ""
    for i in range(grid_size):
        if i % 2 == 0:
            bottom_row += " "
        else:
            bottom_row += f"{i // 2}"

    for j, row2 in enumerate(board):
        if j % 2 == 1:
            board_row.append("".join(row2) + f"{j // 2}")
        else:
            board_row.append("".join(row2))

    board_row.append(bottom_row)
    board_str = "\n".join(board_row)
    return board_str, board


if __name__ == "__main__":
    play_game()
