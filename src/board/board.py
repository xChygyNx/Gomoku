import re
import typing as t

from src.const import LETTERS, WIN_SEQUENCE_LENGTH
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

    def coordinate_generator(self, coordinate: int) -> t.Generator[int]:
        for i in range(coordinate - WIN_SEQUENCE_LENGTH + 1, coordinate + WIN_SEQUENCE_LENGTH):
            if 0 <= i <= self.board_size:
                yield i

    def diagonal_coordinate_generator(self, coordinate_x: int, coordinate_y: int) -> t.Generator[t.Tuple[int, int]]:
        for i, j in zip(range(coordinate_x - WIN_SEQUENCE_LENGTH + 1, coordinate_x + WIN_SEQUENCE_LENGTH),
                        range(coordinate_y - WIN_SEQUENCE_LENGTH + 1, coordinate_y + WIN_SEQUENCE_LENGTH)):
            if 0 <= i < self.board_size and 0 <= j < self.board_size:
                yield i, j

    def alternative_diagonal_coordinate_generator(self, coordinate_x: int, coordinate_y: int) \
            -> t.Generator[t.Tuple[int, int]]:
        for i, j in zip(range(coordinate_x - WIN_SEQUENCE_LENGTH + 1, coordinate_x + WIN_SEQUENCE_LENGTH),
                        range(coordinate_y + WIN_SEQUENCE_LENGTH - 1, coordinate_y - WIN_SEQUENCE_LENGTH)):
            if 0 <= i < self.board_size and 0 <= j < self.board_size:
                yield i, j

    def checks(self, x: int, y: int, now_turn: Color):
        self.check_free_pos(x, y)
        self.check_win(x, y, now_turn)
        self.check_forbidden_turn(x, y)

    def check_free_pos(self, x: int, y: int):
        if self.board[x][y] != Color.EMPTY:
            raise BusyCell(x, y)

    def check_win(self, x: int, y: int, now_turn: Color):
        self.check_win_horizontals(x, y, now_turn)
        self.check_win_verticals(x, y, now_turn)
        self.check_win_diagonals_1(x, y, now_turn)
        self.check_win_diagonals_2(x, y, now_turn)

    def check_win_horizontals(self, x: int, y: int, now_turn: Color) -> None:
        seq_len = 0
        for x in self.coordinate_generator(x):
            if self.board[x][y] == now_turn:
                seq_len += 1
            else:
                seq_len = 0
            if seq_len == 5:
                exception = BlackPlayerWinException if now_turn == Color.BLACK else WhitePlayerWinException
                raise exception()

    def check_win_verticals(self, x: int, y: int, now_turn: Color) -> None:
        seq_len = 0
        for y in self.coordinate_generator(y):
            if self.board[x][y] == now_turn:
                seq_len += 1
            else:
                seq_len = 0
            if seq_len == 5:
                exception = BlackPlayerWinException if now_turn == Color.BLACK else WhitePlayerWinException
                raise exception()

    def check_win_diagonals_1(self, x: int, y: int, now_turn: Color) -> None:
        seq_len = 0
        for x, y in self.diagonal_coordinate_generator(x, y):
            if self.board[x][y] == now_turn:
                seq_len += 1
            else:
                seq_len = 0
            if seq_len == 5:
                exception = BlackPlayerWinException if now_turn == Color.BLACK else WhitePlayerWinException
                raise exception()

    def check_win_diagonals_2(self, x: int, y: int, now_turn: Color) -> None:
        seq_len = 0
        for x, y in self.alternative_diagonal_coordinate_generator(x, y):
            if self.board[x][y] == now_turn:
                seq_len += 1
            else:
                seq_len = 1
            if seq_len == 5:
                exception = BlackPlayerWinException if now_turn == Color.BLACK else WhitePlayerWinException
                raise exception()

    def check_forbidden_turn(self, x: int, y: int):
        if True:
            return
        # raise ForbiddenTurn(self.convert_to_str_coordinate(x, y))
