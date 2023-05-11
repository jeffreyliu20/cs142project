import sys
from typing import List, Optional, Tuple, Set, Callable
from mocks import ReversiStub, ReversiMock
from reversi import BoardGridType
from math import sqrt

import pygame

pygame.init()
# game = ReversiStub(board_size, num_players, othello)
    
reversi = ReversiStub(int(sys.argv[1]), 2, True)

class Board:
    """
    Class for a GUI-based bitmap editor
    """

    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock
    reversi : ReversiStub
    
    def __init__(self, reversi: ReversiStub, window: int = 600, border: int = 10,
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
        
        board_size = int(sys.argv[1])
        self.window = window
        self.border = border
        self.grid = [[False] * cells_side for i in range(cells_side)]
        self.current_tool = "black"

        print (reversi.grid)

        pygame.init()
        pygame.display.set_caption("BitEdit")
        self.surface = pygame.display.set_mode((window + border + cells_side,
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
        mini_left = 2 * self.border + square * cells_side
        mini_top = (self.window - cells_side) // 2

        rect = (mini_left, mini_top, cells_side, cells_side)
        # pygame.draw.rect(self.surface, color=(255, 255, 255),
        #                  rect=rect)
        # pygame.draw.circle(self.surface, color=(255, 0, 0),
        #                    center=current_tool_center, radius=cells_side / 1.5,
        #                    width=10)

        for row in range(len(self.reversi.grid)):
            for col in range(len(self.reversi.grid[row])):
                rect = (self.border + col * square,
                        self.border + row * square,
                        square, square)
                fill = (255, 255, 255)
                border = True
                pygame.draw.rect(self.surface, color=fill,
                                 rect=rect)
                if border:
                    pygame.draw.rect(self.surface, color=(0, 0, 0),
                                     rect=rect, width=1)

        for row in range(len(self.reversi.grid)):
            for col in range(len(self.reversi.grid[row])):   
                if self.reversi.grid[row][col]:
                    # center_x = self.border + row * square + (self.border + col * square - self.border + row * square) / 2
                    # center_y = 
                    color = (255, 0, 0) if self.reversi.grid[row][col] == 1 else (0, 0, 0)
                    pygame.draw.circle(self.surface, color=color,
                           center=(self.border + col * square + square / 2, self.border + row * square + square /2), radius=cells_side * 3,
                           width=10)
                    
    def dist(self, p1: tuple, p2: tuple) -> int:
        """
        Calculates the distance between two points on the grid 

        Parameters:
            p1 : tuple : coordinate of point 1
            p2 : tuple : coordinate of point 2
        
        Returns: distance between p1 and p2
        """
        x1, y1 = p1
        x2, y2 = p2
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def react_to(self):
        """
        Helper function to provide correct behavior for each particular tool (black, white, and fill). 
        Called when user usees mouse to click on tool or grid. 

        Parameters: none beyond self

        Returns: nothing
        """
        cells_side = len(self.grid)
        radius = cells_side // 2
        square = (self.window - 2 * self.border) // cells_side
        pos = pygame.mouse.get_pos()
        x, y = pos

        if self.dist(pos, self.white_tool_center) <= radius:
            self.current_tool = "white"
        
        elif self.dist(pos, self.black_tool_center) <= radius:
            self.current_tool = "black"

        elif self.dist(pos, self.fill_tool_center) <= radius:
            self.current_tool = "fill"
        elif x >= self.border and x <= self.window - self.border and y >= self.border and y <= self.window - self.border:
            row = (y - self.border) // square
            col = (x - self.border) // square
            if self.current_tool == "black":
                self.grid[row][col] = True
            elif self.current_tool == "white":
                self.grid[row][col] = False
            elif self.current_tool == "fill":
                flood_fill(self.grid, (row, col))
        

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

# # set up the window
# size = (640, 640)
# screen = pygame.display.set_mode(size)
# pygame.display.set_caption("Reversi")

# # set up the board
# board = pygame.Surface((1000, 1000))

# #check if the size of the board is valid
# board_size = int(sys.argv[1])
# if board_size > 20 or board_size < 6:
#     print("The board size is not valid")
#     sys.exit()

# # draw the board
# for x in range(0, int(sys.argv[1]), 2):
#     for y in range(0, int(sys.argv[1]), 2):
#         pygame.draw.rect(board, (0, 0, 255), (x*75, y*75, 75, 75))
#         pygame.draw.rect(board, (0, 0, 255), ((x+1)*75, (y+1)*75, 75, 75))

# # add the board to the screen
# screen.blit(board, (20, 20))

# pygame.display.flip()

# # main loop
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()