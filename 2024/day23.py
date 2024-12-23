#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 23, 1)

from collections import defaultdict

#inputs = aoc.examples(2024, 23)[0]  # correct answer: 7
inputs = aoc.get_input(2024, 23)  # 1163

connections_list = [c.split('-') for c in inputs]
connections_set = [set(c) for c in connections_list]

t_clusters = defaultdict(lambda:[])
for c in connections_list:
    if c[0][0] == 't':
        t_clusters[ c[0] ].append(c[1])
    if c[1][0] == 't':
        t_clusters[ c[1] ].append(c[0])

teams = []
for leader, members in t_clusters.items():
    for i in range(len(members)):
        for j in range(i+1, len(members)):
            if set([members[i],members[j]]) in connections_set:
                team = set([leader, members[i], members[j]])
                if not team in teams:
                    teams.append(team)

# submit answer
aoc.submit(2024, 23, 1, len(teams) )


#
# part 2
#

aoc.task(2024, 23, 2)


def fits_in_team(computer, team):
    for member in team:
        if set([computer, member]) not in connections_set:
            return False
    return True

def expand_team(team, candidates):
    global max_team
    candidates = [c for c in candidates if fits_in_team(c, team) ]
    if len(candidates) == 0:
        if len(team) > len(max_team):
            max_team = team
            print('found a longer team:', team)
    elif len(team) + len(candidates) > len(max_team):
        while candidates:
            recruit = candidates.pop()
            expand_team([*team, recruit], candidates)


#inputs = aoc.examples(2024, 23)[0]  # correct answer: co,de,ka,ta
inputs = aoc.get_input(2024, 23)  # bm,bo,ee,fo,gt,hv,jv,kd,md,mu,nm,wx,xh

connections_set = [set(c.split('-')) for c in inputs]
computers = list(set([com for c in connections_set for com in c]))

start_len = len(computers)
max_team = []
while computers:
    print(f'{start_len-len(computers)+1}/{start_len}', end='\r')
    recruit = computers.pop()
    expand_team([recruit], computers)

password = ','.join(sorted(max_team))

# submit answer
aoc.submit(2024, 23, 2, password)

# push to git
# aoc.push_git(2024, 23)