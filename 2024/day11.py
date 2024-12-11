#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 11, 1)

# every blink, first applicable rule:
# 0 -> 1
# even number of digits -> 2 stones: left half of digits left stone, right half right stone
# -> * 2024

#inputs = [125, 17]  # correct answer: 55312
inputs = aoc.get_input(2024, 11, numeric=True)

def blink_num(num):
    if num == 0:
        return [1]
    if len(str(num)) % 2 == 0:
        digits = len(str(num))
        return [ int(str(num)[:digits//2]), int(str(num)[digits//2:]) ]
    return [ num*2024 ]

def blink(nums, times):
    for i in range(times):
        nums = [n_out for n_in in nums for n_out in blink_num(n_in)]
    return nums

stones = len(blink(inputs, 25))

# submit answer
aoc.submit(2024, 11, 1, stones)


#
# part 2
#

aoc.task(2024, 11, 2)

from collections import defaultdict

#inputs = [125, 17]  # correct answer: 55312 @ 25 blinks
inputs = aoc.get_input(2024, 11, numeric=True)

def blink(nums, times):
    for i in range(times):
        print(f'blink {i+1}:')
        result = defaultdict(lambda: 0)
        for n_in, count in nums.items():
            for n_out in blink_num(n_in):
                result[n_out] += count
        nums = result
    return nums

tally = {stone:1 for stone in inputs}  # eg: {125: 1, 17: 1}

stones = sum(blink(tally, 75).values())

# submit answer
aoc.submit(2024, 11, 2, stones)

# push to git
aoc.push_git(2024, 11)