#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#
aoc.task(2024, 1)
aoc.examples(2024, 1)[0]
inputs = aoc.get_input(2024, 1, numeric=True)

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
aoc.submit(2024, 1, 1, cum_diff)

#
# part 2
#
aoc.task(2024, 1, 2)

# sum similarity score
cum_similarity = 0
for i, v in enumerate(lists[0]):
    cum_similarity += v * lists[1].count(v)

# submit answer
aoc.submit(2024, 1, 2, cum_similarity)