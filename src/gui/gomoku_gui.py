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
                           font=(FONT, COPYRIGHT_FONT_SIZE),
                           bg=BACKGROUND_COLOR)
        cright.place(relx=.5, rely=.97, anchor="center")

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
                        bg=BUTTON_COLOR, highlightbackground=HIGHLIGHT_COLOR,
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

        b1.configure(command=lambda: self.game(GameConfig.create("PvE", hard.get(), board_size.get(), color.get())))
        b2.configure(command=lambda: self.game(GameConfig.create("PvP", hard.get(), board_size.get(), color.get())))

    def game(self, config):
        self._config = config
        self._board = Board(self._root, config)

        for widget in self._root.winfo_children():
            widget.destroy()

        self._board.print_board()
        self._board.print_info()


if __name__ == '__main__':
    gui = GomokuGui(1200, 800)
    gui.start()
