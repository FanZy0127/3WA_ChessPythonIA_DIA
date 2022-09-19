from src.consts.consts import *


class Translator:

    @staticmethod
    def translate_board_matrix_to_fen(board_matrix, player_color):
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
    def translate_fen_to_board_matrix(fen_string):
        pass
