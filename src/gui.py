import sys
from typing import List, Optional, Tuple, Set, Callable
from mocks import ReversiStub, ReversiMock
from reversi import Reversi
from math import sqrt

import pygame

pygame.init()
    
reversi = Reversi(int(sys.argv[1]), 2, True)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

class Board:
    """
    Class for a GUI-based bitmap editor
    """

    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock
    reversi : Reversi

    def __init__(self, reversi: Reversi, window: int = 600, border: int = 10,
                 cells_side: int = 32):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            cells_side : int : number of cells on a side of a square bitmap grid
        """
        self.reversi = reversi
        if len(reversi.grid) > 20 or len(reversi.grid) < 6:
            print("The board size is not valid")
            sys.exit()
        
        self.window = window
        self.border = border
        self.grid = [[False] * cells_side for i in range(cells_side)]

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
        # mini_left = 2 * self.border + square * cells_side
        # mini_top = (self.window - cells_side) // 2

        # rect = (mini_left, mini_top, cells_side, cells_side)

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

        for row in range(len(self.reversi.grid)):
            for col in range(len(self.reversi.grid[row])):   
                if self.reversi.grid[row][col]:
                    color = (255, 0, 0) if self.reversi.grid[row][col] == 1 else (0, 0, 0)
                    pygame.draw.circle(self.surface, color=color,
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
    Board(reversi)