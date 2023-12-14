#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(12)

input = '''???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1'''.split('\n')

input = get_input(12, lines=True)

# parse input
rows = []
for i in input:
    i = i.split(' ')
    rows.append({'springs':i[0], 'groups':[int(x) for x in i[1].split(',')]})

# per row: get all options, check which result in valid groups, count them
arrangement_count = 0
for row in rows:
    springs = list(row['springs'])
    groups = row['groups']
    # print(''.join(springs), groups)

    unknown_damaged_count = sum(groups) - springs.count('#') # number of # that we need to add
    unknown_idxs = [i for i,c in enumerate(springs) if c == '?'] # indices where a # can be added
    for combo in combinations(unknown_idxs, unknown_damaged_count):
        arrangement = springs.copy()
        for i in combo:
            arrangement[i] = '#'
        arrangement_groups = [ g.span(0)[1] - g.span(0)[0] for g in re.finditer('#+', ''.join(arrangement)) ]
        #print(''.join(arrangement).replace('?','.'), arrangement_groups, arrangement_groups == groups)
        if arrangement_groups == groups:
            arrangement_count += 1

    #print()

submit(12, 1, arrangement_count)

#
# part 2
#

get_task(12)