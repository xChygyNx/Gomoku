import pytest
import typing as t
import random

from src.exceptions import BusyCell
from src.store.color import Color
from src.const import BOARD_SIZE


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
    def test_create_board(self,
                          new_gomoku):
        assert len(new_gomoku.board) == 19
        assert board_size(new_gomoku.board) == 361
        assert isinstance(new_gomoku.board[random.randint(0, 18)][random.randint(0, 18)], Color)
        assert board_is_empty(new_gomoku.board)
        assert new_gomoku.now_turn == Color.WHITE

    def test_gomoku_turn(self,
                    new_gomoku):
        x, y = random.randint(0, 18), random.randint(0, 18)
        new_gomoku.make_turn(x, y)

        assert not board_is_empty(new_gomoku.board)
        assert new_gomoku.board[x][y] == Color.WHITE
        assert new_gomoku.now_turn == Color.BLACK

        with pytest.raises(BusyCell) as error:
            new_gomoku.make_turn(x, y)
        assert error.value.args[0] == f'Cell ({x} : {y}) is busy'

    def test_turn_around(self,
                         new_gomoku):
        x, y = 10, 10
        turn_around(new_gomoku.board, x, y, 3, Color.BLACK)
        assert new_gomoku.board[x][y] == Color.EMPTY
        assert new_gomoku.board[x-3][y] == Color.BLACK
        assert new_gomoku.board[x-3][y-3] == Color.BLACK
        assert new_gomoku.board[x][y-3] == Color.BLACK
        assert new_gomoku.board[x+3][y-3] == Color.BLACK
        assert new_gomoku.board[x+3][y] == Color.BLACK
        assert new_gomoku.board[x+3][y+3] == Color.BLACK
        assert new_gomoku.board[x][y+3] == Color.BLACK
        assert new_gomoku.board[x-3][y+3] == Color.BLACK

        new_gomoku.reset_board()
        x, y = 0, 0
        turn_around(new_gomoku.board, x, y, 3, Color.WHITE)
        assert new_gomoku.board[x - 3][y] == Color.EMPTY
        assert new_gomoku.board[x - 3][y - 3] == Color.EMPTY
        assert new_gomoku.board[x][y - 3] == Color.EMPTY
        assert new_gomoku.board[x + 3][y - 3] == Color.EMPTY
        assert new_gomoku.board[x + 3][y] == Color.WHITE
        assert new_gomoku.board[x + 3][y + 3] == Color.WHITE
        assert new_gomoku.board[x][y + 3] == Color.WHITE
        assert new_gomoku.board[x - 3][y + 3] == Color.EMPTY

    def test_correct_capture(self,
                             new_gomoku):
        x, y = 10, 10
        turn_around(new_gomoku.board, x, y, 3, Color.WHITE)
        turn_around(new_gomoku.board, x, y, 2, Color.BLACK)
        turn_around(new_gomoku.board, x, y, 1, Color.BLACK)
        assert new_gomoku.board[x - 2][y] == Color.BLACK
        assert new_gomoku.board[x - 1][y] == Color.BLACK
        assert new_gomoku.board[x - 2][y - 2] == Color.BLACK
        assert new_gomoku.board[x - 1][y - 1] == Color.BLACK
        assert new_gomoku.board[x][y - 2] == Color.BLACK
        assert new_gomoku.board[x][y - 1] == Color.BLACK
        assert new_gomoku.board[x + 2][y - 2] == Color.BLACK
        assert new_gomoku.board[x + 1][y - 1] == Color.BLACK
        assert new_gomoku.board[x + 2][y] == Color.BLACK
        assert new_gomoku.board[x + 1][y] == Color.BLACK
        assert new_gomoku.board[x + 2][y + 2] == Color.BLACK
        assert new_gomoku.board[x + 1][y + 1] == Color.BLACK
        assert new_gomoku.board[x][y + 2] == Color.BLACK
        assert new_gomoku.board[x][y + 1] == Color.BLACK
        assert new_gomoku.board[x - 2][y + 2] == Color.BLACK
        assert new_gomoku.board[x - 1][y + 1] == Color.BLACK

        new_gomoku.make_turn(x, y)
        assert new_gomoku.board[x - 2][y] == Color.EMPTY
        assert new_gomoku.board[x - 1][y] == Color.EMPTY
        assert new_gomoku.board[x - 2][y - 2] == Color.EMPTY
        assert new_gomoku.board[x - 1][y - 1] == Color.EMPTY
        assert new_gomoku.board[x][y - 2] == Color.EMPTY
        assert new_gomoku.board[x][y - 1] == Color.EMPTY
        assert new_gomoku.board[x + 2][y - 2] == Color.EMPTY
        assert new_gomoku.board[x + 1][y - 1] == Color.EMPTY
        assert new_gomoku.board[x + 2][y] == Color.EMPTY
        assert new_gomoku.board[x + 1][y] == Color.EMPTY
        assert new_gomoku.board[x + 2][y + 2] == Color.EMPTY
        assert new_gomoku.board[x + 1][y + 1] == Color.EMPTY
        assert new_gomoku.board[x][y + 2] == Color.EMPTY
        assert new_gomoku.board[x][y + 1] == Color.EMPTY
        assert new_gomoku.board[x - 2][y + 2] == Color.EMPTY
        assert new_gomoku.board[x - 1][y + 1] == Color.EMPTY
