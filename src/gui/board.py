import tkinter as ttk
from constants import BACKGROUND_COLOR, BOARD_COLOR, PAD_FROM_WIN
from player import Player
from piece import Piece


class Board:

    def __init__(self, win, config):
        self._win = win
        self._config = config

        # board props
        self._board_width = win.winfo_height() - PAD_FROM_WIN
        self._padding = 50
        self._cell_width = (self._board_width - 2 * self._padding) / self._config.get_board_size()
        self._board_frame = None
        self._board_canvas = None

        # info frame props
        self._info_frame = None
        self._turn = ttk.StringVar()
        self._moves = ttk.IntVar()
        self._moves.set(0)

        # player properties
        self._p1 = None
        self._p2 = None
        self._cur_player = None
        self._pieces = []

    def print_board(self):
        """Initialize game board"""
        self._board_frame = ttk.Frame(self._win,
                                      width=self._win.winfo_height(),
                                      height=self._win.winfo_height(),
                                      bg=BACKGROUND_COLOR,
                                      bd=10)

        rel_x = 1 - (self._win.winfo_width() - self._win.winfo_height() / 2) / self._win.winfo_width()
        self._board_frame.place(relx=rel_x, rely=.5, anchor="center")

        self._board_canvas = ttk.Canvas(self._board_frame,
                                        width=self._board_width,
                                        height=self._board_width,
                                        bg=BOARD_COLOR)
        self._board_canvas.place(relx=.5, rely=.5, anchor="center")

        padding = self._padding
        width = self._board_width
        cell_width = self._cell_width

        for n in range(0, self._config.get_board_size() + 1):
            # print lines
            self._board_canvas.create_line(padding, padding + cell_width * n, width - padding, padding + cell_width * n)
            self._board_canvas.create_line(padding + cell_width * n, padding, padding + cell_width * n, width - padding)

            # print lines
            self._board_canvas.create_text(padding / 2, width - padding - cell_width * n, text=str(n + 1))
            self._board_canvas.create_text(width - padding / 2, width - padding - cell_width * n, text=str(n + 1))

            # print lines
            self._board_canvas.create_text(padding + cell_width * n, padding / 2, text=chr(97 + n))
            self._board_canvas.create_text(padding + cell_width * n, width - padding / 2, text=chr(97 + n))

        self._board_canvas.bind('<Button-1>', self.set_piece)

    def print_info(self):
        """Initialize info panel"""
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
                self._p1 = Player(self._info_frame, "Player", "black")
                self._p2 = Player(self._info_frame, f"AI {self._config.get_difficult().lower()}", "white")
            else:
                self._p1 = Player(self._info_frame, f"AI {self._config.get_difficult().lower()}", "black")
                self._p2 = Player(self._info_frame, "Player", "white")
        else:
            self._p1 = Player(self._info_frame, "Player #1", "black")
            self._p2 = Player(self._info_frame, "Player #2", "white")
        self._cur_player = self._p1
        self._turn.set(self._cur_player.get_name())

        self._p1.place(rel_y=.78)
        self._p2.place(rel_y=.88)

    def set_piece(self, event):
        """Event on-click on board to set Piece"""
        x = Board.round_cell(event.x - self._padding, self._cell_width) + self._padding
        y = Board.round_cell(event.y - self._padding, self._cell_width) + self._padding

        if self._padding / 2 < x < self._board_width - self._padding / 2 and \
                self._padding / 2 < y < self._board_width - self._padding / 2:

            position = chr(97 + round((x - self._padding) / self._cell_width)) + \
                       str(self._config.get_board_size() - round((y - self._padding) / self._cell_width) + 1)

            if position not in self._pieces:
                p = Board.create_circle(self._board_canvas, x, y, 12, fill=self._cur_player.get_color())
                self._pieces.append(Piece(p, position, self._cur_player.get_color()))
                self.next()
                print(f"{self._cur_player.get_color()} piece set on {position}")

    def switch_player(self):
        if self._cur_player == self._p1:
            self._cur_player = self._p2
        else:
            self._cur_player = self._p1
        self._turn.set(self._cur_player.get_name())

    def back(self, catch=False):
        cur = self._moves.get()
        if cur != 0:
            if catch:
                self._cur_player.undo_catch()
            p = self._pieces.pop()
            self._board_canvas.delete(p.get_piece())
            self.switch_player()
            self._moves.set(self._moves.get() - 1)

    def next(self, catch=False):
        if catch:
            self._cur_player.catch()
        self._moves.set(self._moves.get() + 1)
        self.switch_player()

    @staticmethod
    def create_circle(canvas, x, y, r, **kwargs):
        return canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    @staticmethod
    def round_cell(x, base):
        return base * round(x / base)
