#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 23: Amphipod, part 1

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

import numpy as np

task = getAoC(23, 2021)
task['example']
task['real']

#
# set cost per amphipod step
#
PRICE = {'A':1, 'B': 10, 'C': 100, 'D': 1000}

#
# create a dataset `paths` on distance between each set of points, and which points are on its path
#
CAVE = np.array([['#','#','#','#','#','#','#','#','#','#','#','#','#'],
                 ['#',  8,  9, -1, 10, -1, 11, -1, 12, -1, 13, 14,'#'],
                 ['#','#','#',  1,'#',  3,'#',  5,'#',  7,'#','#','#'],
                 ['#','#','#',  0,'#',  2,'#',  4,'#',  6,'#','#','#'],
                 ['#','#','#','#','#','#','#','#','#','#','#','#','#']])


def cell_explorer(cell, verbose=False):
    my_coor = np.argwhere(CAVE==str(cell))[0]
    my_val = CAVE[my_coor[0],my_coor[1]]
    if verbose: print('coor:', my_coor)
    if verbose: print('value:', my_val)

    def walk_into(init_coor, distance, parent, blockades):
        points = {}
        for new_direction in [[-1,0],[1,0],[0,-1],[0,1]]:
            coor = init_coor + new_direction
            val = CAVE[coor[0],coor[1]]
            if verbose: print('\t'*distance, coor, '=',val)
            if val != '#' and np.any(coor != parent):
                if val != '-1':
                    points.update({int(val): (distance+1, blockades)})
                    subblocks = blockades + [int(val)]
                else:
                    subblocks = blockades
                if verbose: print('\t'*distance, 'walk into, distance =',distance+1, 'parent =',init_coor, 'blockades =',subblocks)
                points.update(walk_into(coor, distance+1, init_coor, subblocks))

        return points

    points = walk_into(my_coor, 0, my_coor, [])

    return dict(sorted(points.items()))
# cell_explorer(0, verbose=True)

def cave_explorer():

    distance = {}
    for n in range(15):
        distance[n] = cell_explorer(n)

    # remove useless moves
    groups = [[0,1],[2,3],[4,5],[6,7],[8,9,10,11,12,13,14]]
    for group in groups:
        for i,v in enumerate(group[:-1]):
            for i2,v2 in enumerate(group[i+1:]):
                del distance[v][v2]
                del distance[v2][v]

    return distance


PATHS = cave_explorer()


#
# load game state into board
#
def load_board(joblist):

    board = []
    for n in range(15):
        coor = np.argwhere(CAVE==str(n))[0]
        board.append(joblist[coor[0]][coor[1]])
    return board

# board = load_board(task['example'])

#
# print the cave or the board
#
def print_cave(board=False):
    rows, cols = CAVE.shape
    for row in range(rows):
        for col in range(cols):
            if board is False:
                if CAVE[row,col] == '#':
                    print('███', end='', flush=False)
                else:
                    print(CAVE[row,col].rjust(2), end=' ', flush=False)
            else:
                cell = CAVE[row,col]
                if cell.isdigit():
                    print('',board[int(cell)], end=' ', flush=False)
                elif cell == '-1':
                    print(' . ', end='', flush=False)
                else:
                    print('███', end='', flush=False)
        print()
# print_cave()
# print_cave(board)


def p(cost,board):
    print_cave(board)
    print('cost =',cost[0], flush=True)
# p()


#
# figure out which next steps we can take
#


# get the distance to another location, or False if impossible
def check_path(pos_from, pos_to, board):

    # check if target is free
    if board[pos_to] != '.': return False

    # check if inbetween points are free
    for pos in PATHS[pos_from][pos_to][1]:
        if board[pos] != '.':
            return False

    # return length of path
    return PATHS[pos_from][pos_to][0]
# check_path(1,8, board)
# check_path(1,5, board)

# check if an amphipod is already at home, or if there is a home he can go to right away
def check_home(board, amphipos):

    letter = board[amphipos]

    # get all home positions
    if letter == 'A': homes = [0,1]
    if letter == 'B': homes = [2,3]
    if letter == 'C': homes = [4,5]
    if letter == 'D': homes = [6,7]

    # check if we're at home
    athome = False
    if homes[0] == amphipos: athome = True
    if homes[1] == amphipos and board[homes[0]] == letter: athome = True

    # which homes are suitable goals
    goal = False
    if not athome:
        # give bottom bunk as option, if available
        if cost := check_path(amphipos, homes[0], board):
            goal = (homes[0], cost)
        # if the bottom bunk is already filled correctly, ánd the top one is available, give top bunk as option
        elif board[homes[0]] == letter:
            if cost := check_path(amphipos, homes[1], board):
                goal = (homes[1], cost)

    return (athome, goal)
# check_home(board, 7)


# move an amphipod to a new position (need to verify if possible first!)
def move_amphipod(oldpos, newpos, distance, board, price):
    board[newpos] = board[oldpos]
    board[oldpos] = '.'
    price[0] += PRICE[board[newpos]] * distance
# cost = [0]
# move_amphipod(1, 9, 2, cost, board)
# p()


# check if a board has the solution
def check_solution(board):
    if board[:8] == ['A','A','B','B','C','C','D','D']:
        return True
    else:
        return False


def task23a(joblist, verbose=False):

    # load paths and board
    board = load_board(joblist)
    cost = [0]
    best_solution = [999999999999]

    def try_all_options(debug=False):

        # show board state
        if debug:
            p(cost, board)
            print('', flush=False)

        # get options for current board state
        move_opts_home = []
        move_opts = []
        # for every letter on the board
        for pos,val in enumerate(board):  # pos = cave field ID, val = letter on that field
            if val != '.':
                # check if we are home or can go home
                athome, goal = check_home(board, pos)
                if athome:
                    continue
                if goal is not False:
                    move_opts_home.append((pos, goal[0], goal[1]))
                # check all places we cán go
                else:
                    for n in [k for k in PATHS[pos].keys() if 8 <= k <= 14]:  # n = next field
                        if c := check_path(pos, n, board):  # c = cost
                            move_opts.append((pos, n, c))

        # if we can move something home, do it; otherwise use the other options
        if move_opts_home:
            move_opts = move_opts_home

        # show options
        if debug: print('option list:\n',move_opts, flush=False)

        if move_opts:
            for o in move_opts:
                if debug: print(o[0], '->', o[1], flush=False)
                move_amphipod(o[0], o[1], o[2], board, cost)
                if cost[0] < best_solution[0]:
                   try_all_options(debug)
                else:
                    if debug: print('over budget!', flush=False)
                if debug: print(o[0], '<-', o[1], flush=False)
                move_amphipod(o[1], o[0], -o[2], board, cost)
        elif check_solution(board) and cost[0] < best_solution[0]:
            best_solution[0] = cost[0]

    try_all_options(verbose)
    answer = best_solution[0]

    print('answer 23a:',answer)
# task23a(task['example'])  # 12521
# task23a(task['real'])  # 16506

# benchmark
benchmark("task23a(task['real'])", 1)
