#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(11)

input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''.split('\n')

input = get_input(11, lines=True)

# parse into numpy array
grid = np.array([[*i] for i in input])

def printgrid():
    for row in grid:
        print(''.join(row).replace('.','⬜️').replace('#','⭐️'))

# expand universe
# rows
for row,vals in reversed(list(enumerate(grid))):
    if all(vals == '.'):
        grid = np.insert(grid, row, '.', axis=0)
# columns
for col,vals in reversed(list(enumerate(grid.T))):
    if all(vals == '.'):
        grid = np.insert(grid, col, '.', axis=1)

# get (IDs of) all pairs of stars
stars = np.argwhere(grid == '#')
pairidxs = np.stack(np.triu_indices(len(stars), k=1), axis=1)

# find distances
distance_sum = 0
for idxs in pairidxs:
    distance_sum += abs(stars[idxs[1]][0] - stars[idxs[0]][0]) + abs(stars[idxs[1]][1] - stars[idxs[0]][1])

submit(11, 1, distance_sum) # distance_sum


#
# part 2
#
get_task(11)

input = '''...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....'''.split('\n')

input = get_input(11, lines=True)

# parse into numpy array
grid = np.array([[*i] for i in input])

def printgrid():
    for row in grid:
        print(''.join(row).replace('.','⬜️').replace('#','⭐️'))

# find rows and columns to expand in this universe
# rows
expanding_rows = [ row for row,vals in enumerate(grid) if all(vals == '.')]
expanding_cols = [ col for col,vals in enumerate(grid.T) if all(vals == '.')]

# get (IDs of) all pairs of stars
stars = np.argwhere(grid == '#')
pairidxs = np.stack(np.triu_indices(len(stars), k=1), axis=1)

# find distances
distance_sum = 0
expansion_rate = 1000000 - 1
for idxs in pairidxs:
    rows = sorted([stars[idxs[1]][0], stars[idxs[0]][0]])
    row_expansions = expansion_rate * len([row for row in expanding_rows if rows[0] < row < rows[1]])
    cols = sorted([stars[idxs[1]][1], stars[idxs[0]][1]])
    col_expansions = expansion_rate * len([col for col in expanding_cols if cols[0] < col < cols[1]])
    distance_sum += rows[1]-rows[0] + row_expansions + cols[1]-cols[0] + col_expansions

submit(11, 2, distance_sum) # 644248339497