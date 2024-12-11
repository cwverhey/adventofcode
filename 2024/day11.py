#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 11, 1)

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
from math import log10

#inputs = [125, 17]  # correct answer: 55312 @ 25 blinks
inputs = aoc.get_input(2024, 11, numeric=True)

def digs(num):
  '''faster than int(log10(num))+1'''
  if num < 10:
    return 1
  elif num < 100:
    return 2
  elif num < 1000:
    return 3
  elif num < 10_000:
    return 4
  elif num < 100_000:
    return 5
  elif num < 1_000_000:
    return 6
  elif num < 10_000_000:
    return 7
  elif num < 100_000_000:
    return 8
  elif num < 1_000_000_000:
    return 9
  elif num < 10_000_000_000:
    return 10
  elif num < 100_000_000_000:
    return 11
  elif num < 1_000_000_000_000:
    return 12
  else:
    return -1

def blink_num(num):
    if num == 0:
        return [1]
    digits = digs(num)
    if digits % 2 == 0:
        divisor = 10**(digits//2)
        return [ num // divisor, num % divisor ]
    return [ num*2024 ]

def blink(nums, times):
    for i in range(times):
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