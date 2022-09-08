import math
import os


class Piece:

    def __init__(self, name, color, theoric_value, image_url=None, image_rectangle=None):

        value_sign = 1 if color == 'white' else -1
        self.name = name
        self.color = color
        self.value = theoric_value * value_sign
        self.legal_moves = []
        self.has_moved = False
        self.image = image_url
        self.set_image()
        self.texture_rectangle = image_rectangle
        self.is_promoted = False

    def __eq__(self, other):
        return self.name == other.name

    def set_image(self, size=80):
        self.image = os.path.join(
            f'../assets/images/imgs-{size}px/{self.color}_{self.name.lower()}.png'
        )

    def add_move(self, move):
        self.legal_moves.append(move)

    def reset_moves(self):
        self.legal_moves = []  # Reset of the legal moves array for the next turn


class Pawn(Piece):

    def __init__(self, color):
        self.direction = -1 if color == 'white' else 1
        self.prise_en_passant = False
        super().__init__('Pawn', color, 1.0)

    @staticmethod
    def get_promotion_choices(color):
        return [
            Knight(color),
            Bishop(color),
            Rook(color),
            Queen(color)
        ]

    @staticmethod
    def set_promotion(clicked_button, color):
        # Parsing of the image path to get the Object class name
        if '.png' in clicked_button:
            clicked_button = os.path.basename(clicked_button)[6:-4].capitalize()

        # eval will return the piece class with the good color : ie. Knight('white')
        return eval(clicked_button)(color)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('Knight', color, 3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('Bishop', color, 3.0)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('Rook', color, 5.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('Queen', color, 9.0)


class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('King', color, 9999)
