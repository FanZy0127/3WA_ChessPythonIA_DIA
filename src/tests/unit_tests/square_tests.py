from src.build.piece import *
from src.build.square import *


def test_get_square_row():
    square = Square(1, 2)
    assert square.row == 1


def test_get_square_column():
    square = Square(1, 2)
    assert square.column == 2


def test_square_has_no_piece():
    square = Square(1, 2)
    assert square.is_empty()


def test_get_square_piece_name_and_color():
    square = Square(7, 0, Rook('white'))
    assert square.has_piece() and square.piece.name == 'Rook' and square.piece.color == 'white'

