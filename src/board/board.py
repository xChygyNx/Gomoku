import re
import typing as t

from src.const import LETTERS
from src.gomoku.structures import Color
from src.exceptions import *


class Board:
    def __init__(self, **kwargs):
        self.board_size = kwargs.get('board_size')
        self.board = [[Color.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.check_init()

    def check_init(self) -> None:
        if self.board_size is None:
            raise ConfigGomokuError('Board_size of Gomoku is unfilled')

    def convert_to_str_coordinate(self, x: int, y: int) -> str:
        if x > self.board_size or y > self.board_size:
            raise ValueError(f'Coordinate ({x}, {y}) absence on board')
        return LETTERS[x] + str(y)

    def convert_to_int_coordinate(self, coord: str) -> t.Tuple[int, int]:
        if re.match('[a-z]', coord[0]) is None or re.match('^\d{1:2}$', coord[1:]) is None:
            raise ValueError(f'Coordinate {coord} is invalid')
        x = LETTERS.find(coord[0])
        y = int(coord[1:])
        if x > self.board_size or y > self.board_size:
            raise ValueError(f'Coordinate {coord} absence on board')
        return x, y

    def checks(self, x: int, y: int):
        self.check_free_pos(x, y)
        self.check_win()
        self.check_forbidden_turn(x, y)

    def check_free_pos(self, x: int, y: int):
        if self.board[x][y] != Color.EMPTY:
            raise BusyCell(x, y)

    def check_win(self):
        self.check_win_horizontals()
        self.check_win_verticals()
        self.check_win_diagonals_1()
        self.check_win_diagonals_2()

    def check_win_horizontals(self):
        for line in self.board:
            now_seq = Color.EMPTY
            seq_len = 0
            for pos in line:
                if pos == now_seq:
                    seq_len += 1
                else:
                    seq_len = 1
                if seq_len == 5 and pos != Color.EMPTY:
                    exception = BlackPlayerWinException if pos == Color.BLACK else WhitePlayerWinException
                    raise exception()

    def check_win_verticals(self):
        for x in range(self.board_size):
            now_seq = Color.EMPTY
            seq_len = 0
            for y in range(self.board_size):
                if self.board[x][y] == now_seq:
                    seq_len += 1
                else:
                    seq_len = 1
                if seq_len == 5 and self.board[x][y] != Color.EMPTY:
                    exception = BlackPlayerWinException if self.board[x][y] == Color.BLACK else WhitePlayerWinException
                    raise exception()

    def check_win_diagonals_1(self):
        for init_v in range(4, self.board_size):
            now_seq = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(0, init_v + 1), range(init_v, -1, -1)):
                if self.board[x][y] == now_seq:
                    seq_len += 1
                else:
                    seq_len = 1
                if seq_len == 5 and self.board[x][y] != Color.EMPTY:
                    exception = BlackPlayerWinException if self.board[x][y] == Color.BLACK else WhitePlayerWinException
                    raise exception()
        for init_h in range(1, self.board_size - 4):
            now_seq = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(init_h, self.board_size), range(self.board_size - 1, init_h - 1, -1)):
                if self.board[x][y] == now_seq:
                    seq_len += 1
                else:
                    seq_len = 1
                if seq_len == 5 and self.board[x][y] != Color.EMPTY:
                    exception = BlackPlayerWinException if self.board[x][y] == Color.BLACK else WhitePlayerWinException
                    raise exception()

    def check_win_diagonals_2(self):
        for init_h in range(self.board_size - 5, 0, -1):
            now_seq = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(init_h, self.board_size), range(0, self.board_size - init_h)):
                if self.board[x][y] == now_seq:
                    seq_len += 1
                else:
                    seq_len = 1
                if seq_len == 5 and self.board[x][y] != Color.EMPTY:
                    exception = BlackPlayerWinException if self.board[x][y] == Color.BLACK else WhitePlayerWinException
                    raise exception()
        for init_v in range(0, self.board_size - 4):
            now_seq = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(0, self.board_size - init_v), range(init_v, self.board_size)):
                if self.board[x][y] == now_seq:
                    seq_len += 1
                else:
                    seq_len = 1
                if seq_len == 5 and self.board[x][y] != Color.EMPTY:
                    exception = BlackPlayerWinException if self.board[x][y] == Color.BLACK else WhitePlayerWinException
                    raise exception()

    def check_forbidden_turn(self, x: int, y: int):
        if True:
            return
        raise ForbiddenTurn(self.convert_to_str_coordinate(x, y))
