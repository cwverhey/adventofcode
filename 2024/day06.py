#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname('__file__')); import aoc

#
# part 1
#

aoc.task(2024, 6, 1)

from collections import Counter

#inputs = aoc.examples(2024, 6)[0]  # correct answer: 41
inputs = aoc.get_input(2024, 6)

directions = (-1,0), (0,1), (1,0), (0,-1)

pos = [(i,x.index('^')) for i,x in enumerate(inputs) if '^' in x][0]
path = [pos]
dir = 0

while True:
    nextpos = tuple(sum(x) for x in zip(pos, directions[dir]))
    if not 0 <= nextpos[0] < len(inputs) or not 0 <= nextpos[1] < len(inputs[0]):
        break
    elif inputs[ nextpos[0] ][ nextpos[1] ] == '#':
        dir = (dir+1) % 4
    else:
        pos = nextpos
        path.append(pos)

unique_positions = len(Counter(path))

aoc.submit(2024, 6, 1, unique_positions)

#
# part 2
#

aoc.task(2024, 6, 2)

from copy import deepcopy


def run_rounds(start_map: list, start_path: dict, extra_obstacle: tuple = None):
    directions = (-1,0), (0,1), (1,0), (0,-1)

    pos = list(start_path.keys())[-1][0:2]
    dir = list(start_path.keys())[-1][2]
    map = deepcopy(start_map)
    path = deepcopy(start_path)

    if extra_obstacle:
        visited_positions = {pos[0:2]:None for pos in start_path}
        if extra_obstacle in visited_positions:
            return ['been_there', path]
        map[extra_obstacle[0]][extra_obstacle[1]] = '#'

    while True:
        nextpos = [sum(x) for x in zip(pos, directions[dir])]
        if not 0 <= nextpos[0] < len(map) or not 0 <= nextpos[1] < len(map[0]):
            return ['exit', path]
        elif map[ nextpos[0] ][ nextpos[1] ] == '#':
            dir = (dir+1) % 4
        else:
            pos = nextpos
            if (*pos, dir) in path:
                return ['loop', path]
            path[(*pos, dir)] = None


#inputs = aoc.examples(2024, 6)[0]  # correct answer: 6
inputs = aoc.get_input(2024, 6)

pos = [[i,x.index('^')] for i,x in enumerate(inputs) if '^' in x][0]
map = [list(line) for line in inputs]
dir = 0
start_path = { (*pos, dir): None }
result, original_path = run_rounds(map, start_path)
assert result == 'exit'

obstacles = {'exit': {}, 'loop': {}, 'been_there': {}}
for i in range(1,len(original_path)):
    print(f'{i}/{len(original_path)}')
    start_path = dict(list(original_path.items())[:i])
    obstacle = list(original_path.keys())[i][:2]
    result, _ = run_rounds(map, start_path, obstacle)
    print(i, obstacle, start_path, result)
    obstacles[result][obstacle] = None

unique_positions = len(obstacles['loop'])

aoc.submit(2024, 6, 2, unique_positions)

aoc.push_git(2024, 6)