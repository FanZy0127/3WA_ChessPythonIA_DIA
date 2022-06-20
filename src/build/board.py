from src.consts.consts import *
from src.build.square import Square
from src.build.piece import *


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(COLUMNS)]
        self._instantiate()
        self._add_pieces('white')
        self._add_pieces('black')

    def _instantiate(self):

        for row in range(ROWS):
            for column in range(COLUMNS):
                self.squares[row][column] = Square(row, column)

    def _add_pieces(self, color):

        row_pieces, row_pawns = (7, 6) if color == 'white' else (0, 1)

        # Initialization of the Pawns
        for column in range (COLUMNS):
            self.squares[row_pawns][column] = Square(row_pawns, column, Pawn(color))

        # Initialization of the Rooks
        self.squares[row_pieces][0] = Square(row_pieces, 0, Rook(color))
        self.squares[row_pieces][7] = Square(row_pieces, 7, Rook(color))

        # Initialization of the Knights
        self.squares[row_pieces][1] = Square(row_pieces, 1, Knight(color))
        self.squares[row_pieces][6] = Square(row_pieces, 6, Knight(color))

        # Initialization of the Bishops
        self.squares[row_pieces][2] = Square(row_pieces, 2, Bishop(color))
        self.squares[row_pieces][5] = Square(row_pieces, 5, Bishop(color))

        # Initialization of the Queens
        self.squares[row_pieces][3] = Square(row_pieces, 3, Queen(color))

        # Initialization of the Kings
        self.squares[row_pieces][4] = Square(row_pieces, 4, King(color))

    def calculate_allowed_moves(self, piece, row, column):

        def knight_moves():
            # A Knight has a maximum of 8 alowed moves
            allowed_moves = [
                (row + allowed_move_row, column + allowed_move_column)
                for x, y in [(1, 2), (2, 1)]  # magnitudes
                for allowed_move_row, allowed_move_column in [(x, y), (x, -y), (-x, y), (-x, -y)]  # directions
            ]

            for allowed_move_row, allowed_move_column in allowed_moves:
                if Square.is_in_range(row + allowed_move_row, column + allowed_move_column):  # check if out of the board
                    # TODO Resolve this part of the script
                    if self.squares[allowed_move_row][allowed_move_column].is_empty_or_has_an_opponent_piece(piece.color):
                        pass

        if isinstance(piece, Pawn):
            pass
        elif isinstance(piece, Rook):
            pass
        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            pass
        elif isinstance(piece, Queen):
            pass
        elif isinstance(piece, King):
            pass
