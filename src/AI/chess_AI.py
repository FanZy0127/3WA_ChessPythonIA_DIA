import copy
import math
import random
from src.consts.consts import *

CHECKMATE = math.inf
STALEMATE = 0
DEPTH = 2


# Function returning a random move to do for the AI.
def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


# Function returning the best move for the AI, based on material, 1 depth ahead (greedy algo).
# Turned it into a basic self made dirty MinMax algorithm, which ends up being SUPER SLOW.
def find_the_best_move(board, valid_moves, player_color):
    opponents_min_max_score = CHECKMATE
    best_move = None
    piece_to_move = None
    opponents_color = 'white' if player_color == 'black' else 'black'
    random.shuffle(valid_moves)
    temporary_board = copy.deepcopy(board)

    for moves in valid_moves:
        piece = moves[0]
        temporary_piece = copy.deepcopy(piece)

        for move in moves[3]:
            temporary_board.apply_move_on_screen(temporary_piece, move, not_allowed=True)
            opponents_valid_moves = board.get_valid_moves(opponents_color)
            opponents_temporary_board = copy.deepcopy(temporary_board)

            if temporary_board.is_stalemate(piece, move):
                opponents_max_score = STALEMATE
            elif temporary_board.is_checkmate(piece, move):
                opponents_max_score = -CHECKMATE
            else:
                opponents_max_score = -CHECKMATE

                for opponents_moves in opponents_valid_moves:
                    opponents_piece = opponents_moves[0]
                    opponents_temporary_piece = copy.deepcopy(opponents_piece)

                    for opponents_move in opponents_moves[3]:
                        opponents_temporary_board.apply_move_on_screen(
                            opponents_temporary_piece, opponents_move, not_allowed=True)
                        opponents_temporary_board.get_valid_moves(opponents_color)
                        if opponents_temporary_board.is_checkmate(opponents_temporary_piece, opponents_move):
                            board_score = CHECKMATE
                        elif opponents_temporary_board.is_stalemate(opponents_temporary_piece, opponents_move):
                            board_score = STALEMATE
                        else:
                            board_score = calculate_board_score_material(opponents_temporary_board)
                            print(f'NEW BOARD SCORE : {board_score}')

                        if board_score > opponents_max_score:
                            opponents_max_score = board_score

            if opponents_max_score < opponents_min_max_score:
                opponents_min_max_score = opponents_max_score
                best_move = move
                piece_to_move = piece

    return piece_to_move, best_move


# Function to calculate the current board score (naive solution)
def calculate_board_score_material(board):
    score_material = 0

    for row in range(ROWS):
        for column in range(COLUMNS):
            if board.squares[row][column].has_piece():
                piece = board.squares[row][column].piece
                score_material += piece.value

    return score_material
