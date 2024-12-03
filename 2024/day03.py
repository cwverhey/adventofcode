#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 3, 1)

import re

#inputs = aoc.examples(2024, 3, lines=True)[0]
inputs = aoc.get_input(2024, 3, raw=True)

muls = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', inputs)

cum_mul = sum([int(m[0]) * int(m[1]) for m in muls])

aoc.submit(2024, 3, 1, cum_mul)

#
# part 2
#

aoc.task(2024, 3, 2)

instructions = re.findall(r'(mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\))', inputs)

cum_mul = 0
do = True
for instr in instructions:
    if instr == 'do()':
        do = True
    elif instr == 'don\'t()':
        do = False
    else:
        if do:
            values = re.search(r'mul\((\d{1,3}),(\d{1,3})\)', instr).groups()
            cum_mul += int(values[0]) * int(values[1])
        
aoc.submit(2024, 3, 2, cum_mul)

aoc.push_git(2024, 3)