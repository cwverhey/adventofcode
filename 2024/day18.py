#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 18, 1)

#inputs = aoc.examples(2024, 18)[0]  # correct answer: 2
#grid_max = 6
#bytes = 12
inputs = aoc.get_input(2024, 18)
grid_max = 70
bytes = 1024

history = {k:None for k in [ (int(pos[0]),int(pos[1])) for pos in [ str.split(',') for str in inputs[:bytes] ] ]}
directions = ( (0,-1), (1,0), (0,1), (-1,0) )
start = (0,0)
target = (grid_max, grid_max)

steps = 0
positions = [start]
history.update({k:None for k in positions})

while True:
    steps += 1
    new_positions = []
    for p in positions:
        for d in directions:
            new_pos = tuple([x + y for x, y in zip(p, d)])
            if 0 <= new_pos[0] <= grid_max and 0 <= new_pos[1] <= grid_max and not new_pos in history and not new_pos in new_positions:
                new_positions.append(new_pos)
    positions = new_positions
    if target in positions:
        print(steps)
        break
    history.update({k:None for k in positions})

# submit answer
aoc.submit(2024, 18, 1, 312)


#
# part 2
#

aoc.task(2024, 18, 2)


def try_maze(inputs, grid_max, bytes):
    history = {k:None for k in [ (int(pos[0]),int(pos[1])) for pos in [ str.split(',') for str in inputs[:bytes] ] ]}
    directions = ( (0,-1), (1,0), (0,1), (-1,0) )
    start = (0,0)
    target = (grid_max, grid_max)

    steps = 0
    positions = [start]
    history.update({k:None for k in positions})

    while True:
        steps += 1
        new_positions = []
        for p in positions:
            for d in directions:
                new_pos = tuple([x + y for x, y in zip(p, d)])
                if 0 <= new_pos[0] <= grid_max and 0 <= new_pos[1] <= grid_max and not new_pos in history and not new_pos in new_positions:
                    new_positions.append(new_pos)
        if not new_positions:
            return False
        if target in new_positions:
            #print(steps)
            return True
        history.update({k:None for k in new_positions})
        positions = new_positions


#inputs = aoc.examples(2024, 18)[0]  # correct answer: 2
#grid_max = 6
#known_possible_bytes = 12
inputs = aoc.get_input(2024, 18)
grid_max = 70
known_possible_bytes = 1024

left = known_possible_bytes
right = len(inputs)+1
while left+1 < right:
    try_bytes = left + (right - left)//2
    print(f'range: {left} - {right}, trying {try_bytes} bytes:',end=' ')
    if try_maze(inputs, grid_max, try_bytes):
        print('ok')
        left = try_bytes
    else:
        print('fail')
        right = try_bytes

print(f'first breaking byte: {inputs[left]}')

# submit answer
aoc.submit(2024, 18, 2, inputs[left])

# push to git
# aoc.push_git(2024, 18)