import pygame
from src.consts.consts import *
from src.build.board import Board


class Chess:

    def __init__(self):
        self.board = Board()

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

    def display_pieces(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):

                # Checking if there's already any piece on the square
                if self.board.squares[row][column].has_piece():
                    piece = self.board.squares[row][column].piece
                    piece_image = pygame.image.load(piece.image)
                    image_center = column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                    piece.image_rectangle = piece_image.get_rect(center=image_center)
                    surface.blit(piece_image, piece.image_rectangle)