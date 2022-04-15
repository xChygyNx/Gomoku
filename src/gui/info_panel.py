
import tkinter as ttk
from constants import BOARD_COLOR, PAD_FROM_WIN


class InfoPanel:

    def __init__(self, win, config):
        self._win = win
        self._config = config
        self._frame = None
        self._turn = None

    def print_info(self):
        self._frame = ttk.Frame(self._win,
                                width=self._win.winfo_width() - self._win.winfo_height() - PAD_FROM_WIN / 2,
                                height=self._win.winfo_height() - PAD_FROM_WIN,
                                bg=BOARD_COLOR)
        self._frame.update()

        win_width = self._win.winfo_width()
        f_width = self._win.winfo_width() - self._win.winfo_height() - PAD_FROM_WIN / 2

        rel_x = (win_width - (f_width + PAD_FROM_WIN) / 2) / win_width
        self._frame.place(relx=rel_x, rely=.5, anchor="center")

        info_l = ttk.Label(self._frame,
                           text='INFO',
                           font=('Arial', 20),
                           bg=BOARD_COLOR)
        info_l.place(relx=.5, rely=.05, anchor="center")
