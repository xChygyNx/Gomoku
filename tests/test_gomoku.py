import pytest
import typing as t
import random

from src.exceptions import BusyCell
from src.store.color import Color


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
    board[x-distance][y] = color
    board[x-distance][y-distance] = color
    board[x][y-distance] = color
    try:
        board[x+distance][y-distance] = color
    except IndexError:
        pass
    try:
        board[x+distance][y] = color
    except IndexError:
        pass
    try:
        board[x+distance][y+distance] = color
    except IndexError:
        pass
    try:
        board[x][y+distance] = color
    except IndexError:
        pass
    try:
        board[x-distance][y+distance] = color
    except IndexError:
        pass


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
