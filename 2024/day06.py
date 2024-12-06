#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname('__file__')); import aoc

#
# part 1
#

aoc.task(2024, 6, 1)

from collections import Counter

#inputs = aoc.examples(2024, 6, lines=True)[0]  # correct answer: 41
inputs = aoc.get_input(2024, 6, lines=True)

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

def run_rounds(map, pos, dir):
    directions = (-1,0), (0,1), (1,0), (0,-1)
    path = [ [*pos, dir] ]
    while True:
        nextpos = [sum(x) for x in zip(pos, directions[dir])]
        if not 0 <= nextpos[0] < len(map) or not 0 <= nextpos[1] < len(map[0]):
            return ['exit', path]
        elif map[ nextpos[0] ][ nextpos[1] ] == '#':
            dir = (dir+1) % 4
        else:
            pos = nextpos
            if [*pos, dir] in path:
                return ['loop', path]
            path.append( [*pos, dir] )
                

#inputs = aoc.examples(2024, 6, lines=True)[0]  # correct answer: 6
inputs = aoc.get_input(2024, 6, lines=True)

pos = [[i,x.index('^')] for i,x in enumerate(inputs) if '^' in x][0]
dir = 0
_, potential_obstacle_positions = run_rounds(inputs, pos, dir)

obstacle_positions = []
for i,p in enumerate(potential_obstacle_positions[1:]):
    print(f'{i+1}/{len(potential_obstacle_positions)}: ', end='')
    newmap = inputs.copy()
    newmap[ p[0] ] = newmap[ p[0] ][ :p[1] ] + '#' + newmap[ p[0] ][ p[1]+1: ]
    result, _ = run_rounds(newmap, pos, dir)
    print(result)
    if result == 'loop':
        obstacle_positions.append(p[0:2])

unique_positions = len(Counter([tuple(x) for x in obstacle_positions]))

aoc.submit(2024, 6, 2, unique_positions)

aoc.push_git(2024, 6)