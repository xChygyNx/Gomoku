import typing as t
from typing import List

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

    def set_piece(self, x: int, y: int, color: Color):
        self.board[y][x] = color

    def set_piece_by_pos(self, position: str, color: str):
        x, y = self.position_to_coordinates(position)
        c = Color.WHITE if color.upper() == Color.WHITE.name else Color.BLACK
        self.set_piece(x, y, c)

    def delete_piece(self, x: int, y: int):
        self.board[y][x] = Color.EMPTY

    def delete_piece_by_pos(self, position: str):
        x, y = self.position_to_coordinates(position)
        self.delete_piece(x, y)

    def coordinates_to_position(self, x: int, y: int) -> str:
        if x > self.board_size or y > self.board_size:
            raise ValueError(f'Coordinate ({x}, {y}) absence on board')
        return LETTERS[x] + str(self.board_size - y)

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
        for y in range(len(self.board)):
            seq_color = Color.EMPTY
            seq_len = 0
            for x in range(len(self.board)):
                seq_color, seq_len = self._check_win_strike(x, y, seq_color, seq_len)

    def check_win_verticals(self):
        for x in range(self.board_size):
            seq_color = Color.EMPTY
            seq_len = 0
            for y in range(self.board_size):
                seq_color, seq_len = self._check_win_strike(x, y, seq_color, seq_len)

    def check_win_diagonals_1(self):
        for init_v in range(4, self.board_size):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(0, init_v + 1), range(init_v, -1, -1)):
                seq_color, seq_len = self._check_win_strike(x, y, seq_color, seq_len)

        for init_h in range(1, self.board_size - 4):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(init_h, self.board_size), range(self.board_size - 1, init_h - 1, -1)):
                seq_color, seq_len = self._check_win_strike(x, y, seq_color, seq_len)

    def check_win_diagonals_2(self):
        for init_h in range(self.board_size - 5, 0, -1):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(init_h, self.board_size), range(0, self.board_size - init_h)):
                seq_color, seq_len = self._check_win_strike(x, y, seq_color, seq_len)
        for init_v in range(0, self.board_size - 4):
            seq_color = Color.EMPTY
            seq_len = 0
            for x, y in zip(range(0, self.board_size - init_v), range(init_v, self.board_size)):
                seq_color, seq_len = self._check_win_strike(x, y, seq_color, seq_len)

    def get_coordinates_of_captures(self, position: str, color: str):
        x, y = self.position_to_coordinates(position)
        c = Color.WHITE if color.upper() == Color.WHITE.name else Color.BLACK
        return self.get_captures(x, y, c)

    def get_positions_of_captures(self, position: str, color: str) -> List[str]:
        coordinates = self.get_coordinates_of_captures(position, color)
        return [self.coordinates_to_position(x, y) for x, y in coordinates]

    def get_captures(self, x: int, y: int, color: Color) -> List[str]:
        """Returns list of captures pieces. [a1, a2]"""
        catches = []
        versa_color = Color.WHITE if color == Color.BLACK else Color.BLACK

        # horizontal left
        if x > 2:
            if self.board[y][x - 3] == color and \
                    self.board[y][x - 1] == versa_color and self.board[y][x - 2] == versa_color:
                self.board[y][x - 1] = Color.EMPTY
                self.board[y][x - 2] = Color.EMPTY
                catches += [(x - 1, y), (x - 2, y)]
        # horizontal right
        if x < self.board_size - 3:
            if self.board[y][x + 3] == color and \
                    self.board[y][x + 1] == versa_color and self.board[y][x + 2] == versa_color:
                self.board[y][x + 1] = Color.EMPTY
                self.board[y][x + 2] = Color.EMPTY
                catches += [(x + 1, y), (x + 2, y)]

        # vertical top
        if y > 2:
            if self.board[y - 3][x] == color and \
                    self.board[y - 1][x] == versa_color and self.board[y - 2][x] == versa_color:
                self.board[y - 1][x] = Color.EMPTY
                self.board[y - 2][x] = Color.EMPTY
                catches += [(x, y - 1), (x, y - 2)]
        # vertical bottom
        if y < self.board_size - 3:
            if self.board[y + 3][x] == color and \
                    self.board[y + 1][x] == versa_color and self.board[y + 2][x] == versa_color:
                self.board[y + 1][x] = Color.EMPTY
                self.board[y + 2][x] = Color.EMPTY
                catches += [(x, y + 1), (x, y + 2)]

        # diagonal top-left <-> bottom-right
        if x > 2 and y > 2:
            if self.board[y - 3][x - 3] == color and \
                    self.board[y - 1][x - 1] == versa_color and self.board[y - 2][x - 2] == versa_color:
                self.board[y - 1][x - 1] = Color.EMPTY
                self.board[y - 2][x - 2] = Color.EMPTY
                catches += [(x - 1, y - 1), (x - 2, y - 2)]

        if x < self.board_size - 3 and y < self.board_size - 3:
            if self.board[y + 3][x + 3] == color and \
                    self.board[y + 1][x + 1] == versa_color and self.board[y + 2][x + 2] == versa_color:
                self.board[y + 1][x + 1] = Color.EMPTY
                self.board[y + 2][x + 2] = Color.EMPTY
                catches += [(x + 1, y + 1), (x + 2, y + 2)]

        # diagonal top-right <-> bottom-left
        if x < self.board_size - 3 and y > 2:
            if self.board[y - 3][x + 3] == color and \
                    self.board[y - 1][x + 1] == versa_color and self.board[y - 2][x + 2] == versa_color:
                self.board[y - 1][x + 1] = Color.EMPTY
                self.board[y - 2][x + 2] = Color.EMPTY
                catches += [(x + 1, y - 1), (x + 2, y - 2)]

        if x > 2 and y < self.board_size - 3:
            if self.board[y + 3][x - 3] == color and \
                    self.board[y + 1][x - 1] == versa_color and self.board[y + 2][x - 2] == versa_color:
                self.board[y + 1][x - 1] = Color.EMPTY
                self.board[y + 2][x - 2] = Color.EMPTY
                catches += [(x - 1, y + 1), (x - 2, y + 2)]
        return catches

    def _check_win_strike(self, x: int, y: int, seq_color: Color, seq_len: int):
        current_color = self.board[y][x]
        if current_color == seq_color and current_color != Color.EMPTY:
            seq_len += 1
        else:
            seq_len = 1
            seq_color = current_color
        if seq_len == 5:
            exception = BlackPlayerWinException if current_color == Color.BLACK else WhitePlayerWinException
            raise exception()
        return seq_color, seq_len

    def get_win_coordinates(self):
        strike = []
        # horizontal
        for y in range(len(self.board)):
            seq_color = Color.EMPTY
            for x in range(len(self.board)):
                seq_color, strike = self._check_next_in_strike(x, y, seq_color, strike)
                if len(strike) == 5:
                    return strike
        # vertical
        for x in range(len(self.board)):
            seq_color = Color.EMPTY
            for y in range(len(self.board)):
                seq_color, strike = self._check_next_in_strike(x, y, seq_color, strike)
                if len(strike) == 5:
                    return strike
        # diagonal 1
        for init_v in range(4, self.board_size):
            seq_color = Color.EMPTY
            for x, y in zip(range(0, init_v + 1), range(init_v, -1, -1)):
                seq_color, strike = self._check_next_in_strike(x, y, seq_color, strike)
                if len(strike) == 5:
                    return strike
        for init_h in range(1, self.board_size - 4):
            seq_color = Color.EMPTY
            for x, y in zip(range(init_h, self.board_size), range(self.board_size - 1, init_h - 1, -1)):
                seq_color, strike = self._check_next_in_strike(x, y, seq_color, strike)
                if len(strike) == 5:
                    return strike

        # diagonal 2
        for init_h in range(self.board_size - 5, 0, -1):
            seq_color = Color.EMPTY
            for x, y in zip(range(init_h, self.board_size), range(0, self.board_size - init_h)):
                seq_color, strike = self._check_next_in_strike(x, y, seq_color, strike)
                if len(strike) == 5:
                    return strike
        for init_v in range(0, self.board_size - 4):
            seq_color = Color.EMPTY
            for x, y in zip(range(0, self.board_size - init_v), range(init_v, self.board_size)):
                seq_color, strike = self._check_next_in_strike(x, y, seq_color, strike)
                if len(strike) == 5:
                    return strike
        return []

    def get_win_positions(self):
        coordinates = self.get_win_coordinates()
        return [self.coordinates_to_position(x, y) for x, y in coordinates]

    def _check_next_in_strike(self, x: int, y: int, seq_color: Color, strike: List[tuple]):
        current_color = self.board[y][x]
        if current_color == seq_color and current_color != Color.EMPTY:
            strike.append((x, y))
        else:
            strike = [(x, y)]
            seq_color = current_color
        return seq_color, strike

    def check_forbidden_turn(self, x: int, y: int):
        pass
        raise ForbiddenTurn(self.coordinates_to_position(x, y))

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
