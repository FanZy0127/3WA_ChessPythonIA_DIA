import pygame
from consts.consts import *


class Chess:

    def __init__(self):
        pass

    # Display method
    def display_background(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if (row + column) % 2 == 0:
                    # color = (255, 174, 105) # caramel brown
                    color = (255, 191, 0)  # amber yellow
                else:
                    color = (0, 150, 152)  # viridian green

                # Defining shape of the rectangle (start_x, start_y, width, height)
                rectangle = (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(surface, color, rectangle)
