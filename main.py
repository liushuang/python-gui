#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk 
import threading
import time as time

window = tk.Tk()

window.title("My window")

window.geometry('500x500')

labels =[]
for i in range(10):
    row = []
    for j in range(10):
        label = tk.Label(bg="red", width=1, height=1)
        label.grid(row=i, column=j)
        row.append(label)
    labels.append(row)

def change_color():
    for k in range(10):
        time.sleep(1)
        labels[k][k].configure(bg="yellow")

thr = threading.Thread(target=change_color)
thr.start()

window.mainloop()

