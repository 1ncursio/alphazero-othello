from GameBorder import Border
from Qagent import Qplayer
from tkinter import *
import tkinter.font as tkFont
from functools import partial
import numpy as np
import pickle
import time
root = Tk()
root.geometry('240x240')

helv36 = tkFont.Font(family='Helvetica', size=15, weight=tkFont.BOLD)


border = Border()
border.reset()

with open('qValue.p', 'rb') as f:
    tableData = pickle.load(f)

player = Qplayer(-1)
player.states_value = tableData
player.exp_rate = 0

check = False


def reStart():
    global check
    check = False
    border.reset()
    mapLoad()


def mapLoad():
    contaier.delete('all')
    contaier.create_rectangle(0, 0, 240, 240, width=0.0, fill='#00A0FF')
    contaier.create_line(80, 0, 80, 240, width=2.0, fill='#0077BB')
    contaier.create_line(160, 0, 160, 240, width=2.0, fill='#0077BB')
    contaier.create_line(0, 80, 240, 80, width=2.0, fill='#0077BB')
    contaier.create_line(0, 160, 240, 160, width=2.0, fill='#0077BB')

    state = np.reshape(border.state, [9])
    for index, s in enumerate(state):
        x = (index % 3) * 80 + 10
        y = int(index / 3) * 80 + 10
        if s == np.float(1.0):
            contaier.create_oval(x, y, x + 60, y + 60,
                                 width=2.0, outline='#FFFFFF')

        elif s == np.float(-1.0):
            contaier.create_line(x, y, x + 60, y + 60,
                                 width=2.0, fill='#5D5D5D')
            contaier.create_line(x + 60, y, x, y + 60,
                                 width=2.0, fill='#5D5D5D')


def change_label_number(event):
    global check

    if(check):
        reStart()
        return

    x = int(event.x / 80)
    y = int(event.y / 80)
    if x < 0 or 2 < x or y < 0 or 2 < y:  # 범위 외
        return
    action = (y, x)

    position = border.availablePositions()

    if action not in position or check:
        return

    border.step(action, 1)
    mapLoad()

    position = border.availablePositions()

    action = player.chooseAction(position, border.state)

    border.step(action, -1)

    mapLoad()

    if(border.done):
        check = True
        print('게임끝')

        return
        # reStart()

    if len(border.availablePositions()) == 1:
        check = True
        print('무승부')

        # reStart()
        return


contaier = Canvas(width=240, height=240, highlightthickness=0)
contaier.bind('<Button-1>', change_label_number)
contaier.pack()


mapLoad()
root.mainloop()
