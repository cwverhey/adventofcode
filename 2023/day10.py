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
prettypipes = {'L': '╰', 'J': '╯', '7': '╮','F': '╭', '|': '│', '-': '─', '.': '·', 'S': 'S'}

grid = np.array([['']*len(input[0])]*len(input))
for row,i in enumerate(input):
    for col,char in enumerate([*i]):
        grid[row, col] = prettypipes[char]
        if char == 'S':
            start = [row, col]

def printgrid():
    for i in grid:
        print(''.join(i))

# find adjacent, connecting pipes
pipe_directions = {'S': [[-1,0],[0,-1],[0,+1],[+1,0]],
    '│': [[-1,0],[+1,0]],
    '─': [[0,-1],[0,+1]],
    '╰': [[-1,0],[0,+1]],
    '╯': [[0,-1],[-1,0]],
    '╮': [[0,-1],[+1,0]],
    '╭': [[+1,0],[0,+1]] }

def get_neighbours(A):
    try:
        directions = pipe_directions[ grid[*A] ]
        return [ [x[0]+A[0], x[1]+A[1]] for x in directions]
    except (IndexError, KeyError):
        return []

tube_ends = [] # currently known ends for the tube
trace = [] # points we've been right before the current tube_ends
steps = 0 # steps taken

# find tube ends connected to the start (always 2 points, as per the task)
tube_ends = [n for n in get_neighbours(start) if start in get_neighbours(n)]
trace = [start]
steps += 1

# find next points
while len(tube_ends):
    old_ends = tube_ends
    tube_ends = [n for end in tube_ends for n in get_neighbours(end) if n not in trace]
    trace = old_ends
    steps += 1

# submit
submit(10, 1, steps-1) # 7107


#
# part 2
#
get_task(10)

input = '''..F7.
.FJ|.
SJ.L7
|F--J
LJ...'''.split('\n')

input = '''...........
.S-------7.
.|F-----7|.
.||.....||F
.||.....||F
J|L-7.F-J|.
.|..|.|..|.
7L--J.L--J.
...........'''.split('\n')

input = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''.split('\n')

input = get_input(10, lines=True)

# parse input into numpy array, find starting point
prettypipes = {'L': '╰', 'J': '╯', '7': '╮','F': '╭', '|': '│', '-': '─', '.': '·', 'S': 'S'}

grid = np.array([['']*len(input[0])]*len(input))
for row,i in enumerate(input):
    for col,char in enumerate([*i]):
        grid[row, col] = prettypipes[char]
        if char == 'S':
            start = [row, col]

def printgrid():
    for i in grid:
        print(''.join(i))

# function to find adjacent, connecting pipes
pipe_directions = {'S': [[-1,0],[0,-1],[0,+1],[+1,0]],
    '│': [[-1,0],[+1,0]],
    '─': [[0,-1],[0,+1]],
    '╰': [[-1,0],[0,+1]],
    '╯': [[0,-1],[-1,0]],
    '╮': [[0,-1],[+1,0]],
    '╭': [[+1,0],[0,+1]] }

def get_neighbours(A):
    try:
        directions = pipe_directions[ grid[*A] ]
        return [ [x[0]+A[0], x[1]+A[1]] for x in directions]
    except (IndexError, KeyError):
        return []

# find all points on the main pipe: `trace[]`
tube_ends = [n for n in get_neighbours(start) if start in get_neighbours(n)] # ends connected to the start (always 2 points, as per the task)
trace = [start, *tube_ends]

while len(tube_ends): # next points
    tube_ends = [n for end in tube_ends for n in get_neighbours(end) if n not in trace]
    trace.extend(tube_ends)

# convert all pipe-symbols that are *not* part of the main pipe into '·'
for row in range(grid.shape[0]):
    for col in range(grid.shape[1]):
        if grid[row,col] != '·' and [row,col] not in trace:
            grid[row,col] = '·'

# iterate over all dots in grid, except the ones on the outside:
# * raycast to the right, count how many │ ╰ ╯ we encounter. Don't count ─ ╭ ╮
# * if number is uneven, we're inside the main pipe
inside_points_counter = 0
for row in range(1, grid.shape[0]-1):
    for col in range(1, grid.shape[1]-1):
        if grid[row,col] == '·':
            crossings = 0
            for c in range(col+1, grid.shape[1]):
                if grid[row,c] in ['│','╰','╯']:
                    crossings += 1
            #print(f'[{row},{col}]: {crossings}')
            if crossings%2 == 1:
                inside_points_counter += 1

submit(10, 2, inside_points_counter) # 281