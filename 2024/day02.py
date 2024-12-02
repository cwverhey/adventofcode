#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 2, 1)

#inputs = aoc.examples(2024, 2, lines=True)[0]
inputs = aoc.get_input(2024, 2, lines=True)

cum_safe = 0
for line in inputs:
    levels = [int(x) for x in line.split()]
    safe = True
    increasing = levels[0] < levels[1]
    for i,l1 in enumerate(levels[:-1]):
        l2 = levels[i+1]
        if (l1 < l2) != increasing or abs(l1 - l2) < 1 or abs(l1 - l2) > 3:
            safe = False
    if safe:
        cum_safe += 1

aoc.submit(2024, 2, 1, cum_safe)

#
# part 2
#

aoc.task(2024, 2, 2)

def is_safe(levels):
    increasing = levels[0] < levels[1]
    for i,l1 in enumerate(levels[:-1]):
        l2 = levels[i+1]
        if (l1 < l2) != increasing or abs(l1 - l2) < 1 or abs(l1 - l2) > 3:
            return False
    return True

cum_safe = 0
for line in inputs:
    levels = [int(x) for x in line.split()]
    safe = is_safe(levels)
    if safe:
        cum_safe += 1
        continue
    for i in range(0, len(levels)):
        levels_sub = levels.copy()
        del levels_sub[i]
        if is_safe(levels_sub) and not safe:
            safe = True
            cum_safe += 1
            continue

aoc.submit(2024, 2, 2, cum_safe)

aoc.push_git(2024, 2)