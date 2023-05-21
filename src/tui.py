
import sys
from typing import List, Optional, Tuple, Set, Callable
from mocks import ReversiStub, ReversiMock
from reversi import BoardGridType, Reversi

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
@click.option('-n', default=2, show_default=True, type=int,
              help="Number of Players in the game")
@click.option('-s', default=8, show_default=True, type=int,
              help="Length of the sides of the board")
@click.option('--othello/--non-othello', default=False, show_default=True,
              help="Whether or not the game is othello or not othello")
def play_game(n, s, othello):
    
    num_players = n
    board_size = s
    
    if board_size < 3:
        print("Board size must be 3 or greater. Please try again.")
    elif not (2 <= num_players <= 9):
        print("Number of players must be between 2 & 9")
    elif num_players % 2 != board_size % 2:
        print("Board size and number of players must both be odd or both be " + 
              "even. Please try again")
    else:

        game = Reversi(board_size, num_players, othello)
        
        grid_size = 2 * board_size + 1
        
        board = []

        for i in range(grid_size):
            board_row = []
            for j in range(grid_size):
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

        for x, row in enumerate(game.grid):
            for y, cell in enumerate(row):
                if game.grid[x][y] != 0:
                    board[2 * x + 1][2 * y + 1] = f"{cell}"

        board_row = [" "]
        bottom_row = ""
        for a in range(grid_size):
            if a % 2 == 0:
                bottom_row += " "
            else:
                bottom_row += f"{a // 2}"

        for b, row2 in enumerate(board):
            if b % 2 == 1:
                board_row.append("".join(row2) + f"{b // 2}")
            else:
                board_row.append("".join(row2))

        board_row.append(bottom_row)
        board_str = "\n".join(board_row)
        print(board_str)

        earlyEnd = False
        players_skipped = 0

        while not game.done and players_skipped < num_players:

            available_moves = game.available_moves
            turn = game._turn

            if len(available_moves) == 0:
                print()
                print(f"Player {turn} has no available moves")
                print(f"Skipping Player {turn}'s turn")
                print()
                game.skip_turn()
                players_skipped += 1
            else:
                print()
                print(f"It is Player {turn}'s turn to make a move.")
                print("Choose one of the following move options:")
                print()

                players_skipped = 0

                for k, move in enumerate(available_moves):
                    i, j = move
                    print(f"{k+1}) ({i}, {j})")
                
                print()
                print("If you want to exit the game, type 'quit' " + 
                    "and then press Enter")
                choice = input("Enter your choice and then press Enter: ")
                print()
                
                while True:
                    if choice == "quit":
                        break
                    if choice.isdigit() and 0 < int(choice) <= len(available_moves):
                        break
                    print("You must input an integer that is the same as one of " +
                        "the options")
                    choice = input("Enter your choice and then press Enter: ")

                if choice == "quit":
                    earlyEnd = True
                    break

                move_r, move_c = available_moves[int(choice)-1]

                # May be redundant
                if not game.legal_move((move_r, move_c)):
                    print("Not a legal move, please try again")
                    continue

                game.apply_move((move_r, move_c))

                for x, row in enumerate(game.grid):
                    for y, cell in enumerate(row):
                        if game.grid[x][y] != 0:
                            board[2 * x + 1][2 * y + 1] = f"{cell}"

                board_row = [" "]
                for b, row2 in enumerate(board):
                    if b % 2 == 1:
                        board_row.append("".join(row2) + f"{b // 2}")
                    else:
                        board_row.append("".join(row2))

                board_row.append(bottom_row)
                board_str = "\n".join(board_row)
                print(board_str)

        if earlyEnd:
            print("Game Ended early")
        else:
            game.end_game()
            winners = game.outcome
            if len(winners) == 1:
                print(f"Congrats for Player {winners[0]} for a nice victory")
            else:
                print("We have a tie between the following players:")
                for person in winners:
                    print(f"Player {person}")

play_game()