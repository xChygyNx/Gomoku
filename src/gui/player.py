import tkinter as ttk
from constants import BOARD_COLOR


class Player:

    def __init__(self, win, name, color):
        self._win = win
        self._name = ttk.Label(self._win, text=name, font=("Arial", 20), bg=BOARD_COLOR)
        self._count = ttk.IntVar()
        self._catches = ttk.Label(self._win, textvariable=self._count, font=("Arial", 20), bg=BOARD_COLOR)
        self._color = color

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

    def get_color(self):
        return self._color

    def __eq__(self, other):
        if self.get_name() == other.get_name():
            return True
        else:
            return False
