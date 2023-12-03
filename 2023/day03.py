#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(3)

input = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''.split('\n')

input = get_input(3)

numbers = []
for row,i in enumerate(input):
    matches = re.finditer('\d+', i)
    for m in matches:
        numbers.append({'row': row, 'col': m.span(), 'number': int(m.group())})

mat = np.chararray((len(input),len(input[0])))
for row,i in enumerate(input):
    for col,c in enumerate(i):
        mat[row, col] = c

partno_sum = 0
for n in numbers:
    rows = range( max(0, n['row']-1),    min(len(input),   n['row']+2) )
    cols = range( max(0, n['col'][0]-1), min(len(input[0]), n['col'][1]+1) )
    adjacent = mat[rows][:,cols]
    for c in np.ravel(adjacent):
        if (c < b'0' or c > b'9') and c != b'.':
            partno_sum += n['number']
            break

submit(3, 1, partno_sum)

#
# part 2
#
get_task(3)

input = '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..'''.split('\n')

input = get_input(3)

numbers = []
for row,i in enumerate(input):
    matches = re.finditer('\d+', i)
    for m in matches:
        numbers.append({'row': row, 'col': m.span(), 'number': int(m.group())})

mat = np.chararray((len(input),len(input[0])))
for row,i in enumerate(input):
    for col,c in enumerate(i):
        mat[row, col] = c

asterisks = defaultdict(lambda: [])
for n in numbers:
    rows = range( max(0, n['row']-1),    min(len(input),   n['row']+2) )
    cols = range( max(0, n['col'][0]-1), min(len(input[0]), n['col'][1]+1) )
    for r in rows:
        for c in cols:
            if mat[r,c] == b'*':
                coord = f'{r}:{c}'
                asterisks[coord].append(n['number'])

gearratio_sum = 0
for a in asterisks.values():
    if len(a) == 2:
        gearratio_sum += np.prod(a)

submit(3, 2, gearratio_sum)