"""
A bot that repeatedly creates ReversiGame instances and plays against itself, 
recording the results.
Currently only functional for the ReversiStub class.
"""
import sys
from reversi import Reversi
from typing import Tuple
import random
import click
import numpy as np
import copy

def choose_random_move(revers: Reversi) -> Tuple[int, int]:
    """
    Chooses a move at random from available moves in a Reversi game

    Parameters:
      revers[Reversi]: a reversi Game
    
    Returns[Tuple[int, int]]: coordinates corresponding to a move
    """
    return random.choice(revers.available_moves)

def choose_high_n_move(revers: Reversi) -> Tuple[int, int]:
    """
    Chooses the move that will take the most pieces in a Reversi game
    
    Parameters:
        revers[Reversi]: a reversi game
        
    Returns[Tuple[int, int]]: coordinates corresponding to a move
    """
    move_n = {}
    for move in revers.available_moves:
        revers.apply_move(move)
        _, counts = np.unique(revers.grid, return_counts=True)
        try:
            move_n[move] = counts[2]
        except IndexError:
            move_n[move] = counts[1]
        revers.roll_back()
        


    return max(move_n, key= lambda x: move_n[x])

def choose_high_m_move(revers: Reversi) -> Tuple[int, int]:
    """
    Chooses the move that will take the most pieces and retain them 
    after the next turn in a Reversi game
    
    Parameters:
        revers[Reversi]: a reversi game
        
    Returns[Tuple[int, int]]: coordinates corresponding to a move
    """
    move_m = {}

    for move in revers.available_moves:
        revers.apply_move(move)
        possible_m_list = []
        for mov in revers.available_moves:
            revers.apply_move(mov)
            _, counts = np.unique(revers.grid, return_counts=True)
            try:
                possible_m_list.append(counts[2])
            except IndexError:
                possible_m_list.append(counts[1])
            revers.roll_back()
        revers.roll_back()

        if len(possible_m_list) > 0:
            move_m[move] = sum(possible_m_list) / len(possible_m_list)
        else:
            move_m[move] = 64

    
    return max(move_m, key= lambda x: move_m[x])


def play_game(player1, player2) -> str:
    """
    Simulates a game of Reversi between two bots
    
    Parameters: none
    
    Returns [str]: "Player X wins" where x is the winning player or "Tie"
    """
    game = Reversi(side=8, players=2, othello=False)

    while not game.done:
        if game.turn == 1:
            if player1 == "random":
                move = choose_random_move(game)
            if player1 == "smart":
                move = choose_high_n_move(game)
            if player1 == "very-smart":
                move = choose_high_m_move(game)
        elif game.turn == 2:
            if player2 == "random":
                move = choose_random_move(game)
            if player2 == "smart":
                move = choose_high_n_move(game)
            if player2 == "very-smart":
                move = choose_high_m_move(game)

        game.apply_move(move)

    if len(game.outcome) > 1:
        return "Tie"
    winning_player = str(game.outcome[0])
    return f"Player {winning_player} wins"



@click.command("banner")
@click.option("-n", "--num_games", default="100")
@click.option("-1", "--player1", 
              type=click.Choice(["random", "smart", "very-smart"]), 
              default="random")
@click.option("-2", "--player2", 
              type=click.Choice(["random", "smart", "very-smart"]), 
              default="random")

def cmd(num_games, player1, player2):
    NUM_GAMES = int(num_games)
    games_played = 0
    results = {"Player 1 wins": 0, "Player 2 wins": 0, "Tie": 0}

    while games_played < NUM_GAMES:
        results[play_game(player1, player2)] += 1
        games_played += 1

    for key, value in results.items():
        percentage = value / NUM_GAMES * 100
        print(f"{key}: {percentage}%")

if __name__ == "__main__":
    cmd()
