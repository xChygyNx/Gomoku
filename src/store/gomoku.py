import typing as t

from src.store.color import Color
from src.exceptions import (
    BusyCell,
)
from src.const import (
    CAPATURE_DISTANCE,
    INITIAL_STATE_SCORE,
    BOARD_SIZE,
)

class Gomoku:
    def __init__(self):
        self._board = None
        self.now_turn = Color.WHITE

    @property
    def board(self) -> t.List[t.List[Color]]:
        if self._board is not None:
            return self._board
        self._board = [[Color.EMPTY for _ in range(19)] for _ in range(19)]
        return self._board

    def make_turn(self, x: int, y: int, color: Color = None) -> None:
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
        self.board[x][y] = Color.EMPTY
        self.board[x+1][y] = Color.EMPTY

    def check_and_clear_vertical(self, x: int, y: int) -> None:
        versa_color = Color.WHITE if self.now_turn == Color.BLACK else Color.BLACK
        if self.board[x][y] != versa_color or self.board[x][y+1] != versa_color:
            return
        self.board[x][y] = Color.EMPTY
        self.board[x][y+1] = Color.EMPTY

    def check_and_clear_diagonal_1(self, x: int, y: int) -> None:
        versa_color = Color.WHITE if self.now_turn == Color.BLACK else Color.BLACK
        if self.board[x][y] != versa_color or self.board[x+1][y+1] != versa_color:
            return
        self.board[x][y] = Color.EMPTY
        self.board[x+1][y+1] = Color.EMPTY

    def check_and_clear_diagonal_2(self, x: int, y: int) -> None:
        versa_color = Color.WHITE if self.now_turn == Color.BLACK else Color.BLACK
        if self.board[x][y] != versa_color or self.board[x+1][y-1] != versa_color:
            return
        self.board[x][y] = Color.EMPTY
        self.board[x+1][y-1] = Color.EMPTY

    def make_capture(self, x: int, y: int) -> None:
        if x - CAPATURE_DISTANCE >= 0 and self.board[x - CAPATURE_DISTANCE][y] == self.now_turn:
            self.check_and_clear_horizontal(x - CAPATURE_DISTANCE + 1, y)
        if x + CAPATURE_DISTANCE <= BOARD_SIZE and self.board[x + CAPATURE_DISTANCE][y] == self.now_turn:
            self.check_and_clear_horizontal(x + 1, y)
        if y - CAPATURE_DISTANCE >= 0 and self.board[x][y - CAPATURE_DISTANCE] == self.now_turn:
            self.check_and_clear_vertical(x, y - CAPATURE_DISTANCE + 1)
        if y + CAPATURE_DISTANCE <= BOARD_SIZE and self.board[x][y + CAPATURE_DISTANCE] == self.now_turn:
            self.check_and_clear_vertical(x, y + 1)
        if (x - CAPATURE_DISTANCE >= 0 and y - CAPATURE_DISTANCE >= 0) and \
            self.board[x-CAPATURE_DISTANCE][y-CAPATURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_1(x - CAPATURE_DISTANCE + 1, y - CAPATURE_DISTANCE + 1)
        if (x + CAPATURE_DISTANCE <= BOARD_SIZE and y + CAPATURE_DISTANCE <= 18) and \
            self.board[x+CAPATURE_DISTANCE][y+CAPATURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_1(x + 1, y + 1)
        if (x - CAPATURE_DISTANCE >= 0 and y + CAPATURE_DISTANCE <= 18) and \
            self.board[x-CAPATURE_DISTANCE][y+CAPATURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_2(x - CAPATURE_DISTANCE + 1, y + CAPATURE_DISTANCE - 1)
        if (x + CAPATURE_DISTANCE <= BOARD_SIZE and y - CAPATURE_DISTANCE >= 0) and \
            self.board[x+CAPATURE_DISTANCE][y-CAPATURE_DISTANCE] == self.now_turn:
            self.check_and_clear_diagonal_2(x + 1, y - 1)

    def check_state(self):
        acc_score = 0
        acc_score += self.check_horizontal()
        acc_score += self.check_vertical()
        acc_score += self.check_diagonal_1()
        acc_score += self.check_diagonal_2()
        state_score = INITIAL_STATE_SCORE + acc_score

    def check_horizontal(self) -> int:
        pass

    def check_vertical(self) -> int:
        pass

    def check_diagonal_1(self) -> int:
        pass

    def check_diagonal_2(self) -> int:
        pass

    def reset_board(self) -> None:
        for line in self.board:
            for pos in line:
                pos = Color.EMPTY
