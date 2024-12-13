#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 13, 1)

# pushing A: 3 tokens, pushing B: 1 token

import re
import sympy

#inputs = aoc.examples(2024, 13, lines=True)[0]  # correct answer: 480
inputs = aoc.get_input(2024, 13, lines=True)

machines = []
for line in inputs:
    if line.startswith('Button A'):
        a = tuple(int(x) for x in re.findall(r'\d+', line))
    elif line.startswith('Button B'):
        b = tuple(int(x) for x in re.findall(r'\d+', line))
    elif line.startswith('Prize'):
        target = tuple(int(x) for x in re.findall(r'\d+', line))
        machines.append(tuple([a, b, target]))

total_price = 0
for m in machines:
    A, B = sympy.symbols('A B')
    eqs = [ sympy.Eq( m[0][i]*A + m[1][i]*B, m[2][i] ) for i in range(2)]
    solution = sympy.solve(eqs, (A, B))
    print(eqs, solution)
    if all(isinstance(x, sympy.core.numbers.Integer) for x in solution.values()):
        total_price += solution[A]*3+solution[B]

# submit answer
aoc.submit(2024, 13, 1, total_price)


#
# part 2
#

aoc.task(2024, 13, 2)

inputs = aoc.examples(2024, 13)[0]  # correct answer: ____
#inputs = aoc.get_input(2024, 13)

____

# submit answer
aoc.submit(2024, 13, 2, ____)

# push to git
aoc.push_git(2024, 13)