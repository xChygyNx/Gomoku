import tkinter
from tkinter import Radiobutton
from tkinter import BooleanVar


def config_window():
    window = tkinter.Tk()
    window.title('Chose configs of Gomoku game')
    window.geometry('500x600')
    difficult_lbl = tkinter.Label(window, text='Choose difficulty level of opponent',
                                  font=('Arial Bold', 20))
    difficult_lbl.place(x=0, y=0)
    r_var = BooleanVar()
    r_var.set(0)
    r1 = Radiobutton(text='First',
                     variable=r_var, value=0)
    r2 = Radiobutton(text='Second',
                     variable=r_var, value=1)
    r1.pack()
    r2.pack()
    color_lbl = tkinter.Label(window, text='Choose color of your title', font=('Arial Bold', '20'))
    color_lbl.place(x=0, y=100)
    window.mainloop()


if __name__ == '__main__':
    config_window()