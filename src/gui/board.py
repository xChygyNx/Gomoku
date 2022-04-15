import tkinter as ttk
from constants import BACKGROUND_COLOR, BOARD_COLOR, PAD_FROM_WIN


class Board:

    def __init__(self, win, cells):
        self._win = win
        self._cells = cells
        self._b_width = win.winfo_height() - PAD_FROM_WIN
        self._padding = 50
        self._cell_width = (self._b_width - 2 * self._padding) / self._cells
        self._frame = None
        self._canvas = None

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
