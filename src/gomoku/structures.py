from enum import Enum
from dataclasses import dataclass


class Color(Enum):
    WHITE = 1
    BLACK = 2
    EMPTY = 0


class SequencesInfo:
    def __init__(self, *, color_buffer: Color = Color.EMPTY, last_seen_white: int = -1,
                 last_seen_black: int = -1, buffer: int = 0, seq: int = 0):
        self.color_buffer = color_buffer
        self.last_seen_white = last_seen_white
        self.last_seen_black = last_seen_black
        self.seq = seq
        self.buffer = buffer
        self.combination_score = {0: 0,
                                  1: 1,
                                  2: 10,
                                  3: 100,
                                  4: 1000,
                                  5: float('inf')}
        self.score_coef = {
            Color.WHITE: 1,
            Color.BLACK: -1,
            Color.EMPTY: 0,
        }

    def clear(self, pos_color: Color) -> None:
        self.color_buffer = pos_color
        self.last_seen_black = -1
        self.last_seen_white = -1
        self.buffer = 0
        self.seq = 0

    def refresh(self, pos_color: Color) -> None:
        self.color_buffer = pos_color
        self.buffer = 1
        self.seq = 1

    def inc_seq(self) -> None:
        self.seq += 1

    def update_last_seen(self, pos: int, pos_color: Color) -> None:
        if pos_color == Color.WHITE:
            self.last_seen_white = pos
        else:
            self.last_seen_black = pos

    def count_score(self, pos: int, pos_color: Color):
        if pos_color == self.color_buffer:
            self.inc_seq()
            if self.color_buffer != Color.EMPTY and self.seq == 5:
                return self.combination_score[5] * self.score_coef[self.color_buffer]
        elif pos_color == Color.EMPTY:
            self.buffer += self.combination_score[self.seq] * self.score_coef[self.color_buffer]
            self.seq = 0
        else:
            if pos_color == self.color_buffer:
                self.inc_seq()
                self.update_last_seen(pos, pos_color)
            else:
                boarder = self.last_seen_white if pos_color == Color.WHITE else self.last_seen_black
                if pos - boarder > 5:
                    buffer = self.buffer
                    self.refresh(pos_color)
                    self.update_last_seen(pos, pos_color)
                    return buffer
        return 0

    def complete_line(self, board_size):
        boarder = self.last_seen_black if self.color_buffer == Color.WHITE else self.last_seen_white
        if board_size - boarder > 5:
            return self.buffer
        return 0