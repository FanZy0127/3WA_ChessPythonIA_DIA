from src.build.move import *
from src.build.piece import *
from src.build.square import *


def test_get_piece_name():
    king_piece = King('black')
    assert king_piece.name == 'King'


def test_get_piece_color():
    king_piece = King('black')
    assert king_piece.color == 'black'


def test_get_piece_value():
    king_piece = King('white')

    if king_piece.color == 'white':
        assert king_piece.value == 9999
    else:
        assert king_piece.value == -9999


def test_get_piece_valid_moves():
    pawn_piece = Pawn('white')
    base_square = Square(6, 2)
    final_square = Square(4, 2)
    move = Move(base_square, final_square)
    pawn_piece.add_move(move)

    assert pawn_piece.legal_moves[0] == move
