#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(10)

input = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''.split('\n')

input = get_input(10, lines=True)

# parse input into numpy array, find starting point
grid = np.array([['.']*len(input[0])]*len(input))
for row,i in enumerate(input):
    for col,char in enumerate([*i]):
        grid[row, col] = char
        if char == 'S':
            start = [row, col]

pipe_directions = {'S': [[-1,0],[0,-1],[0,+1],[+1,0]],
    '|': [[-1,0],[+1,0]],
    '-': [[0,-1],[0,+1]],
    'L': [[-1,0],[0,+1]],
    'J': [[0,-1],[-1,0]],
    '7': [[0,-1],[+1,0]],
    'F': [[+1,0],[0,+1]] }

def get_neighbours(A):
    try:
        directions = pipe_directions[ grid[*A] ]
        return [ [x[0]+A[0], x[1]+A[1]] for x in directions]
    except (IndexError, KeyError):
        return []

tube_ends = [] # currently known ends for the tube
trace = [start] # all points we've been
steps = 0 # steps taken

# find points where the grid could be starting (always 2 points, as per the task)
tube_ends = [n for n in get_neighbours(start) if start in get_neighbours(n)]
trace.extend(tube_ends)
steps += 1

# find next points
while len(tube_ends):
    tube_ends = [n for end in tube_ends for n in get_neighbours(end) if n not in trace]
    trace.extend(tube_ends)
    steps += 1

# submit
submit(10, 1, steps-1) # 7107


#
# part 2
#
get_task(10)