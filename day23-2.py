#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 23: Amphipod, part 2

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

import numpy as np

task = getAoC(23, 2021, example='all')
task['example'][11]
task['real'] = task['real'][:3] + ['  #D#C#B#A#','  #D#B#A#C#'] + task['real'][3:]


#
# set PRICE per step, per amphipod type
#

PRICE = {'A':1, 'B': 10, 'C': 100, 'D': 1000}


#
# set CAVE cell ids
#

CAVE = np.array([['#','#','#','#','#','#','#','#','#','#','#','#','#'],
                 ['#', 16, 17, -1, 18, -1, 19, -1, 20, -1, 21, 22,'#'],
                 ['#','#','#',  3,'#',  7,'#', 11,'#', 15,'#','#','#'],
                 ['#','#','#',  2,'#',  6,'#', 10,'#', 14,'#','#','#'],
                 ['#','#','#',  1,'#',  5,'#',  9,'#', 13,'#','#','#'],
                 ['#','#','#',  0,'#',  4,'#',  8,'#', 12,'#','#','#'],
                 ['#','#','#','#','#','#','#','#','#','#','#','#','#']])


#
# create a dataset of PATHS containing the distance between each set of cells, and which cells are on its path
#

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
# cell_explorer(16, verbose=True)

def cave_explorer():

    distance = {}
    for n in range(22+1):
        distance[n] = cell_explorer(n)

    # remove useless moves: moves between groups
    groups = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19,20,21,22]]
    for group in groups:
        for i,v in enumerate(group[:-1]):
            for i2,v2 in enumerate(group[i+1:]):
                del distance[v][v2]
                del distance[v2][v]

    return distance


PATHS = cave_explorer()


#
# load game state from task, return board
#

def load_board(joblist):

    board = []
    for n in range(22+1):
        coor = np.argwhere(CAVE==str(n))[0]
        board.append(joblist[coor[0]][coor[1]])
    return board
# board = load_board(task['example'][11])


#
# print the cave, or the board
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

# some shortcuts
def p(cost,board):
    print_cave(board)
    print('cost =',cost[0], flush=False)
    print(flush=True)
# p([0],board)


#
# get the distance from a cell to another cell, or False if impossible because the target or an intermediate cell is occupied
#

def check_path(pos_from, pos_to, board):

    # check if target is free
    if board[pos_to] != '.': return False

    # check if inbetween points are free
    for pos in PATHS[pos_from][pos_to][1]:
        if board[pos] != '.':
            return False

    # return length of path
    return PATHS[pos_from][pos_to][0]
# check_path(3,16, board)
# check_path(16,12, board)


#
# check if an amphipod is at a suitable home cell, or if there is a home cell he can go to right away
#

def check_home(board, amphipos):

    # get amphipos' letter
    letter = board[amphipos]

    # get all their home positions
    if letter == 'A': homes = [0,1,2,3]
    if letter == 'B': homes = [4,5,6,7]
    if letter == 'C': homes = [8,9,10,11]
    if letter == 'D': homes = [12,13,14,15]

    # check if it's in a good home: in a correct cell and all cells below are the same letter
    athome = False
    if amphipos in homes:
        athome = np.all([board[i]==letter for i in homes[:homes.index(amphipos)]])

    # is a home cell available? (first free cell in his home column, only if there are no other letters below)
    goal = False
    if not athome:
        for i in homes:
            if board[i] == '.':
                if cost := check_path(amphipos, i, board):
                    goal = (i, cost)
                break
            if board[i] != letter:
                break

    return (athome, goal)
# check_home(board, 7)
# check_home(board, 0)


#
# move an amphipod to a new position on the board (!need to check_path first!)
#

def move_amphipod(oldpos, newpos, distance, board, price):
    board[newpos] = board[oldpos]
    board[oldpos] = '.'
    price[0] += PRICE[board[newpos]] * distance
# board = load_board(task['example'][11])
# cost = [0]
# move_amphipod(15, 22, 3, board, cost)
# move_amphipod(14, 16, 10, board, cost)
# move_amphipod(13, 17, 10, board, cost)
# move_amphipod(12, 18, 9, board, cost)
# check_home(board,22)
# move_amphipod(22, 12, 6, board, cost)
# p(cost, board)


#
# check if a board has the desired final outcome
#

def check_solution(board):
    if board[:16] == ['A']*4+['B']*4+['C']*4+['D']*4:
        return True
    else:
        return False
# check_solution(board)


#
# make it so
#

def task23b(joblist, verbose=False):

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

        # for every amphipod on the board
        for pos,val in [(pos,val) for (pos,val) in enumerate(board) if val != '.']:
            # pos = cave field ID, val = amphipod letter on that field

            # check if this amphipod is at home or can go home
            athome, goal = check_home(board, pos)
            if athome:
                # at home: no more options for this bloke
                continue
            if goal is not False:
                # can go home: add it to the priority list
                move_opts_home.append((pos, goal[0], goal[1]))
                continue

            # check all places in the hallway that he can go
            for n in [k for k in PATHS[pos].keys() if 16 <= k <= 22]:  # n = next field
                if c := check_path(pos, n, board):  # c = cost
                    move_opts.append((pos, n, c))

        # if we can move something home, that is definitely the best move we can make: do it; otherwise try the other options
        if move_opts_home:
            move_opts = [move_opts_home[0]]

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

    print('answer 23b:',answer)
# task23b(task['example'][11])  # 44169
# task23b(task['real'])  # 48304


# benchmark
benchmark("task23b(task['example'][11])", 1)
benchmark("task23b(task['real'])", 1)
