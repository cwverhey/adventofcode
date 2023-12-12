#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(9)

input = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''.split('\n')

input = get_input(9, lines = True)

def predict(lst):
    delta = [lst[i+1] - lst[i] for i in range(len(lst)-1)]
    return lst[-1] + delta[0] if len(set(delta)) == 1 else lst[-1] + predict(delta)

prediction_sum = 0
for i in input:
    i = [int(n) for n in i.split(' ')]
    prediction_sum += predict(i)

submit(9, 1, prediction_sum)

#
# part 2
#
get_task(9)

input = '''0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45'''.split('\n')

input = get_input(9, lines = True)

def predict(lst):
    delta = [lst[i+1] - lst[i] for i in range(len(lst)-1)]
    return lst[0] - delta[0] if len(set(delta)) == 1 else lst[0] - predict(delta)

prediction_sum = 0
for i in input:
    i = [int(n) for n in i.split(' ')]
    prediction_sum += predict(i)

submit(9, 2, prediction_sum)