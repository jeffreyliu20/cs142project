# CMSC 14200 Course Project

Team members:
- Ned Tagtmeier (ntagtmeier) - worked on bot
- Sylvia Kim (sylviakim) - worked on gui
- Enoch Woldu (ewoldu) - worked on tui
- Jeffrey Liu (jliu26) - worked on qa

Enhancements:
    -implemented the board as a numpy array
    -added bot player support to the TUI

Improvements:
- Game Logic:
    [Code completeness] This only works if your non-Othello game is 8x8.:
        Addressed by implementing the lower_bound and upper_bound variables
         from lines 588-593 of reversi.py

    [Code completeness] Something seems wrong here, dir_moves should just be a 
    tuple, so this loop makes move an integer.:
        This piece of feedback was incorrect - find_moves outputs a dictionary
         mapping tuples to lists of tuples, meaning that find_moves.values()
         returns a list of lists of tuples, meaning that "move" is a tuple.

    [Code completeness] This does not handle the case where get_piece returns 
    None (this will throw an error).
        Changed the get_piece function (reversi.py lines 676-680) to return
         the value on the grid in the given position. Because the grid is a 
         numpy array that uses 0 to indicate no piece, the function returns
         None iff the given position on the grid is zero.

    [Code completeness] This does not handle the case where neither player 
    has available moves, but the game is still over. This makes the done 
    function incorrect as well.
        For the bot, the code we wrote to skip turns after a move is applied 
         (reversi.py 772-793) should fix this (called in bot.py line 109).
         The tui implemented a "players_skipped" variable (tui.py line 115) instead
         so that it could output a message everytime a player is skipped.

    [Code completeness] Since the turn counter is 1-indexed, this is incorrect. 
    When it is the nth player's turn to play (when n = num_players), their 
    turn will be skipped.
        Our code no longer increments the turn automatically after every move. 
         Instead, each component calls the skip_turn function (reversi.py 795-805)
         individually after each move.

    [Code completeness] Your load game function does not change the turn.
        reversi.py 867 changes the turn
        
- Bot:
    This component received two S's in Milestone 2.
    
- TUI:
    This component received two S's in Milestone 2.
    
- QA:
    This component received two S's in Milestone 2.
