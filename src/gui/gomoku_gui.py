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

        self._board = Board(self._root)
        self._config = GameConfig()

    def start(self):
        self.__welcome__()
        self._root.mainloop()

    def __welcome__(self):
        frame = ttk.Frame(self._root,
                          width=self._root.winfo_width(),
                          height=self._root.winfo_height() / 2,
                          bg=BACKGROUND_COLOR)
        frame.pack()
        frame.place(width=WIN_WIDTH, height=WIN_HEIGHT)

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
        game_rules.place(relx=.5, rely=.7, anchor="center")

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

        b1.configure(command=lambda: self.__choose_diff__(frame, ch_mode, b1, b2))
        b2.configure(command=lambda: self.game(self._config.pvp_mode()))

    def __choose_diff__(self, frame, ch_mode, b1, b2):
        config = GameConfig().pve_mode()

        ch_mode.configure(text="Choose difficulty:")
        b1.configure(text="EASY", command=lambda: self.game(config.easy()))
        b2.configure(text="MEDIUM", command=lambda: self.game(config.medium()))
        b3 = ttk.Button(frame,
                        text="HARD",
                        font=('Arial', 15),
                        width=30, height=1,
                        bg=BUTTON_COLOR,
                        bd=4,
                        cursor="hand2",
                        command=lambda: self.game(config.hard()))
        b3.place(relx=.5, rely=.6, anchor="center")

    def game(self, config):
        for widget in self._root.winfo_children():
            widget.destroy()
        self._board.print_board()


if __name__ == '__main__':
    gui = GomokuGui()
    gui.start()
