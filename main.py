#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import threading
import time as time
import random
import queue
import keyboard

window = tk.Tk()

window.title("My window")

window.geometry('500x500')
width = 10
height = 10

# 0：空的, 白色
# 1：不可达，黑色
# 2：身体，蓝色
# 3：豆子，红色

snake = [[0 for i in range(width + 2)] for j in range(height + 2)]
for i in range(width + 2):
    snake[0][i] = 1
    snake[height + 1][i] = 1
for i in range(height + 2):
    snake[i][0] = 1
    snake[i][width + 1] = 1
head_row = int(height / 2)
head_cell = int(width / 2)
snake[head_row][head_cell] = 2
snake_length = 1
snake_queue = queue.Queue()
snake_queue.put((head_row, head_cell))

direction = "right"




labels = []
for i in range(height + 2):
    row = []
    for j in range(width + 2):
        bg_color = "black"
        if snake[i][j] == 0:
            bg_color = "white"
        elif snake[i][j] == 1:
            bg_color = "black"
        elif snake[i][j] == 2:
            bg_color = "blue"
        elif snake[i][j] == 3:
            bg_color = "red"

        label = tk.Label(bg=bg_color, width=1, height=1)
        label.grid(row=i, column=j)
        row.append(label)
    labels.append(row)

def create_bean():
    while True:
        w = int(random.random() * width + 1)
        h = int(random.random() * height + 1)
        if snake[h][w] == 0:
            snake[h][w] = 3
            labels[h][w].configure(bg="red")
            break

create_bean()

def move():
    global head_row
    global head_cell
    while True:
        time.sleep(0.3)
        next_row = head_row
        next_cell = head_cell
        if direction == "right":
            next_cell = next_cell + 1
        elif direction == "left":
            next_cell = next_cell - 1
        elif direction == "up":
            next_row = next_row - 1
        elif direction == "down":
            next_row = next_row + 1
        if snake[next_row][next_cell] == 1 or snake[next_row][next_cell] == 2:
            tkinter.messagebox.showerror(message="failed")
            break

        labels[next_row][next_cell].configure(bg="blue")

        snake_queue.put((next_row, next_cell))
        head_row = next_row
        head_cell = next_cell
        # 走到空白处
        if snake[next_row][next_cell] == 0:
            (r, w) = snake_queue.get()
            snake[r][w] = 0
            labels[r][w].configure(bg="white")
        # 吃豆子
        elif snake[next_row][next_cell] == 3:
            create_bean()
        snake[next_row][next_cell] = 2

def listen_keyboard(event):
    global direction
    if event.event_type == 'down':
        if event.name == "down" or event.name == "up" or event.name == "left" or event.name == "right":
            direction = event.name

thr = threading.Thread(target=move)
thr.start()
keyboard.hook(listen_keyboard)

window.mainloop()
