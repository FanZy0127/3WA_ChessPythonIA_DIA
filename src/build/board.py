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
        self.last_registered_move = None

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

    def apply_move_on_screen(self, piece, move):
        base_square = move.base_square
        final_square = move.final_square

        self.squares[base_square.row][base_square.column].piece = None
        self.squares[final_square.row][final_square.column].piece = piece

        piece.has_moved = True  # Necessary to define the pawns allowed moves (1 or 2 squares)
        piece.reset_moves()
        self.last_registered_move = move

    @staticmethod
    def validate_move(piece, move):
        return move in piece.legal_moves

    def calculate_allowed_moves(self, piece, row, column):

        def pawn_moves():
            allowed_steps = 1 if piece.has_moved else 2

            # Regular moves (vertical)
            start_of_loop = row + piece.direction
            # Exclusive so excluded from the loop
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
            allowed_move_row = row + piece.direction
            allowed_move_columns = [column - 1, column + 1]

            for allowed_move_column in allowed_move_columns:
                if Square.is_in_range(allowed_move_row, allowed_move_column):
                    if self.squares[allowed_move_row][allowed_move_column].has_opponent_piece(piece.color):
                        self.move(piece, row, column, allowed_move_row, allowed_move_column)

            # TODO Implement the "prise en passant" and pawn promotion

        def knight_moves():
            # A Knight has a maximum of 8 allowed moves
            allowed_moves = [
                (row + allowed_move_row, column + allowed_move_column)
                for x, y in [(1, 2), (2, 1)]  # Magnitudes
                for allowed_move_row, allowed_move_column in [(x, y), (x, -y), (-x, y), (-x, -y)]  # Directions
            ]

            for allowed_move_row, allowed_move_column in allowed_moves:
                if Square.is_in_range(allowed_move_row, allowed_move_column):  # Check if out of the board
                    if self.squares[allowed_move_row][allowed_move_column].is_empty_or_has_an_opponent_piece(
                            piece.color):
                        self.move(piece, row, column, allowed_move_row, allowed_move_column)

        def straightline_moves(increments):
            for increment in increments:
                row_increment, column_increment = increment
                allowed_move_row = row + row_increment
                allowed_move_column = column + column_increment

                while True:
                    if Square.is_in_range(allowed_move_row, allowed_move_column):
                        base_square = Square(row, column)
                        final_square = Square(allowed_move_row, allowed_move_column)
                        move = Move(base_square, final_square)

                        if self.squares[allowed_move_row][allowed_move_column].is_empty():
                            piece.add_move(move)
                        # Check if there's an opponent piece on the way
                        elif self.squares[allowed_move_row][allowed_move_column].has_opponent_piece(piece.color):
                            piece.add_move(move)
                            break
                        # Check if there's one of our pieces on the way
                        elif self.squares[allowed_move_row][allowed_move_column].has_team_piece(piece.color):
                            break
                    else:
                        break

                    # Incrementing the increments
                    allowed_move_row = allowed_move_row + row_increment
                    allowed_move_column = allowed_move_column + column_increment

        def king_moves():

            bordering_squares = [
                (row - 1, column - 1),
                (row - 1, column + 0),
                (row - 1, column + 1),
                (row + 0, column - 1),
                (row + 0, column + 1),
                (row + 1, column - 1),
                (row + 1, column + 0),
                (row + 1, column + 1)
            ]

            # Regular moves
            for allowed_move in bordering_squares:
                allowed_move_row, allowed_move_column = allowed_move

                if Square.is_in_range(allowed_move_row, allowed_move_column):
                    if self.squares[allowed_move_row][allowed_move_column].is_empty_or_has_an_opponent_piece(
                            piece.color):
                        self.move(piece, row, column, allowed_move_row, allowed_move_column)

            # TODO Implement Queen/King Castling
            # Queen Castling
            # King Castling

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Rook):
            straightline_moves([(-1, 0), (0, -1), (1, 0), (0, 1)])
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straightline_moves([(-1, +1), (-1, -1), (1, 1), (1, -1)])
        elif isinstance(piece, Queen):
            straightline_moves([(-1, +1), (-1, -1), (1, 1), (1, -1), (-1, 0), (0, -1), (1, 0), (0, 1)])
        elif isinstance(piece, King):
            king_moves()
