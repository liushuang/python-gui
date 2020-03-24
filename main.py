#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import threading
import time as time
import random
import queue
import keyboard
import sys

window = tk.Tk()

window.title("My window")

window.geometry('500x500')
width = 5
height = 5

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
snake_tail_row=0
snake_tail_cell =0
bean_row = 0
bean_cell = 0
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
    global bean_row
    global bean_cell
    while True:
        w = int(random.random() * width + 1)
        h = int(random.random() * height + 1)
        if snake[h][w] == 0:
            snake[h][w] = 3
            labels[h][w].configure(bg="red")
            bean_row = h
            bean_cell = w
            break

create_bean()


def bfs(temp_map, row, cell, step):
    next_search = []
    if temp_map[row + 1][cell] > step + 1:
        temp_map[row + 1][cell] = step + 1
        next_search.append((row + 1, cell))
    if temp_map[row - 1][cell] > step + 1:
        temp_map[row - 1][cell] = step + 1
        next_search.append((row - 1, cell))
    if temp_map[row][cell + 1] > step + 1:
        temp_map[row][cell + 1] = step + 1
        next_search.append((row, cell + 1))
    if temp_map[row][cell - 1] > step + 1:
        temp_map[row][cell - 1] = step + 1
        next_search.append((row, cell - 1))
    for (r,w) in next_search:
        bfs(temp_map,r,w,step+1)

def find_next_move(temp_map, r, c):
    step = temp_map[r][c]
    if step == 2:
        return (r, c)
    if temp_map[r-1][c] == step - 1:
        return find_next_move(temp_map, r-1, c)
    if temp_map[r+1][c] == step - 1:
        return find_next_move(temp_map, r+1, c)
    if temp_map[r][c-1] == step - 1:
        return find_next_move(temp_map, r, c-1)
    if temp_map[r][c+1] == step - 1:
        return find_next_move(temp_map, r, c+1)

def can_move_to_bean():
    temp_map = [[sys.maxsize for i in range(width + 2)] for j in range(height + 2)]
    for r in range(height+2):
        for c in range(width+2):
            if snake[r][c] == 1 or snake[r][c] == 2:
                temp_map[r][c] = -1
    temp_map[head_row][head_cell] = 1
    bfs(temp_map, head_row, head_cell, 1)
    for row in range(height+2):
        print(temp_map[row])
    if temp_map[bean_row][bean_cell] < sys.maxsize:
        return find_next_move(temp_map, bean_row, bean_cell)
    return (-1,-1)

def choose_next_step():
    global direction
    # 如果可以吃到豆子
    (row, cell) = can_move_to_bean()
    if row != -1:
        if row == head_row + 1:
            direction = "down"
        elif row == head_row -1:
            direction = "up"
        elif cell == head_cell + 1:
            direction = "right"
        else:
            direction = "left"
      # 测试往下走一步，能否存活？

    # wonder一步



def move():
    global head_row
    global head_cell
    global snake_tail_row
    global snake_tail_cell
    while True:
        choose_next_step()
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
            snake_tail_row = r
            snake_tail_cell = w
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
