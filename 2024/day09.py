#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 9, 1)

#inputs = aoc.examples(2024, 9)[0]  # correct answer: 1928
inputs = aoc.get_input(2024, 9)

# load filesystem: list of fileID per block
file = True
id = 0
fs = []
for blocks in list(inputs[0]):
    if file:
        fs.extend([id]*int(blocks))
        id += 1
    else:
        fs.extend([None]*int(blocks))
    file = not file

# compact data
left = 0
right = len(fs)-1
while True:
    while not fs[left] is None:
        left += 1
    while fs[right] is None:
        right -= 1
    if left >= right:
        break
    fs[left] = fs[right]
    right -= 1
fs = fs[:right+1]

# calculate checksum
checksum = sum([i*val for i,val in enumerate(fs)])

# submit answer
aoc.submit(2024, 9, 1, checksum)


#
# part 2
#

aoc.task(2024, 9, 2)

#inputs = aoc.examples(2024, 9)[0]  # correct answer: 2858
inputs = aoc.get_input(2024, 9)

# load filesystem: list of list [file length, fileID / None]
file = True
id = 0
fs = []
for blocks in [int(x) for x in list(inputs[0])]:
    if file:
        if blocks > 0:
            fs.append([int(blocks), id])
        id += 1
    else:
        if blocks > 0:
            fs.append([int(blocks), None])
    file = not file

# defragment
right = len(fs)

while True:

    left = 0
    right -= 1

    # find next file to move
    while fs[right][1] is None and right > 0:
        right -= 1

    if right == 0:
        # tried to move all files
        break

    # find next suitable opening
    while (not fs[left][1] is None or fs[left][0] < fs[right][0]) and left < right:
        left += 1

    if left == right:
        # exhausted all empty openings
        continue

    # move file to left
    space_remaining = fs[left][0] - fs[right][0]
    fs[left] = fs[right].copy()
    fs[right][1] = None
    if space_remaining:
        fs.insert(left+1, [space_remaining, None])
        right += 1

# calculate checksum
checksum = 0
pos = 0
for file in fs:
    if not file[1] is None:
        checksum += file[1] * (pos*2 + file[0] - 1) * file[0] // 2
    pos += file[0]

# submit answer
aoc.submit(2024, 9, 2, checksum)

# push to git
aoc.push_git(2024, 9)