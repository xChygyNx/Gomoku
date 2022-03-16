import pytest
import typing as t
import random

from src.exceptions import BusyCell
from src.store.color import Color
from src.const import BOARD_SIZE
from src.store.gomoku import Gomoku


def board_size(board: t.List[t.List[Color]]) -> int:
    size = 0
    for line in board:
        size += len(line)
    return size

def board_is_empty(board: t.List[t.List[Color]]) -> bool:
    for line in board:
        for pos in line:
            if pos.value != 0:
                return False
    return True

def turn_around(board: t.List[t.List[Color]], x: int, y: int, distance: int, color: Color) -> None:
    if x >= distance:
        board[x-distance][y] = color
    if y >= distance:
        board[x][y-distance] = color
    if x >= distance and y >= distance:
        board[x-distance][y-distance] = color
    if y >= distance and x + distance <= BOARD_SIZE:
            board[x+distance][y-distance] = color
    if x + distance <= BOARD_SIZE:
        board[x+distance][y] = color
    if x + distance <= BOARD_SIZE and y + distance <= BOARD_SIZE:
        board[x+distance][y+distance] = color
    if y + distance <= BOARD_SIZE:
        board[x][y+distance] = color
    if x >= distance:
        board[x-distance][y+distance] = color


class TestGomoku:
    def test_create_board(self):
        gomoku = Gomoku()
        assert len(gomoku.board) == 19
        assert board_size(gomoku.board) == 361
        assert isinstance(gomoku.board[random.randint(0, 18)][random.randint(0, 18)], Color)
        assert board_is_empty(gomoku.board)
        assert gomoku.now_turn == Color.WHITE

    def test_gomoku_turn(self,
                         mini_gomoku):
        x, y = random.randint(0, 6), random.randint(0, 6)
        mini_gomoku.make_turn(x, y)

        assert not board_is_empty(mini_gomoku.board)
        assert mini_gomoku.board[x][y] == Color.WHITE
        assert mini_gomoku.now_turn == Color.BLACK

        with pytest.raises(BusyCell) as error:
            mini_gomoku.make_turn(x, y)
        assert error.value.args[0] == f'Cell ({x} : {y}) is busy'

    def test_turn_around(self,
                         mini_gomoku):
        x, y = 3, 3
        turn_around(mini_gomoku.board, x, y, 3, Color.BLACK)
        assert mini_gomoku.board[x][y] == Color.EMPTY
        assert mini_gomoku.board[x - 3][y] == Color.BLACK
        assert mini_gomoku.board[x - 3][y - 3] == Color.BLACK
        assert mini_gomoku.board[x][y - 3] == Color.BLACK
        assert mini_gomoku.board[x + 3][y - 3] == Color.BLACK
        assert mini_gomoku.board[x + 3][y] == Color.BLACK
        assert mini_gomoku.board[x + 3][y + 3] == Color.BLACK
        assert mini_gomoku.board[x][y + 3] == Color.BLACK
        assert mini_gomoku.board[x - 3][y + 3] == Color.BLACK

        mini_gomoku.reset_board()
        x, y = 0, 0
        turn_around(mini_gomoku.board, x, y, 3, Color.WHITE)
        assert mini_gomoku.board[x - 3][y] == Color.EMPTY
        assert mini_gomoku.board[x - 3][y - 3] == Color.EMPTY
        assert mini_gomoku.board[x][y - 3] == Color.EMPTY
        assert mini_gomoku.board[x + 3][y - 3] == Color.EMPTY
        assert mini_gomoku.board[x + 3][y] == Color.WHITE
        assert mini_gomoku.board[x + 3][y + 3] == Color.WHITE
        assert mini_gomoku.board[x][y + 3] == Color.WHITE
        assert mini_gomoku.board[x - 3][y + 3] == Color.EMPTY

    def test_correct_capture(self,
                             mini_gomoku):
        x, y = 3, 3
        turn_around(mini_gomoku.board, x, y, 3, Color.WHITE)
        turn_around(mini_gomoku.board, x, y, 2, Color.BLACK)
        turn_around(mini_gomoku.board, x, y, 1, Color.BLACK)
        assert mini_gomoku.board[x - 2][y] == Color.BLACK
        assert mini_gomoku.board[x - 1][y] == Color.BLACK
        assert mini_gomoku.board[x - 2][y - 2] == Color.BLACK
        assert mini_gomoku.board[x - 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x][y - 2] == Color.BLACK
        assert mini_gomoku.board[x][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y - 2] == Color.BLACK
        assert mini_gomoku.board[x + 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y] == Color.BLACK
        assert mini_gomoku.board[x + 1][y] == Color.BLACK
        assert mini_gomoku.board[x + 2][y + 2] == Color.BLACK
        assert mini_gomoku.board[x + 1][y + 1] == Color.BLACK
        assert mini_gomoku.board[x][y + 2] == Color.BLACK
        assert mini_gomoku.board[x][y + 1] == Color.BLACK
        assert mini_gomoku.board[x - 2][y + 2] == Color.BLACK
        assert mini_gomoku.board[x - 1][y + 1] == Color.BLACK

        mini_gomoku.make_turn(x, y)
        assert mini_gomoku.board[x - 2][y] == Color.EMPTY
        assert mini_gomoku.board[x - 1][y] == Color.EMPTY
        assert mini_gomoku.board[x - 2][y - 2] == Color.EMPTY
        assert mini_gomoku.board[x - 1][y - 1] == Color.EMPTY
        assert mini_gomoku.board[x][y - 2] == Color.EMPTY
        assert mini_gomoku.board[x][y - 1] == Color.EMPTY
        assert mini_gomoku.board[x + 2][y - 2] == Color.EMPTY
        assert mini_gomoku.board[x + 1][y - 1] == Color.EMPTY
        assert mini_gomoku.board[x + 2][y] == Color.EMPTY
        assert mini_gomoku.board[x + 1][y] == Color.EMPTY
        assert mini_gomoku.board[x + 2][y + 2] == Color.EMPTY
        assert mini_gomoku.board[x + 1][y + 1] == Color.EMPTY
        assert mini_gomoku.board[x][y + 2] == Color.EMPTY
        assert mini_gomoku.board[x][y + 1] == Color.EMPTY
        assert mini_gomoku.board[x - 2][y + 2] == Color.EMPTY
        assert mini_gomoku.board[x - 1][y + 1] == Color.EMPTY

    def test_not_filled_capture(self,
                                mini_gomoku):
        x, y = 3, 3
        turn_around(mini_gomoku.board, x, y, 3, Color.WHITE)
        mini_gomoku.board[x - 2][y] = Color.BLACK
        mini_gomoku.board[x - 1][y - 1] = Color.BLACK
        mini_gomoku.board[x][y - 1] = Color.BLACK
        mini_gomoku.board[x + 2][y - 2] = Color.BLACK
        mini_gomoku.board[x + 2][y] = Color.BLACK
        mini_gomoku.board[x + 2][y + 2] = Color.BLACK
        mini_gomoku.board[x][y + 1] = Color.BLACK
        mini_gomoku.board[x - 2][y + 2] = Color.BLACK

        assert mini_gomoku.board[x - 2][y] == Color.BLACK
        assert mini_gomoku.board[x - 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y - 2] == Color.BLACK
        assert mini_gomoku.board[x + 2][y] == Color.BLACK
        assert mini_gomoku.board[x + 2][y + 2] == Color.BLACK
        assert mini_gomoku.board[x][y + 1] == Color.BLACK
        assert mini_gomoku.board[x - 2][y + 2] == Color.BLACK

        mini_gomoku.make_turn(x, y)
        assert mini_gomoku.board[x - 2][y] == Color.BLACK
        assert mini_gomoku.board[x - 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y - 2] == Color.BLACK
        assert mini_gomoku.board[x + 2][y] == Color.BLACK
        assert mini_gomoku.board[x + 2][y + 2] == Color.BLACK
        assert mini_gomoku.board[x][y + 1] == Color.BLACK
        assert mini_gomoku.board[x - 2][y + 2] == Color.BLACK

    def test_turn_in_trap(self,
                          mini_gomoku):
        x, y = 3, 3
        turn_around(mini_gomoku.board, x, y, 3, Color.WHITE)
        turn_around(mini_gomoku.board, x, y, 1, Color.BLACK)
        mini_gomoku.make_turn(x - 2, y, Color.WHITE)
        mini_gomoku.make_turn(x - 2, y - 2, Color.WHITE)
        mini_gomoku.make_turn(x, y - 2, Color.WHITE)
        mini_gomoku.make_turn(x + 2, y - 2, Color.WHITE)
        mini_gomoku.make_turn(x + 2, y, Color.WHITE)
        mini_gomoku.make_turn(x + 2, y + 2, Color.WHITE)
        mini_gomoku.make_turn(x, y + 2, Color.WHITE)
        mini_gomoku.make_turn(x - 2, y + 2, Color.WHITE)

        assert mini_gomoku.board[x - 2][y] == Color.WHITE
        assert mini_gomoku.board[x - 1][y] == Color.BLACK
        assert mini_gomoku.board[x - 2][y - 2] == Color.WHITE
        assert mini_gomoku.board[x - 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x][y - 2] == Color.WHITE
        assert mini_gomoku.board[x][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y - 2] == Color.WHITE
        assert mini_gomoku.board[x + 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y] == Color.WHITE
        assert mini_gomoku.board[x + 1][y] == Color.BLACK
        assert mini_gomoku.board[x + 2][y + 2] == Color.WHITE
        assert mini_gomoku.board[x + 1][y + 1] == Color.BLACK
        assert mini_gomoku.board[x][y + 2] == Color.WHITE
        assert mini_gomoku.board[x][y + 1] == Color.BLACK
        assert mini_gomoku.board[x - 2][y + 2] == Color.WHITE
        assert mini_gomoku.board[x - 1][y + 1] == Color.BLACK

        mini_gomoku.make_turn(x, y)

        assert mini_gomoku.board[x - 2][y] == Color.WHITE
        assert mini_gomoku.board[x - 1][y] == Color.BLACK
        assert mini_gomoku.board[x - 2][y - 2] == Color.WHITE
        assert mini_gomoku.board[x - 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x][y - 2] == Color.WHITE
        assert mini_gomoku.board[x][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y - 2] == Color.WHITE
        assert mini_gomoku.board[x + 1][y - 1] == Color.BLACK
        assert mini_gomoku.board[x + 2][y] == Color.WHITE
        assert mini_gomoku.board[x + 1][y] == Color.BLACK
        assert mini_gomoku.board[x + 2][y + 2] == Color.WHITE
        assert mini_gomoku.board[x + 1][y + 1] == Color.BLACK
        assert mini_gomoku.board[x][y + 2] == Color.WHITE
        assert mini_gomoku.board[x][y + 1] == Color.BLACK
        assert mini_gomoku.board[x - 2][y + 2] == Color.WHITE
        assert mini_gomoku.board[x - 1][y + 1] == Color.BLACK
