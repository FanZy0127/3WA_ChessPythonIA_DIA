from src.build.move import *
from src.build.square import *


def test_get_move_base_square():
    base_square = Square(1, 1)
    final_square = Square(3, 1)
    move = Move(base_square, final_square)
    assert move.base_square.row == 1 and move.base_square.column == 1


def test_get_move_final_square():
    base_square = Square(1, 5)
    final_square = Square(3, 5)
    move = Move(base_square, final_square)
    assert move.final_square.row == 3 and move.final_square.column == 5


def test_move_base_square_different_of_move_final_square():
    base_square = Square(1, 5)
    final_square = Square(3, 5)
    move = Move(base_square, final_square)
    assert move.base_square != move.final_square
