# File containing main constants necessary to construct the game
import math
# Screen dimensions
HEIGHT = 960
WIDTH = 960

# Board dimensions
ROWS = 8
COLUMNS = 8
SQUARE_SIZE = WIDTH // COLUMNS

CHECKMATE = math.inf
STALEMATE = 0
# Depth the neural network will dig into for the best possible move
DEPTH = 6

SQUARE_COLUMN_INDEXES = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}

SQUARE_ROW_INDEXES = {
    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0
}
