#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 25, 1)

from itertools import product


#inputs = aoc.examples(2024, 25, lines=True)[0]  # correct answer: 3
inputs = aoc.get_input(2024, 25, lines=True)  # 3287

locks = []
keys = []

inputs.append('')
new = [-1,-1,-1,-1,-1]
for line in inputs:
    if line == '':
        if is_key:
            keys.append(new)
        else:
            locks.append(new)
        new = [-1,-1,-1,-1,-1]
        continue
    for i, val in enumerate(line):
        new[i] += val == '#'
    is_key = line == '#####'


count_possible = sum([max([x + y for x, y in zip(lock, key)]) <= 5 for lock, key in product(locks, keys)])

# submit answer
aoc.submit(2024, 25, 1, count_possible)

# push to git
# aoc.push_git(2024, 25)