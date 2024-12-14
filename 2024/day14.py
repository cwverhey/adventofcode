#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 14, 1)
# x0 = left
# y0 = top
# space wraps
# task: where are the robots after 100 steps
# safety_factor: Count robots in each quadrant, multiply. Ignore robots on centerline

import re
from math import ceil, prod
import numpy as np

#inputs = aoc.examples(2024, 14, lines=True)[0]  # correct answer: 12
#space = np.array([11, 7])
inputs = aoc.get_input(2024, 14, lines=True)
space = np.array([101, 103])


def quadrant(pos, center):
    if np.any(pos == center):
        return 4
    rel = [ pos[0] > center[0], pos[1] > center[1] ]
    quads = [ [False, False], [False, True], [True, False], [True, True] ]
    return quads.index(rel)

robots = [ [int(x) for x in re.findall(r'-?\d+', i)] for i in inputs ]  # px, py, vx, vy
robots = [ (np.array([r[0],r[1]]), np.array([r[2],r[3]])) for r in robots ]

space_center = space//2

quadrants = [0,0,0,0,0]
for r in robots:
    pos = (r[0] + r[1]*100) % space
    quadrants[ quadrant(pos, space_center) ] += 1

safety_factor = prod(quadrants[:4])

# submit answer
aoc.submit(2024, 14, 1, safety_factor)


#
# part 2
#

aoc.task(2024, 14, 2)

#inputs = aoc.examples(2024, 14, lines=True)[0]  # correct answer: 12
#space = np.array([11, 7])
inputs = aoc.get_input(2024, 14, lines=True)
space = np.array([101, 103])

from collections import Counter

robots = [ [int(x) for x in re.findall(r'-?\d+', i)] for i in inputs ]  # px, py, vx, vy
robots_p = [ [r[0],r[1]] for r in robots ]
robots_v = [ np.array([r[2],r[3]]) for r in robots ]

time = 0
#for i, v in enumerate(robots_v):
#    robots_p[i] = ((robots_p[i] + robots_v[i] * time) % space).tolist()
while True:
    if time % 100 == 0:
        print(time)
    colmax = max(Counter([p[0] for p in robots_p]).values())
    if colmax > 30:
        rowmax = max(Counter([p[1] for p in robots_p]).values())
        if rowmax > 20:
            for y in range( space[1] ):
                print(''.join(['◻️' if [x,y] in robots_p else '◼️' for x in range( space[0] )]))
            print(f'time: {time} seconds')
            if input('Correct? Y/N: ').lower() == 'y':
                break
    time += 1
    for i, v in enumerate(robots_v):
        robots_p[i] = ((robots_p[i] + robots_v[i]) % space).tolist()

# submit answer
aoc.submit(2024, 14, 2, time)

# push to git
# aoc.push_git(2024, 14)