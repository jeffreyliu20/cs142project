
import sys
from typing import List, Optional, Tuple, Set, Callable
from mocks import ReversiStub, ReversiMock
from reversi import BoardGridType

board_size: int = int(sys.argv[1])
num_players: int = 2
othello: bool = True

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

game = ReversiMock(board_size, num_players, othello)

if 6 <= board_size <= 20:

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
            if game.grid[x][y] is not None:
                board[2 * x + 1][2 * y + 1] = f"{cell}"

    board_row = []
    for row2 in board:
        board_row.append("".join(row2))

    board_str = "\n".join(board_row)
    print(board_str)

    victor = -1
    earlyEnd = False

    while not game.done:

        available_moves = game.available_moves

        print("Choose one of the following move options")
        print()

        for k, move in enumerate(available_moves):
            i, j = move
            print(f"{k+1}) {i}, {j}")
        
        print()
        print("If you want to exit the game, type 'quit' and then press Enter")
        choice = input("Enter your choice and then press Enter: ")
        print()
        
        while True:
            if choice == "quit":
                break
            if choice.isdigit() and 0 < int(choice) <= len(available_moves):
                break
            print("You must input an integer that is the same as one of the " +
                  "options")
            choice = input("Enter your choice and then press Enter: ")
            print()

        if choice == "quit":
            earlyEnd = True
            break

        move_r, move_c = available_moves[int(choice)]

        if not game.legal_move((move_r, move_c)):
            print("Not a legal move, please try again")
            continue

        game.apply_move((move_r, move_c))

        for x, row in enumerate(game.grid):
            for y, cell in enumerate(row):
                if game.grid[x][y] is not None:
                    board[2 * x + 1][2 * y + 1] = f"{cell}"

        board_row = []
        for row2 in board:
            board_row.append("".join(row2))

        board_str = "\n".join(board_row)
        print(board_str)

    if earlyEnd:
        print("Game Ended early")
    else:
        winners = game.outcome
        for person in winners:
            print(f"Congrats for Player {person} for a nice victory")


else:
    print("Invalid board size, please try again")
