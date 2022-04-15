import tkinter as ttk
from constants import BOARD_COLOR, PAD_FROM_WIN


class InfoPanel:

    def __init__(self, win, config):
        self._win = win
        self._config = config

        self._turn = ttk.StringVar()
        self._moves = ttk.IntVar()

        self._info_frame = None
        self._p1 = None
        self._p2 = None
        self._cur_player = None

        self._moves.set(0)

    def print_info(self):
        self._info_frame = ttk.Frame(self._win,
                                     width=self._win.winfo_width() - self._win.winfo_height() - PAD_FROM_WIN / 2,
                                     height=(self._win.winfo_height() / 3) * 2 - PAD_FROM_WIN,
                                     bg=BOARD_COLOR)
        self._info_frame.update()

        win_width = self._win.winfo_width()
        f_width = self._win.winfo_width() - self._win.winfo_height() - PAD_FROM_WIN / 2
        f_height = (self._win.winfo_height() / 3) * 2 - PAD_FROM_WIN

        rel_x = (win_width - (f_width + PAD_FROM_WIN) / 2) / win_width
        self._info_frame.place(relx=rel_x, y=f_height / 2 + (PAD_FROM_WIN / 2), anchor="center")

        info_l = ttk.Label(self._info_frame,
                           text='INFO',
                           font=('Arial', 20, "bold"),
                           bg=BOARD_COLOR)
        info_l.place(relx=.5, rely=.05, anchor="center")

        font = ('Arial', 20)
        font_u = ('Arial', 20, "underline")

        mode_l = ttk.Label(self._info_frame, text='Mode:', font=font_u, bg=BOARD_COLOR)
        mode_l.place(relx=.1, rely=.2, anchor="w")

        mode = ttk.Label(self._info_frame, text=self._config.get_mode(), font=font, bg=BOARD_COLOR)
        mode.place(relx=.7, rely=.2, anchor="center")

        turn_l = ttk.Label(self._info_frame, text='Turn:', font=font_u, bg=BOARD_COLOR)
        turn_l.place(relx=.1, rely=.35, anchor="w")

        turn = ttk.Label(self._info_frame, textvariable=self._turn, font=font, bg=BOARD_COLOR)
        turn.place(relx=.7, rely=.35, anchor="center")

        moves_l = ttk.Label(self._info_frame, text='Moves:', font=font_u, bg=BOARD_COLOR)
        moves_l.place(relx=.1, rely=.5, anchor="w")

        moves = ttk.Label(self._info_frame, textvariable=self._moves, font=font, bg=BOARD_COLOR)
        moves.place(relx=.7, rely=.5, anchor="center")

        catches_l = ttk.Label(self._info_frame, text='Catches:', font=font_u, bg=BOARD_COLOR)
        catches_l.place(relx=.1, rely=.65, anchor="w")

        if self._config.get_mode() == "PvE":
            if self._config.get_first_move() == "BLACK":
                self._p1 = Player(self._info_frame, "Player")
                self._p2 = Player(self._info_frame, f"AI {self._config.get_difficult().lower()}")
            else:
                self._p1 = Player(self._info_frame, f"AI {self._config.get_difficult().lower()}")
                self._p2 = Player(self._info_frame, "Player")
        else:
            self._p1 = Player(self._info_frame, "Player #1")
            self._p2 = Player(self._info_frame, "Player #2")
        self._cur_player = self._p1
        self._turn.set(self._cur_player.get_name())

        self._p1.place(rel_y=.78)
        self._p2.place(rel_y=.88)

    def _inc_moves(self):
        self._moves.set(self._moves.get() + 1)

    def _dec_moves(self):
        cur = self._moves.get()
        if cur != 0:
            self._moves.set(self._moves.get() - 1)

    def switch_turn(self):
        if self._cur_player == self._p1:
            self._cur_player = self._p2
        else:
            self._cur_player = self._p1
        self._turn.set(self._cur_player.get_name())

    def back(self, catch=False):
        if catch:
            self._cur_player.undo_catch()
        self.switch_turn()
        self._dec_moves()

    def next(self, catch=False):
        if catch:
            self._cur_player.catch()
        self.switch_turn()
        self._inc_moves()


class Player:

    def __init__(self, win, name):
        self._win = win
        self._name = ttk.Label(self._win, text=name, font=("Arial", 20), bg=BOARD_COLOR)
        self._count = ttk.IntVar()
        self._catches = ttk.Label(self._win, textvariable=self._count, font=("Arial", 20), bg=BOARD_COLOR)

        self._count.set(0)

    def place(self, rel_y):
        self._name.place(relx=.16, rely=rel_y, anchor="w")
        self._catches.place(relx=.7, rely=rel_y, anchor="center")

    def catch(self):
        self._count.set(self._count.get() + 1)

    def undo_catch(self):
        cur = self._count.get()
        if cur != 0:
            self._count.set(self._count.get() - 1)

    def get_name(self):
        return self._name.cget("text")

    def __eq__(self, other):
        if self.get_name() == other.get_name():
            return True
        else:
            return False
