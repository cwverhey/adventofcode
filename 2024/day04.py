#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 4, 1)

# XMAS horizontal, vertical, diagonal, backwards
txt = 'XMAS'
#inputs = aoc.examples(2024, 4, lines=True)[1]  # answer: 18
inputs = aoc.get_input(2024, 4, lines=True)

txt_idxs = list(range(0, len(txt)))
offsets = [(0,1), (1,1), (1,0), (-1, 1)] # east, southeast, south, southwest (check forwards and backwards)

count_txt = 0
for x in range(len(inputs)):
    for y in range(len(inputs[0])):
        for xdir, ydir in offsets:
            positions = list(zip([x + xdir * i for i in txt_idxs], [y + ydir * i for i in txt_idxs]))
            chars = ''.join([inputs[p[0]][p[1]] for p in positions if 0 <= p[0] < len(inputs) and 0 <= p[1] < len(inputs[0])])
            if chars == txt or chars[::-1] == txt:
                #print(x, y, xdir, ydir)
                count_txt += 1

aoc.submit(2024, 4, 1, count_txt)

#
# part 2
#

aoc.task(2024, 4, 2)

#inputs = aoc.examples(2024, 4, lines=True)[1]  # correct answer: 9
inputs = aoc.get_input(2024, 4, lines=True)

count_x_mas = 0
offsets = [ (-1, -1), (1,1) ], [(-1,1), (1, -1)]
for x in range(1,len(inputs)-1):
    for y in range(1,len(inputs[0])-1):
        if inputs[x][y] == 'A':
            letters = set([ inputs[x-1][y-1], inputs[x+1][y+1] ]), set([ inputs[x-1][y+1], inputs[x+1][y-1] ])
            if letters == ({'M', 'S'}, {'M', 'S'}):
                count_x_mas += 1

aoc.submit(2024, 4, 2, count_x_mas)

aoc.push_git(2024, 4)