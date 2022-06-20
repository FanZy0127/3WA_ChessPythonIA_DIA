import math
import os


class Piece:

    def __init__(self, name, color, theoric_value, image_url=None, image_rectangle=None):

        value_sign = 1 if color == 'white' else -1

        self.name = name
        self.color = color
        self.value = theoric_value * value_sign
        self.moves = []
        self.has_moved = False
        self.image = image_url
        self.set_image()
        self.texture_rectangle = image_rectangle

    def set_image(self, size=80):
        self.image = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name.lower()}.png'
        )

    def add_moves(self, move):
        self.moves.append(move)


class Pawn(Piece):

    def __init__(self, color):
        self.direction = -1 if color == 'white' else 1
        super().__init__('Pawn', color, 1.0)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('Rook', color, 5.0)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('Knight', color, 3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('Bishop', color, 3.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('Queen', color, 9.0)


class King(Piece):
    def __init__(self, color):
        super().__init__('King', color, math.inf)
