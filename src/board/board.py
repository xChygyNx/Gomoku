import typing as t

from src.const import LETTERS
from src.gomoku.structures import Color
from src.exceptions import *


class Board:

    def __init__(self, **kwargs):
        self.board_size = kwargs.get('board_size') + 1
        self.board = [[Color.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.check_init()

    def check_init(self) -> None:
        if self.board_size is None:
            raise ConfigGomokuError('Board_size of Gomoku is unfilled')

    def set_piece(self, position: str, color: str):
        x, y = self.position_to_coordinates(position)
        if color.upper() == Color.WHITE.name:
            self.board[y][x] = Color.WHITE
        else:
            self.board[y][x] = Color.BLACK

    def delete_piece(self, position: str):
        x, y = self.position_to_coordinates(position)
        self.board[y][x] = Color.EMPTY

    def coordinates_to_position(self, x: int, y: int) -> str:
        if x > self.board_size or y > self.board_size:
            raise ValueError(f'Coordinate ({x}, {y}) absence on board')
        return LETTERS[x] + str(y)

    def position_to_coordinates(self, coord: str) -> t.Tuple[int, int]:
        # if re.match('[a-z]', coord[0]) is None or re.match('^\d{1:2}$', coord[1:]) is None:
        #     raise ValueError(f'Coordinate {coord} is invalid')
        x = LETTERS.find(coord[0])
        y = self.board_size - int(coord[1:])
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

    def is_win(self):
        try:
            self.check_win()
        except (WhitePlayerWinException, BlackPlayerWinException):
            return True
        return False

    def check_win_horizontals(self):
        for line in self.board:
            seq_color = Color.EMPTY
            seq_len = 0
            for current_color in line:
                seq_color, seq_len = self._check_win_strike(current_color, seq_color, seq_len)

    def check_win_verticals(self):
        for x in range(self.board_size):
            seq_color = Color.EMPTY
            seq_len = 0
            for y in range(self.board_size):
                seq_color, seq_len = self._check_win_strike(self.board[y][x], seq_color, seq_len)

    def check_win_diagonals_1(self):
        for init_v in range(4, self.board_size):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(0, init_v + 1), range(init_v, -1, -1)):
                seq_color, seq_len = self._check_win_strike(self.board[y][x], seq_color, seq_len)

        for init_h in range(1, self.board_size - 4):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(init_h, self.board_size), range(self.board_size - 1, init_h - 1, -1)):
                seq_color, seq_len = self._check_win_strike(self.board[y][x], seq_color, seq_len)

    def check_win_diagonals_2(self):
        for init_h in range(self.board_size - 5, 0, -1):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(init_h, self.board_size), range(0, self.board_size - init_h)):
                seq_color, seq_len = self._check_win_strike(self.board[y][x], seq_color, seq_len)
        for init_v in range(0, self.board_size - 4):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(0, self.board_size - init_v), range(init_v, self.board_size)):
                seq_color, seq_len = self._check_win_strike(self.board[y][x], seq_color, seq_len)

    def check_forbidden_turn(self, x: int, y: int):
        pass
        raise ForbiddenTurn(self.coordinates_to_position(x, y))

    @staticmethod
    def _check_win_strike(current_color, seq_color, seq_len):
        if current_color == seq_color and current_color != Color.EMPTY:
            seq_len += 1
        else:
            seq_len = 1
            seq_color = current_color
        if seq_len == 5 and current_color != Color.EMPTY:
            exception = BlackPlayerWinException if current_color == Color.BLACK else WhitePlayerWinException
            raise exception()
        return seq_color, seq_len

    def __str__(self):
        res = ""
        for line in self.board:
            for pos in line:
                if pos == Color.EMPTY:
                    res += "- "
                elif pos == Color.WHITE:
                    res += "W "
                else:
                    res += "B "
            res += "\n"
        return res
