import typing as t

from src.gomoku.structures import Color, SequencesInfo
from src.exceptions import *
from src.const import (
    CAPTURE_DISTANCE,
    INITIAL_STATE_SCORE,
    BOARD_SIZE,
)

class Gomoku:
    def __init__(self, **kwargs):
        self.board_size = kwargs.get('board_size')
        self.mode = kwargs.get('mode')
        self.player_color = kwargs.get('player_color')
        self.difficult = kwargs.get('difficult')
        self._board = None
        self.now_turn = Color.WHITE
        self.white_capture = 0
        self.black_capture = 0
        self.check_init()

    def check_init(self):
        if self.mode not in ['PvE', 'PvP']:
            raise ConfigGomokuError('Game mode not correct')
        if self.mode == 'PvE' and self.player_color.lower() not in ['black', 'white']:
            raise ConfigGomokuError('Color of player for PvE mode is not correct')
        if self.mode == 'PvE' and self.difficult.lower() not in ['easy', 'medium', 'hard']:
            raise ConfigGomokuError('Difficult of AI player for PvE mode is not correct')

    @property
    def board(self) -> t.List[t.List[Color]]:
        if self._board is not None:
            return self._board
        self._board = [[Color.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]
        return self._board

    def win_by_capture(self) -> None:
        if self.white_capture >= 10:
            raise WhitePlayerWinException
        elif self.black_capture >= 10:
            raise BlackPlayerWinException

    def make_turn(self, position: str, color: str=None, **kwargs) -> None:
        x, y = position[:1], int(position[1:]) - 1
        x = ord(x) - ord('a')
        if color is not None:
            color = Color.__getattr__(color.upper())
        self._make_turn(x, y, color)

    def _make_turn(self, x: int, y: int, color: Color = None) -> None:
        if self.board[x][y] != Color.EMPTY:
            raise BusyCell(x, y)
        color = self.now_turn if color is None else color
        self.board[x][y] = color
        self.make_capture(x, y)
        if self.now_turn == Color.WHITE:
            self.now_turn = Color.BLACK
        else:
            self.now_turn = Color.WHITE

    def check_and_clear_horizontal(self, x: int, y: int) -> None:
        versa_color = Color.WHITE if self.now_turn == Color.BLACK else Color.BLACK
        if self.board[x][y] != versa_color or self.board[x+1][y] != versa_color:
            return
        if self.now_turn == Color.BLACK:
            self.black_capture += 2
        else:
            self.white_capture += 2
        self.board[x][y] = Color.EMPTY
        self.board[x+1][y] = Color.EMPTY

    def check_and_clear_vertical(self, x: int, y: int) -> None:
        versa_color = Color.WHITE if self.now_turn == Color.BLACK else Color.BLACK
        if self.board[x][y] != versa_color or self.board[x][y+1] != versa_color:
            return
        if self.now_turn == Color.BLACK:
            self.black_capture += 2
        else:
            self.white_capture += 2
        self.board[x][y] = Color.EMPTY
        self.board[x][y+1] = Color.EMPTY

    def check_and_clear_diagonal_1(self, x: int, y: int) -> None:
        versa_color = Color.WHITE if self.now_turn == Color.BLACK else Color.BLACK
        if self.board[x][y] != versa_color or self.board[x+1][y+1] != versa_color:
            return
        if self.now_turn == Color.BLACK:
            self.black_capture += 2
        else:
            self.white_capture += 2
        self.board[x][y] = Color.EMPTY
        self.board[x+1][y+1] = Color.EMPTY

    def check_and_clear_diagonal_2(self, x: int, y: int) -> None:
        versa_color = Color.WHITE if self.now_turn == Color.BLACK else Color.BLACK
        if self.board[x][y] != versa_color or self.board[x+1][y-1] != versa_color:
            return
        if self.now_turn == Color.BLACK:
            self.black_capture += 2
        else:
            self.white_capture += 2
        self.board[x][y] = Color.EMPTY
        self.board[x+1][y-1] = Color.EMPTY

    def make_capture(self, x: int, y: int) -> None:
        if x - CAPTURE_DISTANCE >= 0 and self.board[x - CAPTURE_DISTANCE][y] == self.now_turn:
            self.check_and_clear_horizontal(x - CAPTURE_DISTANCE + 1, y)
        if x + CAPTURE_DISTANCE <= (self.board_size - 1) and self.board[x + CAPTURE_DISTANCE][y] == self.now_turn:
            self.check_and_clear_horizontal(x + 1, y)
        if y - CAPTURE_DISTANCE >= 0 and self.board[x][y - CAPTURE_DISTANCE] == self.now_turn:
            self.check_and_clear_vertical(x, y - CAPTURE_DISTANCE + 1)
        if y + CAPTURE_DISTANCE <= (self.board_size - 1) and self.board[x][y + CAPTURE_DISTANCE] == self.now_turn:
            self.check_and_clear_vertical(x, y + 1)
        if (x - CAPTURE_DISTANCE >= 0 and y - CAPTURE_DISTANCE >= 0) and \
                self.board[x - CAPTURE_DISTANCE][y - CAPTURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_1(x - CAPTURE_DISTANCE + 1, y - CAPTURE_DISTANCE + 1)
        if (x + CAPTURE_DISTANCE <= (self.board_size - 1) and y + CAPTURE_DISTANCE <= (self.board_size - 1)) and \
                self.board[x + CAPTURE_DISTANCE][y + CAPTURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_1(x + 1, y + 1)
        if (x - CAPTURE_DISTANCE >= 0 and y + CAPTURE_DISTANCE <= (self.board_size - 1)) and \
                self.board[x - CAPTURE_DISTANCE][y + CAPTURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_2(x - CAPTURE_DISTANCE + 1, y + CAPTURE_DISTANCE - 1)
        if (x + CAPTURE_DISTANCE <= (self.board_size - 1) and y - CAPTURE_DISTANCE >= 0) and \
                self.board[x + CAPTURE_DISTANCE][y - CAPTURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_2(x + 1, y - 1)
        self.win_by_capture()

    def check_state(self):
        acc_score = INITIAL_STATE_SCORE
        acc_score += self.check_horizontals()
        if -1 * float('inf') < acc_score < float('inf'):
            acc_score += self.check_verticals()
        if -1 * float('inf') < acc_score < float('inf'):
            acc_score += self.check_diagonals_1()
        if -1 * float('inf') < acc_score < float('inf'):
            acc_score += self.check_diagonals_2()
        return acc_score

    def check_horizontals(self) -> int:
        acc = 0
        seq_info = SequencesInfo()
        for line in self.board:
            seq_info.clear(pos_color=line[0])
            for pos in range(len(line)):
                acc += seq_info.count_score(pos, line[pos])
            acc += seq_info.complete_line(self.board_size)
        return acc

    def check_verticals(self) -> int:
        acc = 0
        seq_info = SequencesInfo()
        for pos in range(self.board_size):
            seq_info.clear(pos_color=self.board[0][pos])
            for line in range(self.board_size):
                acc += seq_info.count_score(line, self.board[line][pos])
            acc += seq_info.complete_line(self.board_size)
        return acc

    def check_diagonals_1(self) -> int:
        acc = 0
        seq_info = SequencesInfo()
        for init_v in range(4, self.board_size):
            seq_info.clear(pos_color=self.board[0][init_v])
            for h, v in zip(range(0, init_v + 1), range(init_v, -1, -1)):
                acc += seq_info.count_score(v, self.board[h][v])
            acc += seq_info.complete_line(self.board_size)
        for init_h in range(1, self.board_size - 4):
            seq_info.clear(pos_color=self.board[init_h][self.board_size - 1])
            for h, v in zip(range(init_h, self.board_size), range(self.board_size - 1, init_h - 1, -1)):
                acc += seq_info.count_score(v, self.board[h][v])
            acc += seq_info.complete_line(self.board_size)
        return acc

    def check_diagonals_2(self) -> int:
        acc = 0
        seq_info = SequencesInfo()
        for init_h in range(self.board_size - 5, 0, -1):
            seq_info.clear(pos_color=self.board[init_h][0])
            for h, v in zip(range(init_h, self.board_size), range(0, self.board_size - init_h)):
                acc += seq_info.count_score(v, self.board[h][v])
            acc += seq_info.complete_line(self.board_size)
        for init_v in range(0, self.board_size - 4):
            seq_info.clear(pos_color=self.board[0][init_v])
            for h, v in zip(range(0, self.board_size - init_v), range(init_v, self.board_size)):
                acc += seq_info.count_score(v, self.board[h][v])
            acc += seq_info.complete_line(self.board_size)
        return acc

    def reset_board(self) -> None:
        for line in self.board:
            for pos, _ in enumerate(line):
                line[pos] = Color.EMPTY
