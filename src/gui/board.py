import tkinter as ttk
from constants import BACKGROUND_COLOR, BOARD_COLOR, PAD_FROM_WIN


class Board:

    def __init__(self, win, cells, first_move):
        self._win = win
        self._cells = cells
        self._b_width = win.winfo_height() - PAD_FROM_WIN
        self._padding = 50
        self._cell_width = (self._b_width - 2 * self._padding) / self._cells
        self._frame = None
        self._canvas = None
        self._pieces = []
        self._cur_color = first_move.lower()

    def print_board(self):
        self._frame = ttk.Frame(self._win,
                                width=self._win.winfo_height(),
                                height=self._win.winfo_height(),
                                bg=BACKGROUND_COLOR,
                                bd=10)

        rel_x = 1 - (self._win.winfo_width() - self._win.winfo_height() / 2) / self._win.winfo_width()
        self._frame.place(relx=rel_x, rely=.5, anchor="center")

        self._canvas = ttk.Canvas(self._frame,
                                  width=self._b_width,
                                  height=self._b_width,
                                  bg=BOARD_COLOR)
        self._canvas.place(relx=.5, rely=.5, anchor="center")

        padding = self._padding
        width = self._b_width
        cell_width = self._cell_width

        for n in range(0, self._cells + 1):
            # lines
            self._canvas.create_line(padding, padding + cell_width * n, width - padding, padding + cell_width * n)
            self._canvas.create_line(padding + cell_width * n, padding, padding + cell_width * n, width - padding)

            # numbers
            self._canvas.create_text(padding / 2, width - padding - cell_width * n, text=str(n + 1))
            self._canvas.create_text(width - padding / 2, width - padding - cell_width * n, text=str(n + 1))

            # letters
            self._canvas.create_text(padding + cell_width * n, padding / 2, text=chr(97 + n))
            self._canvas.create_text(padding + cell_width * n, width - padding / 2, text=chr(97 + n))

            c = Board.create_circle(self._canvas, padding, padding + cell_width * n, 12, fill="white")
            self._canvas.delete(c)

        self._canvas.bind('<Button-1>', self.set_piece)

    def set_piece(self, event):
        x = Board.round_cell(event.x - self._padding, self._cell_width) + self._padding
        y = Board.round_cell(event.y - self._padding, self._cell_width) + self._padding

        if self._padding / 2 < x < self._b_width - self._padding / 2 and \
                self._padding / 2 < y < self._b_width - self._padding / 2:

            position = chr(97 + int((x - self._padding) // self._cell_width)) + \
                       str(self._cells - int((y - self._padding) // self._cell_width) + 1)

            if position not in self._pieces:
                p = Board.create_circle(self._canvas, x, y, 12, fill=self._cur_color)
                self._pieces.append(Piece(p, position, self._cur_color))
                self.switch()

    def switch(self):
        sw = {"white": "black", "black": "white"}
        self._cur_color = sw[self._cur_color]

    def undo(self):
        p = self._pieces.pop()
        self._canvas.delete(p.get_piece())
        self.switch()

    @staticmethod
    def create_circle(canvas, x, y, r, **kwargs):
        return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    @staticmethod
    def round_cell(x, base):
        return base * round(x / base)


class Piece:

    def __init__(self, piece, pos, color):
        self._piece = piece
        self._pos = pos
        self._color = color

    def get_pos(self):
        return self._pos

    def get_color(self):
        return self._color

    def get_piece(self):
        return self._piece

    def __eq__(self, other):
        if isinstance(other, str):
            return self.get_pos() == other
        return self.get_pos() == other.get_pos()

    def __str__(self):
        return f"{self._pos}: {self._color}"
