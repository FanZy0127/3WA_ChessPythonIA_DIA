from src.build.piece import *
from src.consts.consts import *
from src.build.move import Move
from src.build.square import Square


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

    # Method initializing the pieces positions
    def _add_pieces(self, color):

        row_pieces, row_pawns = (7, 6) if color == 'white' else (0, 1)

        # Initialization of the Pawns
        for column in range(COLUMNS):
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

    @staticmethod
    def move(piece, base_row, base_column, allowed_move_row, allowed_move_column):
        base_square = Square(base_row, base_column)
        final_square = Square(allowed_move_row, allowed_move_column)

        # print(piece.name, f'Base Square {(base_row, base_column)}',
        #       f'Destination {(allowed_move_row, allowed_move_column)}',
        #       f'Direction {piece.direction if isinstance(piece, Pawn) else None}')

        move = Move(base_square, final_square)
        piece.add_move(move)

    def calculate_allowed_moves(self, piece, row, column):

        def pawn_moves():
            allowed_steps = 1 if piece.has_moved else 2

            # Regular moves (vertical)
            start_of_loop = row + piece.direction
            # exclusive so excluded from the loop
            end_of_loop = row + piece.direction * (1 + allowed_steps)  # Brackets needed for the white pawns destination

            # The loop then goes from [1;3[ for 1st move or [1;2[ after 1st move, mathematically speaking
            for allowed_move_row in range(start_of_loop, end_of_loop, piece.direction):
                if Square.is_in_range(allowed_move_row):
                    if self.squares[allowed_move_row][column].is_empty():
                        self.move(piece, row, column, allowed_move_row, column)
                    else:
                        break  # If there's already a piece in front of our pawn, it can't move straight
                else:
                    break  # Meaning the wanted square is not in range

            # Attacking moves (diagonal)

        def rook_moves():
            pass

        def knight_moves():
            # A Knight has a maximum of 8 allowed moves
            allowed_moves = [
                (row + allowed_move_row, column + allowed_move_column)
                for x, y in [(1, 2), (2, 1)]  # magnitudes
                for allowed_move_row, allowed_move_column in [(x, y), (x, -y), (-x, y), (-x, -y)]  # directions
            ]

            for allowed_move_row, allowed_move_column in allowed_moves:
                if Square.is_in_range(allowed_move_row, allowed_move_column):  # check if out of the board
                    if self.squares[allowed_move_row][allowed_move_column].is_empty_or_has_an_opponent_piece(
                            piece.color):
                        self.move(piece, row, column, allowed_move_row, allowed_move_column)

        def bishop_moves():
            pass

        def queen_moves():
            pass

        def king_moves():
            pass

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Rook):
            rook_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            bishop_moves()
        elif isinstance(piece, Queen):
            queen_moves()
        elif isinstance(piece, King):
            king_moves()
