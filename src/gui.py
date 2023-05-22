import sys
from typing import List, Optional, Tuple, Set, Callable
from mocks import ReversiStub, ReversiMock
from reversi import Reversi
from math import sqrt

import pygame
import click

pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

@click.command()
@click.option('-n', '--num_players', default=2, show_default=True, type=int,
              help="Number of Players in the game")
@click.option('-s', '--board_size', default=8, show_default=True, type=int,
              help="Length of the sides of the board")
@click.option('--othello/--non-othello', default=False, show_default=True,
              help="Whether or not the game is othello or not othello")

class ReversiGUI:
    """
    Class for a GUI-based bitmap editor
    """
    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock
    reversi : Reversi

    def __init__(self, num_players : int, board_size: int, othello : bool, window: int = 600, border: int = 10,
                 cells_side: int = 32):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            cells_side : int : number of cells on a side of a square bitmap grid
        """
        if board_size > 20 or board_size < 6:
            print("The board size is not valid")
            sys.exit()
        
        self.window = window
        self.border = border
        self.grid = [[False] * cells_side for i in range(cells_side)]
        self.reversi = Reversi(board_size, num_players, othello)

        pygame.init()
        pygame.display.set_caption("BitEdit")
        self.surface = pygame.display.set_mode((window + 12 * border + cells_side,
                                                window))
        self.clock = pygame.time.Clock()

        self.event_loop()

    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        cells_side = len(self.reversi.grid)

        self.surface.fill((128, 128, 128))

        square = (self.window - 2 * self.border) // cells_side

        for row in range(len(self.reversi.grid)):
            for col in range(len(self.reversi.grid[row])):
                rect = (self.border + col * square,
                        self.border + row * square,
                        square, square)
                fill = (255, 255, 255)
                pygame.draw.rect(self.surface, color=fill,
                                 rect=rect)
                pygame.draw.rect(self.surface, color=(0, 0, 0),
                                     rect=rect, width=1)

        player_colors = [(255, 0, 0), (0, 0, 0), (0, 255, 0), (0, 0, 255), (255, 215, 0), (191,62,255), (0, 238, 238), (255, 52, 179), (205, 186, 150)]
        for row in range(len(self.reversi.grid)):
            for col in range(len(self.reversi.grid[row])):   
                if self.reversi.grid[row][col]:
                    color = self.reversi.grid[row][col] - 1
                    pygame.draw.circle(self.surface, color=player_colors[color],
                           center=(self.border + col * square + square / 2, self.border + row * square + square /2), radius=cells_side * 3,
                           width=10)
        

        pygame.display.set_caption('Show Text')
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(f"Player {self.reversi.turn}", True, white, blue)
        textRect = text.get_rect()
        textRect.center = (665, 80)
        self.surface.blit(text, textRect)

        for move in self.reversi.available_moves:
            rect = (self.border + move[1] * square,
                    self.border + move[0] * square,
                    square, square)
            fill = (211, 211, 211)
            pygame.draw.circle(self.surface, color=fill,
                        center=(self.border + move[1] * square + square / 2, self.border + move[0] * square + square /2), radius=cells_side * 3,
                        width=10)

    def react_to(self):
        """
        Helper function to provide correct behavior for each particular tool (black, white, and fill). 
        Called when user usees mouse to click on tool or grid. 

        Parameters: none beyond self

        Returns: nothing
        """
        cells_side = len(self.reversi.grid)
        square = (self.window - 2 * self.border) // cells_side
        x, y = pygame.mouse.get_pos()

        if x >= self.border and x <= self.window - self.border and y >= self.border and y <= self.window - self.border:
            row = (y - self.border) // square
            col = (x - self.border) // square
        
            if self.reversi.legal_move((row, col)):
                self.reversi.apply_move((row, col))
                
    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.react_to()

            self.draw_window()
            pygame.display.update()
            self.clock.tick(24)


if __name__ == "__main__":
    ReversiGUI()