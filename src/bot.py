"""
A bot that repeatedly creates ReversiGame instances and plays against itself, 
recording the results.
Currently only functional for the ReversiStub class.
"""
import sys
from reversi import ReversiBase
from mocks import ReversiStub, ReversiBotMock
from typing import Tuple
import random

def choose_random_move(revers: ReversiBase) -> Tuple[int, int]:
    """
    Chooses a move at random from available moves in a Reversi game

    Parameters:
      revers[ReversiBase]: a reversi Game
    
    Returns[Tuple[int, int]]: coordinates corresponding to a move
    """
    return random.choice(revers.available_moves)

def choose_high_n_move(revers: ReversiBase) -> Tuple[int, int]:
    """
    Chooses the move that will take the most pieces in a Reversi game
    
    Parameters:
        revers[ReversiBase]: a reversi game
        
    Returns[Tuple[int, int]]: coordinates corresponding to a move
    """
    move_n = {}
    for move in revers.available_moves:
        n = 0
        simulated_game = revers.simulate_moves([move])
        for row in simulated_game.grid:
            for piece in row:
                if piece == revers.turn:
                    n += 1
        move_n[move] = n

    return max(move_n, key=move_n.get)


def play_game() -> str:
    """
    Simulates a game of Reversi between two bots
    
    Parameters: none
    
    Returns [str]: "Player X wins" where x is the winning player or "Tie"
    """
    game = ReversiBotMock(side=8, players=2, othello=True)

    while not game.done:
        if game.turn == 1:
            move = choose_random_move(game)
        elif game.turn == 2:
            move = choose_high_n_move(game)
        game.apply_move(move)

    if len(game.outcome) > 1:
        return "Tie"
    winning_player = str(game.outcome[0])
    return f"Player {winning_player} wins"



if len(sys.argv) != 2:
    raise ValueError("bot.py only accepts one input (number of games)")
NUM_GAMES = int(sys.argv[1])
games_played = 0
results = {"Player 1 wins": 0, "Player 2 wins": 0, "Tie": 0}

while games_played < NUM_GAMES:
    results[play_game()] += 1
    games_played += 1

for key, value in results.items():
    percentage = value / NUM_GAMES * 100
    print(f"{key}: {percentage}%")
