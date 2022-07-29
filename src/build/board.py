import copy
from easygui import *
from src.AI.chess_AI import *
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

    def set_move(self, base_row, base_column, allowed_move_row, allowed_move_column):
        base_square = Square(base_row, base_column)
        final_square_piece = self.squares[allowed_move_row][allowed_move_column].piece
        final_square = Square(allowed_move_row, allowed_move_column, final_square_piece)

        return Move(base_square, final_square)

    def apply_move_on_screen(self, piece, move, not_allowed=False):
        base_square = move.base_square
        final_square = move.final_square

        empty_square_for_prise_en_passant = self.squares[final_square.row][final_square.column].is_empty()

        # Update of the board move
        self.squares[base_square.row][base_square.column].piece = None
        self.squares[final_square.row][final_square.column].piece = piece

        # Prise en passant
        if isinstance(piece, Pawn):
            difference = final_square.column - base_square.column
            if difference != 0 and empty_square_for_prise_en_passant:
                self.squares[base_square.row][base_square.column + difference].piece = None
                self.squares[final_square.row][final_square.column].piece = piece

        # Castling
        if isinstance(piece, King):
            if self.is_castling(base_square, final_square) and not not_allowed:
                difference = final_square.column - base_square.column
                rook = piece.left_rook if (difference < 0) else piece.right_rook
                self.apply_move_on_screen(rook, rook.legal_moves[-1])

        piece.has_moved = True  # Necessary to define the pawns allowed moves (1 or 2 squares)
        piece.reset_moves()
        self.last_registered_move = move

    @staticmethod
    def validate_move(piece, move):
        return move in piece.legal_moves

    def set_prise_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for column in range(COLUMNS):
                if isinstance(self.squares[row][column].piece, Pawn):
                    self.squares[row][column].piece.prise_en_passant = False

        piece.prise_en_passant = True

    def define_prise_en_passant_move(self, piece, row, column, row_to_check, column_to_check, final_row, boolean):
        if Square.is_in_range(column_to_check) and row == row_to_check:
            if self.squares[row][column_to_check].has_opponent_piece(piece.color):
                opponent_piece = self.squares[row][column_to_check].piece

                if isinstance(opponent_piece, Pawn):
                    if opponent_piece.prise_en_passant:
                        base_square = Square(row, column)
                        final_square = Square(final_row, column_to_check, opponent_piece)
                        move = Move(base_square, final_square)

                        # Checking if the king is in check
                        if boolean:
                            if not self.is_in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

    # Method displaying choices for the pawn promotion, and handling the promotion itself
    def promote_pawn(self, piece):
        final_square = self.last_registered_move.final_square
        promotion_choices = piece.get_promotion_choices(piece.color)
        promotion_choices_names = [promotion_choice.name for promotion_choice in promotion_choices]
        promotion_choices_images = [promotion_choice.image for promotion_choice in promotion_choices]
        title = "Pawn promotion"
        button = buttonbox("Choose a Pawn promotion", title=title,
                           images=promotion_choices_images, choices=promotion_choices_names)
        # TODO See if it is possible to beautify the display
        piece = self.squares[final_square.row][final_square.column].piece
        self.squares[final_square.row][final_square.column].piece = piece.set_promotion(button, piece.color)
        self.squares[final_square.row][final_square.column].piece.is_promoted = True

    def prepare_castling(self, king, rook, base_row, base_column, min_range, middle_column, max_range, boolean):
        if not rook.has_moved:
            for col in range(min_range, max_range):
                # Castling is impossible cause there's pieces between the King and the Rook
                if self.squares[base_row][col].has_piece():
                    break
                if col == middle_column:
                    if middle_column == 6:
                        king.right_rook = rook
                        base_square = Square(base_row, max_range)
                        final_square = Square(base_row, min_range)
                    elif middle_column == 3:
                        king.left_rook = rook
                        base_square = Square(base_row, 0)  # 0 being the starting column of the Queen's Rook
                        final_square = Square(base_row, middle_column)

                    rook_move = Move(base_square, final_square)

                    base_square = Square(base_row, base_column)
                    # King's final_square column is 6 for Queen's Rook and 2 for King's Rook
                    final_square = Square(base_row, (middle_column if middle_column == 6 else 2))
                    king_move = Move(base_square, final_square)

                    if boolean:
                        if not self.is_in_check(king, king_move) and not self.is_in_check(rook, rook_move):
                            rook.add_move(rook_move)
                            king.add_move(king_move)
                        else:
                            break
                    else:
                        rook.add_move(rook_move)
                        king.add_move(king_move)

    @staticmethod
    def is_castling(base_square, final_square):
        return abs(base_square.column - final_square.column) == 2

    def is_in_range_is_empty_or_has_opponent_piece_is_in_check(self, piece, row, column, allowed_moves_array, boolean):
        for allowed_move_row, allowed_move_column in allowed_moves_array:
            if Square.is_in_range(allowed_move_row, allowed_move_column):  # Check if out of the board
                if self.squares[allowed_move_row][allowed_move_column].is_empty_or_has_an_opponent_piece(
                        piece.color):
                    move = self.set_move(row, column, allowed_move_row, allowed_move_column)

                    if boolean:
                        if not self.is_in_check(piece, move):
                            piece.add_move(move)
                        # TODO Check if this is not causing bugs on check for castlings
                        else:
                            break
                    else:
                        piece.add_move(move)

    def calculate_allowed_moves(self, piece, row, column, boolean=True):

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
                        move = self.set_move(row, column, allowed_move_row, column)

                        if boolean:
                            if not self.is_in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
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
                        move = self.set_move(row, column, allowed_move_row, allowed_move_column)

                        if boolean:
                            if not self.is_in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            # Prise en passant
            row_to_check = 3 if piece.color == 'white' else 4
            final_row = 2 if piece.color == 'white' else 5

            # Left prise en passant
            self.define_prise_en_passant_move(piece, row, column, row_to_check, column - 1, final_row, boolean)
            # Right prise en passant
            self.define_prise_en_passant_move(piece, row, column, row_to_check, column + 1, final_row, boolean)

        def knight_moves():
            # A Knight has a maximum of 8 allowed moves
            allowed_moves = [
                (row + allowed_move_row, column + allowed_move_column)
                for x, y in [(1, 2), (2, 1)]  # Magnitudes
                for allowed_move_row, allowed_move_column in [(x, y), (x, -y), (-x, y), (-x, -y)]  # Directions
            ]

            self.is_in_range_is_empty_or_has_opponent_piece_is_in_check(piece, row, column, allowed_moves, boolean)

        def straightline_moves(increments):
            for increment in increments:
                row_increment, column_increment = increment
                allowed_move_row = row + row_increment
                allowed_move_column = column + column_increment

                while True:
                    if Square.is_in_range(allowed_move_row, allowed_move_column):
                        base_square = Square(row, column)
                        final_square_piece = self.squares[allowed_move_row][allowed_move_column].piece
                        final_square = Square(allowed_move_row, allowed_move_column, final_square_piece)
                        move = Move(base_square, final_square)

                        if self.squares[allowed_move_row][allowed_move_column].is_empty():
                            if boolean:
                                if not self.is_in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                        # Check if there's an opponent piece on the way
                        elif self.squares[allowed_move_row][allowed_move_column].has_opponent_piece(piece.color):
                            if boolean:
                                if not self.is_in_check(piece, move):
                                    piece.add_move(move)
                            else:
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
            self.is_in_range_is_empty_or_has_opponent_piece_is_in_check(piece, row, column, bordering_squares, boolean)

            # TODO PAT, STALEMATE AND CHECKMATE
            # Castling
            if not piece.has_moved:
                # King Castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    self.prepare_castling(piece, right_rook, row, column, 5, 6, 7, boolean)
                # Queen Castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    self.prepare_castling(piece, left_rook, row, column, 1, 3, 4, boolean)

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

    def is_in_check(self, piece, move):
        temporary_piece = copy.deepcopy(piece)
        temporary_board = copy.deepcopy(self)
        temporary_board.apply_move_on_screen(temporary_piece, move, not_allowed=True)

        for row in range(ROWS):
            for column in range(COLUMNS):
                if temporary_board.squares[row][column].has_opponent_piece(piece.color):
                    piece_from_temporary_board = temporary_board.squares[row][column].piece
                    temporary_board.calculate_allowed_moves(piece_from_temporary_board, row, column, boolean=False)

                    for temporary_legal_moves in piece_from_temporary_board.legal_moves:
                        if isinstance(temporary_legal_moves.final_square.piece, King):
                            return True

        return False

    def is_checkmate(self, piece, move):
        if isinstance(piece, King) and self.is_in_check(piece, move) and not piece.legal_moves:
            return True

        return False

    def generate_random_ai_valid_moves(self, next_player_color):
        valid_moves = []
        # print(f'Valid moves before treatment : {valid_moves}')
        for row in range(ROWS):
            for column in range(COLUMNS):
                square = self.squares[row][column]
                if square.has_piece():
                    piece = square.piece
                    if piece.color == next_player_color:
                        self.calculate_allowed_moves(piece, row, column)
                        if piece.legal_moves:
                            # print(piece, piece.legal_moves)
                            valid_moves.append([piece, row, column, piece.legal_moves])
        # print(f'Valid moves after treatment : {valid_moves}')
        ai_move = find_random_move(valid_moves)
        ai_piece_to_move = ai_move[0]
        ai_piece_row = ai_move[1]
        ai_piece_column = ai_move[2]
        ai_move_to_do = ai_move[3][random.randint(0, len(ai_move[3]) - 1)]
        # print(f'AI selected piece : {ai_piece_to_move} and move : {ai_move_to_do}')

        for row in range(ROWS):
            for column in range(COLUMNS):
                if row == ai_piece_row and column == ai_piece_column:
                    if self.validate_move(ai_piece_to_move, ai_move_to_do):
                        self.apply_move_on_screen(ai_piece_to_move, ai_move_to_do)
