import math
import random
from src.consts.consts import *

CHECKMATE = math.inf
STALEMATE = 0


# Function returning a random move to do for the AI.
def find_random_move(valid_moves):
    return valid_moves[random.randint(0, len(valid_moves) - 1)]


# Function returning the best move for the AI, based on material.
def find_the_best_move(board, valid_moves):
    max_score = -CHECKMATE
    best_move = None
    board_score = 0

    for move in valid_moves:
        board.apply_move_on_screen(move[0], move[3])

        if board.is_checkmate():
            max_score = CHECKMATE
        elif board.is_stalemate():
            max_score = STALEMATE
        else:
            board_score = calculate_board_score_material(board)

        if board_score > max_score:
            board_score = max_score
            best_move = move


# Function to calculate the current board score
def calculate_board_score_material(board):
    score_material = 0

    for row in range(ROWS):
        for column in range(COLUMNS):
            if board.squares[row][column].has_piece():
                piece = board.squares[row][column].piece
                score_material += piece.value

    return score_material
