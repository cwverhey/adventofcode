#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 25: Sea Cucumber

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

tasks = getAoC(25, 2021)
tasks['example']
tasks['real']


import numpy as np


def parse_task(task):
    lut = {'v': 2, '>': 1, '.': 0}
    arr = [[lut[x] for x in line] for line in task]
    return np.array(arr, dtype=np.uint8)
# board = parse_task(tasks['example'])


def printb(board):
    lut = {0: '·', 1: '→', 2: '↓'}
    for r in board:
        for v in r:
            print(lut[v], end='')
        print()
# printb(board)


def task25a(task, verbose=False):

    board = parse_task(task)
    rows, cols = board.shape
    steps = 1

    while 1:

        # move east
        curr_pos = np.array(np.where(board==1)) # get positions of current '>' cucumbers
        next_col = np.array((curr_pos[1]+1)%cols) # get their next position
        next_val = board[curr_pos[0],next_col] == 0 # check if next value == 0
        move = np.vstack((curr_pos[:,next_val],next_col[next_val])) # get 2D array of current and future positions for those that will move
        board[move[0],move[1]] = 0
        board[move[0],move[2]] = 1
        moved = np.any(next_val)

        # move south
        curr_pos = np.array(np.where(board==2)) # get positions of current '>' cucumbers
        next_row = np.array((curr_pos[0]+1)%rows) # get their next position
        next_val = board[next_row,curr_pos[1]] == 0 # check if next value == 0
        move = np.vstack((curr_pos[:,next_val],next_row[next_val])) # get 2D array of current and future positions for those that will move
        board[move[0],move[1]] = 0
        board[move[2],move[1]] = 2
        moved |= np.any(next_val)

        # print
        if verbose:
            print(f'** step {steps} **\nmoved: {moved}')
            printb(board)

        # break or reiterate
        if not moved:
            break
        steps += 1

    print('answer 25a:',steps)
# task25a(tasks['example'], verbose=True)  # 58
# task25a(tasks['real'], verbose=True)  # 520


# benchmark
benchmark("task25a(tasks['real'])", 25)
