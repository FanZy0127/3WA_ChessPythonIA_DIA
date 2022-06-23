class Move:

    def __init__(self, base_square, final_square):
        self.base_square = base_square
        self.final_square = final_square

    def __eq__(self, other):
        return self.base_square == other.base_square and self.final_square == other.final_square
