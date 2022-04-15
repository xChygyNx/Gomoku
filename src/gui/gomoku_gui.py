import tkinter as ttk
import webbrowser as wb
from game_config import GameConfig
from constants import *
from board import Board
from info_panel import InfoPanel


class GomokuGui:

    def __init__(self, width=WIN_WIDTH, heigth=WIN_HEIGHT):
        self._root = ttk.Tk()

        self._root.title('Gomoku')
        self._root.geometry(f"{width}x{heigth}")
        self._root.config(bg=BACKGROUND_COLOR)
        self._root.update()

        self._info_panel = None
        self._board = None
        self._config = None

    def start(self):
        self.__welcome__()
        self._root.mainloop()

    def __welcome__(self):
        frame = ttk.Frame(self._root,
                          width=self._root.winfo_width(),
                          height=self._root.winfo_height(),
                          bg=BACKGROUND_COLOR)
        frame.pack()
        frame.place(relx=.5, rely=.5, anchor="center")

        cright = ttk.Label(frame,
                           text='© 21 School, 2022',
                           font=('Arial', 10),
                           bg=BACKGROUND_COLOR)
        cright.place(relx=.5, rely=.97, anchor="center")

        welcome = ttk.Label(frame,
                            text='Welcome to Gomoku',
                            font=('Arial', 20, "bold"),
                            bg=BACKGROUND_COLOR)
        welcome.place(relx=.5, rely=.1, anchor="center")

        game_rules = ttk.Label(frame,
                               text='Game rules',
                               font=('Arial', 20, "underline", "bold"),
                               cursor="hand2",
                               bg=BACKGROUND_COLOR)
        game_rules.bind("<Button-1>", lambda e: wb.open_new("https://cdn.intra.42.fr/pdf/pdf/42138/en.subject.pdf"))
        game_rules.place(relx=.5, rely=.8, anchor="center")

        ch_mode = ttk.Label(frame,
                            text='Game mode:',
                            font=('Arial', 20),
                            bg=BACKGROUND_COLOR)
        ch_mode.place(relx=.5, rely=.3, anchor="center")

        b1 = ttk.Button(frame,
                        text="Player VS AI",
                        font=('Arial', 15),
                        width=30, height=1,
                        bg=BUTTON_COLOR, highlightbackground=HIGHLIGHT_COLOR,
                        bd=4,
                        cursor="hand2")
        b1.place(relx=.5, rely=.4, anchor="center")

        b2 = ttk.Button(frame,
                        text="Player VS Player",
                        font=('Arial', 15),
                        width=30, height=1,
                        bg=BUTTON_COLOR,
                        bd=4,
                        cursor="hand2")
        b2.place(relx=.5, rely=.5, anchor="center")

        diff = ttk.Label(frame, text='Difficult', font=('Arial', 15), bg=BACKGROUND_COLOR)
        diff.place(relx=.35, rely=.59, anchor="center")

        hard = ttk.StringVar()
        hard.set("EASY")
        r1 = ttk.OptionMenu(frame, hard, "EASY", "MEDIUM", "HARD")
        r1.configure(font=('Arial', 15), width=8, height=1, bg=BUTTON_COLOR, bd=4, cursor="hand2")
        drop = self._root.nametowidget(r1.menuname)
        drop.config(font=('Arial', 15), bg=BOARD_COLOR)
        r1.place(relx=.35, rely=.65, anchor="center")

        b_size = ttk.Label(frame, text='Board size', font=('Arial', 15), bg=BACKGROUND_COLOR)
        b_size.place(relx=.5, rely=.59, anchor="center")

        board_size = ttk.StringVar()
        board_size.set("19 x 19")
        r2 = ttk.OptionMenu(frame, board_size, "15 x 15", "19 x 19")
        r2.configure(font=('Arial', 15), width=8, height=1, bg=BUTTON_COLOR, bd=4, cursor="hand2")
        drop = self._root.nametowidget(r2.menuname)
        drop.config(font=('Arial', 15), bg=BOARD_COLOR)
        r2.place(relx=.5, rely=.65, anchor="center")

        f_move = ttk.Label(frame, text='First move', font=('Arial', 15), bg=BACKGROUND_COLOR)
        f_move.place(relx=.65, rely=.59, anchor="center")

        first = ttk.StringVar()
        first.set("BLACK")
        r1 = ttk.OptionMenu(frame, first, "BLACK", "WHITE")
        r1.configure(font=('Arial', 15), width=8, height=1, bg=BUTTON_COLOR, bd=4, cursor="hand2")
        drop = self._root.nametowidget(r1.menuname)
        drop.config(font=('Arial', 15), bg=BOARD_COLOR)
        r1.place(relx=.65, rely=.65, anchor="center")

        b1.configure(command=lambda: self.game(GameConfig.create("PvE", hard.get(), board_size.get(), first.get())))
        b2.configure(command=lambda: self.game(GameConfig.create("PvP", hard.get(), board_size.get(), first.get())))

    def game(self, config):
        self._config = config
        self._board = Board(self._root, config.get_board_size())
        self._info_panel = InfoPanel(self._root, self._config)

        for widget in self._root.winfo_children():
            widget.destroy()

        self._board.print_board()
        self._info_panel.print_info()


if __name__ == '__main__':
    gui = GomokuGui(1200, 800)
    gui.start()
