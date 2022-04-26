import typing as t
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

    def checks(self):
        self.check_win()

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
                    raise exception

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
                    raise exception

    def check_win_diagonals1(self):
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
                    raise exception
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
                    raise exception

    def check_win_diagonals2(self):
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
                    raise exception
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
                    raise exception
