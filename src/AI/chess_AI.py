import copy
import math
import random
from src.consts.consts import *

CHECKMATE = math.inf
STALEMATE = 0


# Function returning a random move to do for the AI.
def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


# Function returning the best move for the AI, based on material, 1 depth ahead (greedy algo).
def find_the_best_move(board, valid_moves):
    max_score = -CHECKMATE
    best_move = None
    board_score = 0
    piece_to_move = None

    temporary_board = copy.deepcopy(board)

    for moves in valid_moves:
        piece = moves[0]
        temporary_piece = copy.deepcopy(piece)

        for move in moves[3]:

            temporary_board.apply_move_on_screen(temporary_piece, move, not_allowed=True)

            if temporary_board.is_checkmate(temporary_piece, move):
                max_score = CHECKMATE
            elif temporary_board.is_stalemate(temporary_piece, move):
                max_score = STALEMATE
            else:
                board_score = calculate_board_score_material(temporary_board)

            if board_score > max_score:
                max_score = board_score
                best_move = move
                piece_to_move = piece

    return piece_to_move, best_move


# Function to calculate the current board score
def calculate_board_score_material(board):
    score_material = 0

    for row in range(ROWS):
        for column in range(COLUMNS):
            if board.squares[row][column].has_piece():
                piece = board.squares[row][column].piece
                score_material += piece.value
    # print(f'Score Material : {score_material}')
    return score_material
