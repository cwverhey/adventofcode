#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 12, 1)

#inputs = aoc.examples(2024, 12)[3]  # correct answer: 1930
inputs = aoc.get_input(2024, 12)

map = np.array([list(l) for l in inputs])

def neighbours(coord, map):
    n = np.empty((0,2), dtype=int)
    directions = (0,1), (1,0), (0, -1), (-1, 0)
    for dir in directions:
        pos = (dir+np.array(coord))
        if 0 <= pos[0] < map.shape[0] and 0 <= pos[1] < map.shape[1]:
            if map[*coord] == map[*pos]:
                n = np.vstack([n, pos])
    return n

total_price = 0
map_todo = {coord:None for coord in np.ndindex(map.shape)}
while map_todo:

    region_area = 0
    region_perimiter = 0
    region_todo = {map_todo.popitem()[0]: None}

    while region_todo:

        nbs = neighbours(region_todo.popitem()[0], map)
        region_area += 1
        region_perimiter += 4 - len(nbs)
        for n in nbs.tolist():
            n = tuple(n)
            try:
                region_todo[n] = map_todo.pop(n)
            except KeyError:
                pass

    total_price += region_area * region_perimiter

# submit answer
aoc.submit(2024, 12, 1, total_price)


#
# part 2
#

aoc.task(2024, 12, 2)

#inputs = aoc.examples(2024, 12)[0]  # correct answer: 80
inputs = aoc.get_input(2024, 12)

map = np.array([list(l) for l in inputs])

total_price = 0
map_todo = {coord:None for coord in np.ndindex(map.shape)}
while map_todo:

    region_area = 0
    region_perimiter = 0
    region_done = []
    region_todo = {map_todo.popitem()[0]: None}

    while region_todo:
        pos = region_todo.popitem()[0]
        nbs = neighbours(pos, map)
        region_done.append(pos)
        region_area += 1
        region_perimiter += 4 - len(nbs)
        for n in nbs.tolist():
            n = tuple(n)
            try:
                region_todo[n] = map_todo.pop(n)
            except KeyError:
                pass

    region_corners = 0
    scanranges = list(zip( np.min(region_done, axis=0)-1, np.max(region_done, axis=0)+1 ))
    for x in range(*scanranges[0]):
        for y in range(*scanranges[1]):
            quad = [ pos in region_done for pos in [ (x,y), (x,y+1), (x+1,y), (x+1,y+1) ] ]
            if sum(quad) in [1, 3]:
                region_corners += 1
            elif sum(quad) == 2 and quad in [ [True,False,False,True], [False,True,True,False] ]:
                region_corners += 2

    total_price += region_area * region_corners
    
# submit answer
aoc.submit(2024, 12, 2, total_price)

# push to git
aoc.push_git(2024, 12)