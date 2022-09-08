import pygame
from src.consts.consts import *
from src.build.board import Board
from src.build.dragger import Dragger


class Chess:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.hovered_square = None

    # Display method
    @staticmethod
    def display_background(surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                if (row + column) % 2 == 0:
                    color = (255, 191, 0)  # Amber yellow
                else:
                    color = (0, 150, 152)  # Viridian green

                # Defining shape of the rectangle (start_x, start_y, width, height)
                rectangle = (column * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

                pygame.draw.rect(surface, color, rectangle)

    def display_pieces(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):

                # Checking if there's already any piece on the square
                if self.board.squares[row][column].has_piece():
                    piece = self.board.squares[row][column].piece

                    if piece is not self.dragger.piece:
                        piece.set_image(size=80)
                        piece_image = pygame.image.load(piece.image)
                        image_center = column * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.image_rectangle = piece_image.get_rect(center=image_center)
                        surface.blit(piece_image, piece.image_rectangle)

    def display_moves(self, surface):

        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.legal_moves:
                color = '#C86464' if (move.final_square.row + move.final_square.column) % 2 == 0 else '#C84646'
                rectangle = (
                    move.final_square.column * SQUARE_SIZE,
                    move.final_square.row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE
                )
                pygame.draw.rect(surface, color, rectangle)

    def display_last_move(self, surface):
        if self.board.last_registered_move:
            base_square = self.board.last_registered_move.base_square
            final_square = self.board.last_registered_move.final_square

            for position in [base_square, final_square]:
                color = (255, 192, 203) if position.row + position.column % 2 == 0 else (255, 105, 180)
                rectangle = (position.column * SQUARE_SIZE, position.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rectangle)

    def display_hovered_square(self, surface):
        if self.hovered_square:
            color = (88, 24, 69)
            rectangle = (
                self.hovered_square.column * SQUARE_SIZE,
                self.hovered_square.row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE
            )
            pygame.draw.rect(surface, color, rectangle, width=5)

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    # Define which squares have to be hovered with a different color
    def set_hover_square(self, row, column):
        self.hovered_square = self.board.squares[row][column]

    def restart(self):
        self.__init__()
