from src.consts.consts import *


class Translator:

    @staticmethod
    def translate_board_matrix_to_fen(board_matrix: list, player_color: str):
        fen_string = ''

        for row_matrix in board_matrix:
            empty_squares = 0

            for square in row_matrix:

                piece_name = ''

                if square == 'empty':
                    empty_squares += 1
                else:
                    if square[0] == 'Pawn':
                        piece_name = 'p'
                    elif square[0] == 'Rook':
                        piece_name = 'r'
                    elif square[0] == 'Knight':
                        piece_name = 'n'
                    elif square[0] == 'Bishop':
                        piece_name = 'b'
                    elif square[0] == 'Queen':
                        piece_name = 'q'
                    elif square[0] == 'King':
                        piece_name = 'k'

                if square[1] != 'black':
                    piece_name = piece_name.upper()
                else:
                    piece_name = piece_name.lower()

                if piece_name != '' and (0 < empty_squares < 8):
                    fen_string += str(empty_squares)
                    fen_string += piece_name
                    empty_squares = 0
                elif piece_name != '' and empty_squares == 0:
                    fen_string += piece_name
                elif empty_squares == 8:
                    fen_string += str(empty_squares)

            if 8 > empty_squares > 0:
                fen_string += str(empty_squares)

            fen_string += '/'
        fen_string = fen_string.rstrip(fen_string[-1])

        return fen_string + (' w' if player_color == 'white' else ' b')

    @staticmethod
    def translate_network_best_move_to_matrix_move(network_best_move):
        move_matrix = []
        count = 0
        base_square_column = 0
        base_square_row = 0
        final_square_column = 0
        final_square_row = 0

        for character in str(network_best_move):
            if count in range(0, 2):
                if character.isalpha():
                    base_square_column = SQUARE_COLUMN_INDEXES[character]
                if character.isdigit():
                    base_square_row = SQUARE_ROW_INDEXES[character]
            elif count in range(2, 4):
                if character.isalpha():
                    final_square_column = SQUARE_COLUMN_INDEXES[character]
                if character.isdigit():
                    final_square_row = SQUARE_ROW_INDEXES[character]
            count = count + 1

        move_matrix.append([base_square_row, base_square_column])
        move_matrix.append([final_square_row, final_square_column])

        return move_matrix

