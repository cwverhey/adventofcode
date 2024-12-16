#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 16, 1)

# assumption: the best path always has the least possible amount of turns
# assumption: you can only go east, north or south from the start

#inputs = aoc.examples(2024, 16)[0]  # correct answer: 7036
#inputs = aoc.examples(2024, 16)[2]  # correct answer: 11048
inputs = aoc.get_input(2024, 16)

import numpy as np

def view(visited = []):
    theme = {'#':'⬛️', '.':'⬜️', 'S':'📍', 'E':'⛳️', 'X':'🦌'}
    view_map = map.copy()
    for pos in visited:
        view_map[*pos] = 'X'
    for line in view_map:
        print(''.join([ theme[x] for x in line ]))

def run(points, verbose=False):

    dirs = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}

    while True:

        # fully extend points in current direction
        new_points = []
        for point in points:
            #print(point)
            new_pos = point[0]
            new_cost = point[2]
            while not map[ *new_pos ] in ['#','E']:
                if not new_pos.tolist() in visited:
                    visited.append(new_pos.tolist())
                    new_points.append([ new_pos, point[1], new_cost ])
                new_pos = new_pos + dirs[ point[1] ]
                new_cost += 1
            if map[ *new_pos ] == 'E':
                if verbose:
                    view(visited)
                return new_cost
            
        # sort by cost
        points = sorted(new_points, key=lambda x: x[2])

        # turn both ways
        new_points = []
        for point in points:
            for new_dir in ['N','S'] if point[1] in ['W','E'] else ['W','E']:
                if map[ *point[0]+dirs[new_dir] ] != '#':
                    new_points.append([ point[0], new_dir, point[2]+1000 ])
        points = new_points

        if verbose:
            view(visited)
            input('Continue? ')

# go
map = np.array([list(l) for l in inputs])
start = np.argwhere(map == 'S')[0]
view()
points = [ [ start.copy(), 'E', 0 ] ]
visited = []
best_score = run(points, False)

# submit answer
aoc.submit(2024, 16, 1, best_score)


#
# part 2
#

aoc.task(2024, 16, 2)

# now we need to record the past path for all points, and get *all* possible shortest paths by (1) still inserting a new point if it's been visited for the same cost and (2) keep extending all points in their current direction after we found the first one

#inputs = aoc.examples(2024, 16)[0]  # correct answer: 45
#inputs = aoc.examples(2024, 16)[2]  # correct answer: 64
inputs = aoc.get_input(2024, 16)

import numpy as np

def view(visited = []):
    theme = {'#':'⬛️', '.':'⬜️', 'S':'📍', 'E':'⛳️', 'X':'🦌'}
    view_map = map.copy()
    for pos in visited:
        view_map[*pos] = 'X'
    for line in view_map:
        print(''.join([ theme[x] for x in line ]))

def run(points, verbose=False):

    dirs = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}

    while True:

        # fully extend points in current direction
        new_points = []
        for point in points:
            #print(point)
            new_pos = point[0]
            new_cost = point[2]
            new_path = point[3].copy()
            while not map[ *new_pos ] in ['#']:
                hash = tuple(new_pos.tolist())
                if not hash in visited or visited[hash] == new_cost:
                    new_points.append([ new_pos, point[1], new_cost, new_path.copy() ])
                    visited[hash] = new_cost
                new_pos = new_pos + dirs[ point[1] ]
                new_cost += 1
                new_path.append( new_pos.tolist() )
    
        # sort by cost
        points = sorted(new_points, key=lambda x: x[2])

        # return winning paths
        finishers = [ p for p in points if np.array_equal(p[0], target) ]
        if finishers:
            best_score = min([ f[2] for f in finishers ])
            winners = [ f for f in finishers if f[2] == best_score ]
            tracks = list(set([ tuple(pos) for w in winners for pos in w[3] ]))
            return (best_score, winners, tracks)

        # turn both ways
        new_points = []
        for point in points:
            for new_dir in ['N','S'] if point[1] in ['W','E'] else ['W','E']:
                if map[ *point[0]+dirs[new_dir] ] != '#':
                    new_points.append([ point[0], new_dir, point[2]+1000, point[3].copy() ])
        points = new_points

        if verbose:
            view(visited)
            input('Continue? ')

# go
map = np.array([list(l) for l in inputs])
start = np.argwhere(map == 'S')[0]
target = np.argwhere(map == 'E')[0]
view()
points = [ [ start.copy(), 'E', 0, [start.tolist()] ] ]  # pos(x,y), direction, cost, path[]
visited = {}
_, _, tracks = run(points)

# submit answer
aoc.submit(2024, 16, 2, len(tracks))

# push to git
# aoc.push_git(2024, 16)