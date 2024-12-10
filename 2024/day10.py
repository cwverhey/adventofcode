#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 10, 1)

#inputs = aoc.examples(2024, 10)[4]  # correct answer: 36
inputs = aoc.get_input(2024, 10)


def neighbours(map, pos):
    '''Get valid neighbouring coordinates'''
    neighbours = [ dir+pos for dir in [(-1, 0), (0, 1), (1, 0), (0, -1)] ]
    return [ n for n in neighbours if 0 <= n[0] < map.shape[0] and 0 <= n[1] < map.shape[1] ]

def stepup(map, start_poss, target_level):
    '''Get unique list of neighbouring coordinates of given value'''
    return np.unique([n for pos in start_poss for n in neighbours(map,pos) if map[*n] == target_level], axis=0)

def score(map, trailhead_pos):
    '''Get score for a given trailhead'''
    start = [trailhead_pos]
    for lvl in range(1,10):
        start = stepup(map, start, lvl)
    return len(start)

map = np.array([list(line) for line in inputs], int)
trailheads = np.argwhere(map == 0)

cum_score = 0
for t in trailheads:
    cum_score += score(map, t)

# submit answer
aoc.submit(2024, 10, 1, cum_score)


#
# part 2
#

aoc.task(2024, 10, 2)

#inputs = aoc.examples(2024, 10)[4]  # correct answer: 81
inputs = aoc.get_input(2024, 10)

def stepup(map, start_poss, target_level):
    '''Get list of neighbouring coordinates of given value'''
    return [n for pos in start_poss for n in neighbours(map,pos) if map[*n] == target_level]

map = np.array([list(line) for line in inputs], int)
trailheads = np.argwhere(map == 0)

cum_score = 0
for t in trailheads:
    cum_score += score(map, t)

# submit answer
aoc.submit(2024, 10, 2, cum_score)

# push to git
aoc.push_git(2024, 10)