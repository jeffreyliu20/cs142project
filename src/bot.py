"""
A bot that repeatedly creates ReversiGame instances and plays against itself, 
recording the results.
Currently only functional for the ReversiStub class.
"""
import sys
from mocks import ReversiStub
from typing import Union

NUM_GAMES = sys.argv[1]
games_played = 0
results = {"Player 1 wins": 0, "Player 2 wins": 0, "Tie": 0}

while games_played < NUM_GAMES:
    results[play_game()] += 1
    games_played += 1

for key, value in results.items():
    percentage = value / NUM_GAMES
    print(f"{key}: {percentage}%")



