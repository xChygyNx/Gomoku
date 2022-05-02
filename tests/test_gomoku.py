import pytest
import typing as t
import random
from unittest.mock import patch, MagicMock

from src.exceptions import BusyCell
from src.gomoku.structures import Color
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
        board[x - distance][y] = color
    if y >= distance:
        board[x][y - distance] = color
    if x >= distance and y >= distance:
        board[x - distance][y - distance] = color
    if y >= distance and x + distance <= BOARD_SIZE:
        board[x + distance][y - distance] = color
    if x + distance <= BOARD_SIZE:
        board[x + distance][y] = color
    if x + distance <= BOARD_SIZE and y + distance <= BOARD_SIZE:
        board[x + distance][y + distance] = color
    if y + distance <= BOARD_SIZE:
        board[x][y + distance] = color
    if x >= distance:
        board[x - distance][y + distance] = color


class TestGomoku:
    def test_create_board(self,
                          normal_gomoku):
        assert len(normal_gomoku.board) == 19
        assert board_size(normal_gomoku.board) == 361
        assert isinstance(normal_gomoku.board[random.randint(0, 18)][random.randint(0, 18)], Color)
        assert board_is_empty(normal_gomoku.board)
        assert normal_gomoku.now_turn == Color.WHITE

    def test_gomoku_turn(self,
                         mini_gomoku):
        y = random.randint(1, 7)
        x_int = random.randint(0, 6)
        x = chr(ord('a') + x_int)
        pos = x + str(y)
        mini_gomoku.make_turn(position=pos)

        assert not board_is_empty(mini_gomoku.board)
        assert mini_gomoku.board[x_int][y - 1] == Color.WHITE
        assert mini_gomoku.now_turn == Color.BLACK

        with pytest.raises(BusyCell) as error:
            mini_gomoku.make_turn(position=pos)
        assert error.value.args[0] == f'Cell ({x_int} : {y - 1}) is busy'

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
        mini_gomoku.win_by_capture = MagicMock(return_value=False)
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

        mini_gomoku.make_turn(position='d4')
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

        mini_gomoku.make_turn(position='d4')
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
        mini_gomoku.make_turn(position='b4', color='white')
        mini_gomoku.make_turn(position='b2', color='white')
        mini_gomoku.make_turn(position='d2', color='white')
        mini_gomoku.make_turn(position='f2', color='white')
        mini_gomoku.make_turn(position='f4', color='white')
        mini_gomoku.make_turn(position='f6', color='white')
        mini_gomoku.make_turn(position='d6', color='white')
        mini_gomoku.make_turn(position='b6', color='white')

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

        mini_gomoku.make_turn(position='d4')

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

    @patch('src.gomoku.gomoku.Gomoku.check_horizontals')
    @patch('src.gomoku.gomoku.Gomoku.check_verticals')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_1')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_2')
    def test_check_for_horizontal_white_win(self,
                                            check_diagonal2_mock: MagicMock,
                                            check_diagonal1_mock: MagicMock,
                                            check_verticals_mock: MagicMock,
                                            check_horizontals_mock: MagicMock,
                                            normal_gomoku):
        check_horizontals_mock.return_value = float('inf')
        normal_gomoku.check_state()
        assert check_horizontals_mock.called
        assert check_horizontals_mock.call_count == 1
        assert not check_verticals_mock.called
        assert not check_diagonal1_mock.called
        assert not check_diagonal2_mock.called

    @patch('src.gomoku.gomoku.Gomoku.check_horizontals')
    @patch('src.gomoku.gomoku.Gomoku.check_verticals')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_1')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_2')
    def test_check_for_horizontal_black_win(self,
                                            check_diagonal2_mock: MagicMock,
                                            check_diagonal1_mock: MagicMock,
                                            check_verticals_mock: MagicMock,
                                            check_horizontals_mock: MagicMock,
                                            normal_gomoku):
        check_horizontals_mock.return_value = -1 * float('inf')
        normal_gomoku.check_state()
        assert check_horizontals_mock.called
        assert check_horizontals_mock.call_count == 1
        assert not check_verticals_mock.called
        assert not check_diagonal1_mock.called
        assert not check_diagonal2_mock.called

    @patch('src.gomoku.gomoku.Gomoku.check_horizontals')
    @patch('src.gomoku.gomoku.Gomoku.check_verticals')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_1')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_2')
    def test_check_for_vertical_white_win(self,
                                          check_diagonal2_mock: MagicMock,
                                          check_diagonal1_mock: MagicMock,
                                          check_verticals_mock: MagicMock,
                                          check_horizontals_mock: MagicMock,
                                          normal_gomoku):
        check_horizontals_mock.return_value = 5
        check_verticals_mock.return_value = float('inf')
        normal_gomoku.check_state()
        assert check_horizontals_mock.called
        assert check_horizontals_mock.call_count == 1
        assert check_verticals_mock.called
        assert check_verticals_mock.call_count == 1
        assert not check_diagonal1_mock.called
        assert not check_diagonal2_mock.called

    @patch('src.gomoku.gomoku.Gomoku.check_horizontals')
    @patch('src.gomoku.gomoku.Gomoku.check_verticals')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_1')
    @patch('src.gomoku.gomoku.Gomoku.check_diagonals_2')
    def test_check_for_vertical_black_win(self,
                                          check_diagonal2_mock: MagicMock,
                                          check_diagonal1_mock: MagicMock,
                                          check_verticals_mock: MagicMock,
                                          check_horizontals_mock: MagicMock,
                                          normal_gomoku):
        check_horizontals_mock.return_value = -5
        check_verticals_mock.return_value = -1 * float('inf')
        normal_gomoku.check_state()
        assert check_horizontals_mock.called
        assert check_horizontals_mock.call_count == 1
        assert check_verticals_mock.called
        assert check_verticals_mock.call_count == 1
        assert not check_diagonal1_mock.called
        assert not check_diagonal2_mock.called

    def test_horizontal_white_win(self, normal_gomoku):
        normal_gomoku.make_turn(position='c2', color='white')
        normal_gomoku.make_turn(position='c3', color='white')
        normal_gomoku.make_turn(position='c4', color='white')
        normal_gomoku.make_turn(position='c5', color='white')
        normal_gomoku.make_turn(position='c6', color='white')
        assert normal_gomoku.check_state() == float('inf')

    def test_horizontal_black_win(self, normal_gomoku):
        normal_gomoku.make_turn(position='c2', color='black')
        normal_gomoku.make_turn(position='c3', color='black')
        normal_gomoku.make_turn(position='c4', color='black')
        normal_gomoku.make_turn(position='c5', color='black')
        normal_gomoku.make_turn(position='c6', color='black')
        assert normal_gomoku.check_state() == -1 * float('inf')

    def test_vertical_white_win(self, normal_gomoku):
        normal_gomoku.make_turn(position='f10', color='white')
        normal_gomoku.make_turn(position='g10', color='white')
        normal_gomoku.make_turn(position='h10', color='white')
        normal_gomoku.make_turn(position='i10', color='white')
        normal_gomoku.make_turn(position='j10', color='white')
        assert normal_gomoku.check_state() == float('inf')

    def test_vertical_black_win(self, normal_gomoku):
        normal_gomoku.make_turn(position='f10', color='black')
        normal_gomoku.make_turn(position='g10', color='black')
        normal_gomoku.make_turn(position='h10', color='black')
        normal_gomoku.make_turn(position='i10', color='black')
        normal_gomoku.make_turn(position='j10', color='black')
        assert normal_gomoku.check_state() == -1 * float('inf')
