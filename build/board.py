from consts.consts import *
from build.square import Square

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for column in range(COLUMNS)]
        self._instantiate()

    def _instantiate(self):

        for row in range(ROWS):
            for column in range(COLUMNS):
                self.squares[row][column] = Square(row, column)

    def _add_pieces(self, color):
        pass
