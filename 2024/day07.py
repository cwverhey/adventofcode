#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 7, 1)


#inputs = aoc.examples(2024, 7, lines=True)[0]  # correct answer: 3749
inputs = aoc.get_input(2024, 7, lines=True)


def get_outcomes(n: list) -> list:
    """
    Get all possible outcomes for a list of numbers
    """
    outcomes = [
        [ n[0]+n[1] , *n[2:] ],
        [ n[0]*n[1] , *n[2:] ]
    ]
    if len(n) == 2:
        return [ o[0] for o in outcomes ]
    else:
        return [ o2 for o1 in outcomes for o2 in get_outcomes(o1) ]


# iterate over all input lines, sum all possible targets
possible_cum = 0
for i in inputs:
    i = i.split(': ')
    target = int(i[0])
    numbers = [int(x) for x in i[1].split(' ')]
    print(f'target: {target}, numbers: {numbers}, outcomes:', end=' ')
    outcomes = get_outcomes(numbers)
    print(target in outcomes)
    if target in outcomes:
        possible_cum += target

# submit answer
aoc.submit(2024, 7, 1, possible_cum)


#
# part 2
#

aoc.task(2024, 7, 2)


def get_outcomes_v2(n: list) -> list:
    """
    Get all possible outcomes for a list of numbers
    """
    outcomes = [
        [ n[0]+n[1] , *n[2:] ],
        [ n[0]*n[1] , *n[2:] ],
        [ int(str(n[0]) + str(n[1])) , *n[2:] ]
    ]
    if len(n) == 2:
        return [ o[0] for o in outcomes ]
    else:
        return [ o2 for o1 in outcomes for o2 in get_outcomes_v2(o1) ]

#inputs = aoc.examples(2024, 7, lines=True)[0]  # correct answer: 11387
inputs = aoc.get_input(2024, 7, lines=True)

# iterate over all input lines, sum all possible targets
possible_cum = 0
for i,instruction in enumerate(inputs):
    instruction = instruction.split(': ')
    target = int(instruction[0])
    numbers = [int(x) for x in instruction[1].split(' ')]
    print(f'[{i+1}/{len(inputs)}] target: {target}, numbers: {numbers}, outcomes:', end=' ')
    outcomes = get_outcomes_v2(numbers)
    print(target in outcomes)
    if target in outcomes:
        possible_cum += target

#
# part 2 take 2: depth-first should work faster (return as soon as one possible outcome matches)
#


def check_outcome(target: int, n: list) -> bool:
    """
    Check if a given target can be reached with the given list of numbers, and the operators +, *, and ||
    """
    outcomes = [
        [ n[0]+n[1] , *n[2:] ],
        [ n[0]*n[1] , *n[2:] ],
        [ int(str(n[0]) + str(n[1])) , *n[2:] ]
    ]
    if len(n) == 2:
        return [target] in outcomes
    else:
        for o in outcomes:
            if check_outcome(target, o):
                return True
        return False


#inputs = aoc.examples(2024, 7, lines=True)[0]  # correct answer: 11387
inputs = aoc.get_input(2024, 7, lines=True)


# iterate over all input lines, sum all possible targets
possible_cum = 0
for i,instruction in enumerate(inputs):
    instruction = instruction.split(': ')
    target = int(instruction[0])
    numbers = [int(x) for x in instruction[1].split(' ')]
    print(f'[{i+1}/{len(inputs)}] target: {target}, numbers: {numbers}, valid:', end=' ')
    valid = check_outcome(target, numbers)
    print(valid)
    if valid:
        possible_cum += target

# submit answer
aoc.submit(2024, 7, 2, possible_cum)

# push to git
aoc.push_git(2024, 7)