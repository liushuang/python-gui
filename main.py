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

window.title("")

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
            bg_color = "green"
        elif snake[i][j] == 3:
            bg_color = "red"

        label = tk.Label(bg=bg_color, width=2, height=1)
        padx = 0
        pady = 0
        if i == 0 or i == height + 1 or j == 0 or j == width +1:
            padx = 1
            pady = 1
        label.grid(row=i, column=j, ipadx=padx, ipady=pady)
        row.append(label)
    labels.append(row)

def create_bean():
    global bean_row
    global bean_cell
    # random.seed(0)
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
snake_tail_row=head_row
snake_tail_cell =head_cell
def print_snake():
    for row in range(height+2):
        print(snake[row])

def bfs(temp_map, from_r, from_c, step):
    next_search = []
    test_direction_order =["up","down", "left", "right"]
    random.shuffle(test_direction_order)

    for test_direction in test_direction_order:
        if test_direction == "up":
            if temp_map[from_r - 1][from_c] != -1 and temp_map[from_r - 1][from_c] > step + 1:
                temp_map[from_r - 1][from_c] = step + 1
                next_search.append((from_r - 1, from_c))
        elif test_direction == "down":
            if temp_map[from_r + 1][from_c] != -1 and temp_map[from_r + 1][from_c] > step + 1:
                temp_map[from_r + 1][from_c] = step + 1
                next_search.append((from_r + 1, from_c))
        elif test_direction == "left":
            if temp_map[from_r][from_c - 1] != -1 and temp_map[from_r][from_c - 1] > step + 1:
                temp_map[from_r][from_c - 1] = step + 1
                next_search.append((from_r, from_c - 1))
        elif test_direction == "right":
            if temp_map[from_r][from_c + 1] != -1 and temp_map[from_r][from_c + 1] > step + 1:
                temp_map[from_r][from_c + 1] = step + 1
                next_search.append((from_r, from_c + 1))

    for (r,w) in next_search:
        bfs(temp_map,r,w,step+1)

def find_next_move(temp_map, r, c):
    step = temp_map[r][c]
    if step == 2:
        return (r, c)
    test_nextmove_order = ["up", "down", "left", "right"]
    random.shuffle(test_nextmove_order)
    for next_move in test_nextmove_order:
        if next_move == "up":
            if temp_map[r-1][c] == step - 1:
                return find_next_move(temp_map, r-1, c)
        elif next_move == "down":
            if temp_map[r+1][c] == step - 1:
                return find_next_move(temp_map, r+1, c)
        elif next_move == "left":
            if temp_map[r][c-1] == step - 1:
                return find_next_move(temp_map, r, c-1)
        elif next_move == "right":
            if temp_map[r][c+1] == step - 1:
                return find_next_move(temp_map, r, c+1)

def can_move_to(from_r, from_c, to_r, to_c):
    if from_r == to_r and from_c == to_c:
        return (from_r, from_c)
    temp_map = [[sys.maxsize for i in range(width + 2)] for j in range(height + 2)]
    for r in range(height+2):
        for c in range(width+2):
            if snake[r][c] == 1 or snake[r][c] == 2:
                temp_map[r][c] = -1
    temp_map[from_r][from_c] = 1
    temp_map[to_r][to_c] = sys.maxsize
    bfs(temp_map, from_r, from_c, 1)
    # for row in range(height+2):
    #     print(temp_map[row])
    if temp_map[to_r][to_c] < sys.maxsize:
        return find_next_move(temp_map, to_r, to_c)
    return (-1,-1)

def do_wonder():
    global direction
    test_direction_order = []
    # 豆子在右下方
    if snake_tail_row >= head_row and snake_tail_cell >= head_cell:
        test_direction_order.append("up")
        test_direction_order.append("left")
        test_direction_order.append("right")
        test_direction_order.append("down")
    # 豆子在左下方
    elif snake_tail_row >= head_row and snake_tail_cell <= head_cell:
        test_direction_order.append("up")
        test_direction_order.append("right")
        test_direction_order.append("left")
        test_direction_order.append("down")
    # 豆子在右上方
    elif snake_tail_row <= head_row and snake_tail_cell >= head_cell:
        test_direction_order.append("left")
        test_direction_order.append("down")
        test_direction_order.append("right")
        test_direction_order.append("up")
    # 豆子在左上方
    elif snake_tail_row <= head_row and snake_tail_cell <= head_cell:
        test_direction_order.append("down")
        test_direction_order.append("right")
        test_direction_order.append("left")
        test_direction_order.append("up")
    if head_row == 2:
        test_direction_order.remove("up")
        test_direction_order.append("up")
    if head_row == height -1:
        test_direction_order.remove("down")
        test_direction_order.append("down")
    if head_cell == 2:
        test_direction_order.remove("left")
        test_direction_order.append("left")
    if head_cell == width - 1:
        test_direction_order.remove("right")
        test_direction_order.append("right")

    for test_direction in test_direction_order:
        if test_direction == "down":
            if snake[head_row+1][head_cell] == 0 or snake[head_row+1][head_cell] == 3:
                if can_move_to(head_row + 1, head_cell, snake_tail_row, snake_tail_cell) != (-1,-1):
                    direction = "down"
                    return
        elif test_direction == "up":
            if snake[head_row - 1][head_cell] == 0 or snake[head_row - 1][head_cell] == 3:
                if can_move_to(head_row - 1, head_cell, snake_tail_row, snake_tail_cell) != (-1,-1):
                    direction = "up"
                    return
        elif test_direction == "right":
            if snake[head_row][head_cell + 1] == 0 or snake[head_row][head_cell + 1] == 3:
                if can_move_to(head_row, head_cell + 1, snake_tail_row, snake_tail_cell) != (-1,-1):
                    direction = "right"
                    return
        elif test_direction == "left":
            if snake[head_row][head_cell - 1] == 0 or snake[head_row][head_cell - 1] == 3:
                if can_move_to(head_row, head_cell - 1, snake_tail_row, snake_tail_cell) != (-1,-1):
                    direction = "left"
                    return

    print("wonder fail")
    print_snake()

def choose_next_step():
    global direction
    # 如果可以吃到豆子
    (row, cell) = can_move_to(head_row, head_cell, bean_row, bean_cell)
    if row != -1:
        (can_reach_r, can_reach_c) = can_move_to(row, cell, snake_tail_row, snake_tail_cell)
        # 如果往下走一步，就不能存活，尝试wonder
        if can_reach_r == -1:
            return do_wonder()
        # 如果可以存活，则走向豆子
        if row == head_row + 1:
            direction = "down"
        elif row == head_row -1:
            direction = "up"
        elif cell == head_cell + 1:
            direction = "right"
        else:
            direction = "left"
    else:
        do_wonder()


def move():
    global head_row
    global head_cell
    global snake_tail_row
    global snake_tail_cell
    global snake_length
    time.sleep(10)
    while True:
        choose_next_step()
        time.sleep(0.03)
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
            if next_row != snake_tail_row or next_cell != snake_tail_cell:
                tkinter.messagebox.showerror(message="failed")
                break
        labels[head_row][head_cell].configure(bg="blue")
        labels[next_row][next_cell].configure(bg="green")
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
            snake_length = snake_length + 1
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