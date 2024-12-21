#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 20, 1)

import numpy as np
#from collections import Counter

def view():
    for y in range(map_shape[1]):
        for x in range(map_shape[0]):
            if (y,x) in distances:
                val = str(distances[(y,x)]).rjust(2)
            elif map[y,x]:
                val = '⬛️'
            elif (y,x) == start:
                val = '🟩'
            elif (y,x) == end:
                val = '🟥'
            else:
                val = '⬜️'
            print(val, end=' ')
        print()

def add(tuple1, tuple2):
    '''Pairwise tuple addition'''
    return tuple([x + y for x, y in zip(tuple1, tuple2)])


#inputs = aoc.examples(2024, 20)[0]  # correct answer: 0
inputs = aoc.get_input(2024, 20)

map_all = np.array([ [ c for c in line[1:-1] ] for line in inputs[1:-1] ])
map_shape = map_all.shape
start = tuple(np.argwhere(map_all == 'S')[0].tolist())
end = tuple(np.argwhere(map_all == 'E')[0].tolist())
map = map_all == '#'
dirs = (0,-1), (1,0), (0,1), (-1,0)

# find & remember shortest distance from start (bfs) remember for all options
distance = 0
leaves = [start]
distances = {start: distance}
while True:
    new_leaves = []
    distance += 1
    for pos in leaves:
        for dir in dirs:
            new_pos = add(pos, dir)
            if 0 <= new_pos[0] < map_shape[0] and 0 <= new_pos[1] < map_shape[1] and map[new_pos] == False and new_pos not in distances:
                new_leaves.append(new_pos)
                distances[new_pos] = distance
    if end in new_leaves:
        break
    leaves = new_leaves

print(f'shortest distance without cheating: {distance}')
view()

# for each wall, check if it could connect two paths and how much faster it'd be
cheat_profits = []
for wall in np.argwhere(map == True):
    neighbours = [ add(wall.tolist(),dir) for dir in dirs ]
    neighbour_distances = [ distances[n] for n in neighbours if n in distances ]
    if len(neighbour_distances) > 1:
        saved_time = max(neighbour_distances) - min(neighbour_distances) - 2  # moving from one side to other side of wall takes 2ps
        if saved_time >= 100:
            cheat_profits.append(saved_time)

# submit answer
aoc.submit(2024, 20, 1, len(cheat_profits))


#
# part 2
#

aoc.task(2024, 20, 2)

import numpy as np
from itertools import combinations

#inputs = aoc.examples(2024, 20)[0]
inputs = aoc.get_input(2024, 20)

map_all = np.array([ [ c for c in line ] for line in inputs ])
map_shape = map_all.shape
start = tuple(np.argwhere(map_all == 'S')[0].tolist())
end = tuple(np.argwhere(map_all == 'E')[0].tolist())
map = map_all == '#'
dirs = (0,-1), (1,0), (0,1), (-1,0)

# find & remember shortest distance from start (bfs); remember for all points until the minimum length to the finish is reached
distance = 0
leaves = [start]
distances = {start: distance}
while True:
    new_leaves = []
    distance += 1
    for pos in leaves:
        for dir in dirs:
            new_pos = (pos[0]+dir[0], pos[1]+dir[1])
            if 0 <= new_pos[0] < map_shape[0] and 0 <= new_pos[1] < map_shape[1] and map[new_pos] == False and new_pos not in distances:
                new_leaves.append(new_pos)
                distances[new_pos] = distance
    if end in new_leaves:
        break
    leaves = new_leaves

# for each combo of two points with a known distance to start, check if those distances are more than 102 apart, check if the manhattan distance is 20 or less
cheats = 0
for (pos1, dist1), (pos2, dist2) in combinations(distances.items(), 2):
    if abs(dist1 - dist2) >= 102:
        shortcut_distance = abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
        if shortcut_distance <= 20 and abs(dist1 - dist2) - shortcut_distance >= 100:
            cheats += 1

# submit answer
aoc.submit(2024, 20, 2, cheats )

# push to git
# aoc.push_git(2024, 20)