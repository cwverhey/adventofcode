#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys; sys.path.append(os.path.dirname(__file__)); import aoc

import os; os.chdir(os.path.expanduser('~/Progs/adventofcode/2024/'))
import helper
helper.update_cookie()

#
# part 1
#
helper.get_task(day=1, year=2024)
input = helper.get_input(day=1, year=2024, numeric=True)

# split into 2 lists
lists = [[],[]]
for i,val in enumerate(input):
    lists[i%2].append(val)

# sort lists
lists[0].sort()
lists[1].sort()

# sum difference
cum_diff = 0
for i,v1 in enumerate(lists[0]):
    v2 = lists[1][i]
    cum_diff += abs(v1 - v2)

# submit answer
helper.submit(year=2024, day=1, part=1, answer=cum_diff)

#
# part 2
#
helper.get_task(year=2024, day=1)

# sum similarity score
cum_similarity = 0
for i, v in enumerate(lists[0]):
    cum_similarity += v * lists[1].count(v)

# submit answer
helper.submit(year=2024, day=1, part=2, answer=cum_similarity)