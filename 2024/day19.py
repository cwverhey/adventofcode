#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 19, 1)


def tryToMakeTarget(target, towels):
    for towel in towels:
        if target.startswith(towel):
            if target == towel or tryToMakeTarget(target[len(towel):], towels):
                return True
    return False


#inputs = aoc.examples(2024, 19, lines=True)[0]  # correct answer: 6
inputs = aoc.get_input(2024, 19, lines=True)

towels = inputs[0].split(', ')
targets = inputs[2:]

reduced_towels = []
for t in sorted(towels, key=len):
    if not tryToMakeTarget(t, reduced_towels):
        reduced_towels.append(t)

possible_targets = sum([ tryToMakeTarget(t, reduced_towels) for t in targets ])

# submit answer
aoc.submit(2024, 19, 1, possible_targets)


#
# part 2
#

aoc.task(2024, 19, 2)

def countTowelOptions(target):
    options = 0
    for i in range(1, len(target)+1):
        if target[:i] in towels:
            remaining_target = target[i:]
            if not remaining_target in cache:
                cache[remaining_target] = countTowelOptions(remaining_target)
            options += cache[remaining_target]
    return options


#inputs = aoc.examples(2024, 19, lines=True)[0]  # correct answer: 16
inputs = aoc.get_input(2024, 19, lines=True)

towels = set([k for k in inputs[0].split(', ')])
targets = inputs[2:]
cache = {'': 1}

options = sum([ countTowelOptions(t) for t in targets ])

# submit answer
aoc.submit(2024, 19, 2, options)

# push to git
# aoc.push_git(2024, 19)