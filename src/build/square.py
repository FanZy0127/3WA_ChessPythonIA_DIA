
class Square:

    def __init__(self, row, column, piece=None):
        self.row = row
        self.column = column
        self.piece = piece

    def has_piece(self):
        return self.piece is not None
