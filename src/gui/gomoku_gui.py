import json
import tkinter as ttk
import webbrowser as wb
from game_config import GameConfig
from constants import *
from board import Board


class GomokuGui:

    def __init__(self, width=WIN_WIDTH, heigth=WIN_HEIGHT):
        self._root = ttk.Tk()

        self._root.title('Gomoku')
        self._root.geometry(f"{width}x{heigth}")
        self._root.config(bg=BACKGROUND_COLOR)
        self._root.update()

        self._config = None
        self._board = None
        self._info_panel = None

        self._client = None

    def start(self):
        self.print_config()
        self._root.mainloop()

    def print_config(self):
        """Initialize Config menu and create game"""
        frame = ttk.Frame(self._root,
                          width=self._root.winfo_width(),
                          height=self._root.winfo_height(),
                          bg=BACKGROUND_COLOR)
        frame.pack()
        frame.place(relx=.5, rely=.5, anchor="center")

        copy_right = ttk.Label(frame,
                               text='© 21 School, 2022',
                               font=(FONT, COPYRIGHT_FONT_SIZE),
                               bg=BACKGROUND_COLOR)
        copy_right.place(relx=.5, rely=.97, anchor="center")

        welcome = ttk.Label(frame,
                            text='Welcome to Gomoku',
                            font=(FONT, LABEL_FONT_SIZE, "bold"),
                            bg=BACKGROUND_COLOR)
        welcome.place(relx=.5, rely=.1, anchor="center")

        game_rules = ttk.Label(frame,
                               text='Game rules',
                               font=(FONT, LABEL_FONT_SIZE, "underline", "bold"),
                               cursor="hand2",
                               bg=BACKGROUND_COLOR)
        game_rules.bind("<Button-1>", lambda e: wb.open_new("https://cdn.intra.42.fr/pdf/pdf/42138/en.subject.pdf"))
        game_rules.place(relx=.5, rely=.8, anchor="center")

        ch_mode = ttk.Label(frame,
                            text='Game mode:',
                            font=LABEL_FONT,
                            bg=BACKGROUND_COLOR)
        ch_mode.place(relx=.5, rely=.3, anchor="center")

        b1 = ttk.Button(frame,
                        text="Player VS AI",
                        font=BUTTON_FONT,
                        width=30, height=1,
                        bg=BUTTON_COLOR,
                        bd=4,
                        cursor="hand2")
        b1.place(relx=.5, rely=.4, anchor="center")

        b2 = ttk.Button(frame,
                        text="Player VS Player",
                        font=BUTTON_FONT,
                        width=30, height=1,
                        bg=BUTTON_COLOR,
                        bd=4,
                        cursor="hand2")
        b2.place(relx=.5, rely=.5, anchor="center")

        diff = ttk.Label(frame, text='Difficult', font=BUTTON_FONT, bg=BACKGROUND_COLOR)
        diff.place(relx=.35, rely=.59, anchor="center")

        hard = ttk.StringVar()
        hard.set("EASY")
        r1 = ttk.OptionMenu(frame, hard, "EASY", "MEDIUM", "HARD")
        r1.configure(font=BUTTON_FONT,
                     width=OPTION_MENU_WIDTH, height=OPTION_MENU_HEIGHT,
                     bg=BUTTON_COLOR, bd=4, cursor="hand2")
        drop = self._root.nametowidget(r1.menuname)
        drop.config(font=BUTTON_FONT, bg=BOARD_COLOR)
        r1.place(relx=.35, rely=.65, anchor="center")

        b_size = ttk.Label(frame, text='Board size', font=BUTTON_FONT, bg=BACKGROUND_COLOR)
        b_size.place(relx=.5, rely=.59, anchor="center")

        board_size = ttk.StringVar()
        board_size.set("19 x 19")
        r2 = ttk.OptionMenu(frame, board_size, "15 x 15", "19 x 19")
        r2.configure(font=BUTTON_FONT,
                     width=OPTION_MENU_WIDTH, height=OPTION_MENU_HEIGHT,
                     bg=BUTTON_COLOR, bd=4, cursor="hand2")
        drop = self._root.nametowidget(r2.menuname)
        drop.config(font=BUTTON_FONT, bg=BOARD_COLOR)
        r2.place(relx=.5, rely=.65, anchor="center")

        color_l = ttk.Label(frame, text='Color', font=BUTTON_FONT, bg=BACKGROUND_COLOR)
        color_l.place(relx=.65, rely=.59, anchor="center")

        color = ttk.StringVar()
        color.set("BLACK")
        r1 = ttk.OptionMenu(frame, color, "BLACK", "WHITE")
        r1.configure(font=BUTTON_FONT,
                     width=OPTION_MENU_WIDTH, height=OPTION_MENU_HEIGHT,
                     bg=BUTTON_COLOR, bd=4, cursor="hand2")
        drop = self._root.nametowidget(r1.menuname)
        drop.config(font=BUTTON_FONT, bg=BOARD_COLOR)
        r1.place(relx=.65, rely=.65, anchor="center")

        b1.configure(command=lambda: self.start_game(
            GameConfig.create("PvE", hard.get(), board_size.get(), color.get())))
        b2.configure(command=lambda: self.start_game(
            GameConfig.create("PvP", hard.get(), board_size.get(), color.get())))

    def start_game(self, config):
        self._config = config

        for widget in self._root.winfo_children():
            widget.destroy()

        self._board = Board(self._root, config, self.send_action())
        self._board.print_board()
        self._board.print_info()

        back = ttk.Button(self._root, text="Back",
                          font=BUTTON_FONT,
                          width=20, height=1,
                          bg=BUTTON_COLOR, bd=4,
                          cursor="hand2")
        back.configure(command=self._board.back)
        back.place(relx=self._board.get_info_frame_rel_x(), rely=.7, anchor="center")

        back = ttk.Button(self._root, text="Restart",
                          font=BUTTON_FONT,
                          width=20, height=1,
                          bg=BUTTON_COLOR, bd=4,
                          cursor="hand2")
        back.configure(command=self.restart_game)
        back.place(relx=self._board.get_info_frame_rel_x(), rely=.95, anchor="center")

    def restart_game(self):
        for widget in self._root.winfo_children():
            widget.destroy()
        self.print_config()

    def print_winner(self):
        winner = ttk.Label(self._root,
                           text=f"{self._board.get_cur_player_name()} WINS",
                           font=(FONT, LABEL_FONT_SIZE, "bold"),
                           bg=BACKGROUND_COLOR)
        winner.place(relx=self._board.get_info_frame_rel_x(), rely=.825, anchor="center")

    def send_action(self):
        """Send player action to server"""
        def send(action, msg):
            res = {
                "action": action,
                "position": msg
            }
            print(f"Client send message: {json.dumps(res)}")
        return send


if __name__ == '__main__':
    gui = GomokuGui(WIN_WIDTH, WIN_HEIGHT)
    gui.start()
