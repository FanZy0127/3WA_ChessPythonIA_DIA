
class Square:

    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def has_piece(self):
        return self.piece is not None

    def is_empty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_opponent_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def is_empty_or_has_an_opponent_piece(self, color):
        return self.is_empty() or self.has_opponent_piece(color)

    @staticmethod
    def is_in_range(*args):
        for arg in args:
            if arg not in range(8):
                return False

        return True
