import tkinter as ttk
import json
from constants import *
from player import Player
from piece import Piece


class BoardGui:

    def __init__(self, win, config, send_func, receive_func):
        self._win = win
        self._config = config

        # board props
        self._board_width = win.winfo_height() - PAD_FROM_WIN
        self._padding = 50
        self._cell_width = (self._board_width - 2 * self._padding) / self._config.get_board_size()
        self._piece_radius = round(self._cell_width / 3)
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

        self._send_func = send_func
        self._receive_func = receive_func

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

        self._board_canvas.bind('<Button-1>', self.make_turn_on_event)
        self._print_info()

    def _print_info(self):
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
                           font=(FONT, LABEL_FONT_SIZE, "bold"),
                           bg=BOARD_COLOR)
        info_l.place(relx=.5, rely=.05, anchor="center")

        font_u = [FONT, LABEL_FONT_SIZE, "underline"]

        mode_l = ttk.Label(self._info_frame, text='Mode:', font=font_u, bg=BOARD_COLOR)
        mode_l.place(relx=.1, rely=.2, anchor="w")

        mode = ttk.Label(self._info_frame, text=self._config.get_mode(), font=LABEL_FONT, bg=BOARD_COLOR)
        mode.place(relx=.7, rely=.2, anchor="center")

        turn_l = ttk.Label(self._info_frame, text='Turn:', font=font_u, bg=BOARD_COLOR)
        turn_l.place(relx=.1, rely=.35, anchor="w")

        turn = ttk.Label(self._info_frame, textvariable=self._turn, font=LABEL_FONT, bg=BOARD_COLOR)
        turn.place(relx=.7, rely=.35, anchor="center")

        moves_l = ttk.Label(self._info_frame, text='Moves:', font=font_u, bg=BOARD_COLOR)
        moves_l.place(relx=.1, rely=.5, anchor="w")

        moves = ttk.Label(self._info_frame, textvariable=self._moves, font=LABEL_FONT, bg=BOARD_COLOR)
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

    def print_winner(self, width=350, height=150, **kwargs):
        window = ttk.Toplevel(background=BACKGROUND_COLOR,
                              width=width, height=height)
        window.title("WINNER")

        x = self._win.winfo_x() + self._win.winfo_width() // 2 - width // 2
        y = self._win.winfo_y() + self._win.winfo_height() // 2 - height // 2 - 50
        window.geometry("+{}+{}".format(x, y))

        label = ttk.Label(window,
                          text=f"{self._cur_player.get_name()} WINS",
                          font=(FONT, LABEL_FONT_SIZE, "bold"),
                          bg=BACKGROUND_COLOR)
        label.place(relx=.5, rely=.3, anchor="center")

        button = ttk.Button(window, text="Restart",
                            font=BUTTON_FONT,
                            width=10, height=1,
                            bg=BUTTON_COLOR, bd=4,
                            cursor="hand2",
                            command=window.destroy)
        button.place(relx=.5, rely=.7, anchor="center")

    def make_turn_on_event(self, event):
        """Event on-click on board to set Piece"""

        if self._cur_player.get_name().startswith("AI"):
            return
        x = BoardGui.round_cell(event.x - self._padding, self._cell_width) + self._padding
        y = BoardGui.round_cell(event.y - self._padding, self._cell_width) + self._padding

        if self._padding / 2 < x < self._board_width - self._padding / 2 and \
                self._padding / 2 < y < self._board_width - self._padding / 2:

            position = chr(ord('a') + round((x - self._padding) / self._cell_width)) + \
                       str(self._config.get_board_size() - round((y - self._padding) / self._cell_width) + 1)

            if position not in self._pieces:
                p = BoardGui.create_circle(self._board_canvas, x, y, self._piece_radius,
                                           fill=self._cur_player.get_color())
                self._board_canvas.pack()
                self._pieces.append(Piece(p, position, self._cur_player.get_color()))
                self._send_set_action(position)
                self._next()

    def make_turn(self, position, **kwargs):

        # if kwargs["color"] != self._cur_player.get_color():
        #     print("Wrong color")

        if position not in self._pieces:
            column = ord(position[0]) - ord('a')
            row = self._config.get_board_size() - int(position[1:]) + 1

            x = self._padding + self._cell_width * column
            y = self._padding + self._cell_width * row

            if self._padding / 2 < x < self._board_width - self._padding / 2 and \
                    self._padding / 2 < y < self._board_width - self._padding / 2:
                p = BoardGui.create_circle(self._board_canvas, x, y, self._piece_radius,
                                           fill=self._cur_player.get_color())
                self._pieces.append(Piece(p, position, self._cur_player.get_color()))
                self._next()

    def _switch_player(self):
        if self._cur_player == self._p1:
            self._cur_player = self._p2
        else:
            self._cur_player = self._p1
        self._turn.set(self._cur_player.get_name())
        self._info_frame.update_idletasks()

    def back(self, catch=False):
        cur = self._moves.get()
        if cur != 0:
            if catch:
                self._cur_player.undo_catch()
            p = self._pieces.pop()
            self._board_canvas.delete(p.get_piece())
            self._switch_player()
            self._moves.set(self._moves.get() - 1)
            self.send_delete_action(p.get_pos())

    def _next(self, catch=False):
        if catch:
            self._cur_player.catch()
        self._moves.set(self._moves.get() + 1)
        self._switch_player()
        if self._cur_player.get_name().startswith("AI"):
            data = json.loads(self._receive_func())
            method = self.__getattribute__(data["method"])
            method(**data['arguments'])

    def _send_set_action(self, position):
        arguments = {
            "position": position,
            "color": self._cur_player.get_color(),
        }
        self._send_func(method="make_turn", arguments=arguments)

    def send_delete_action(self, position):
        arguments = {
            "position": position,
            "color": self._cur_player.get_color(),
        }
        self._send_func(method="delete", arguments=arguments)

    def get_cur_player_name(self):
        return self._cur_player.get_name()

    def get_info_frame_rel_x(self):
        return self._info_frame.place_info()['relx']

    @staticmethod
    def create_circle(canvas, x, y, r, **kwargs):
        circle = canvas.create_oval(x - r, y - r, x + r, y + r, **kwargs)
        canvas.update_idletasks()
        return circle

    @staticmethod
    def round_cell(x, base):
        return base * round(x / base)

    def to_json(self):
        return json.dumps(self.__dict__())

    def __dict__(self):
        return {
            "size": self._config.get_board_size(),
            "turn": self._turn.get(),
            "moves": self._moves.get(),
            "current_player": self._cur_player.get_name(),
            "players": [self._p1.__dict__(), self._p2.__dict__()],
            "pieces": [p.__dict__() for p in self._pieces]
        }
