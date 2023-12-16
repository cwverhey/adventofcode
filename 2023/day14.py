#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(14)

input = '''O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....'''.split('\n')

input = get_input(14, lines=True)

# parse input
grid = np.reshape( np.fromiter(''.join(input), dtype='<U1'), (len(input),len(input[0])))

# iterate over columns, roll every stone to the top
for col in grid.T:
    newpos = 0
    for i,val in enumerate(col):
        if val == '#':
            newpos = i+1
        if val == 'O':
            col[i] = '.'
            col[newpos] = 'O'
            newpos += 1

# iterate over rows, summarise weight on north beam
weight_sum = 0
for i,row in enumerate(grid):
    rowweight = grid.shape[0] - i
    rolling_stones_num = len(np.where(row == 'O')[0])
    weight_sum += rowweight * rolling_stones_num

submit(14, 1, weight_sum) # 108840