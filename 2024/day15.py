#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 15, 1)

#inputs = aoc.examples(2024, 15, lines=True)[1]  # correct answer: 2028
#inputs = aoc.examples(2024, 15, lines=True)[0]  # correct answer: 10092
inputs = aoc.get_input(2024, 15, lines=True)

def view():
    '''Info print'''
    icons = {'#':'⬛️', 'O':'📦', '@':'🤖', '.':'⬜️'}
    for y in range(map_size[1]):
        for x in range(map_size[0]):
            try:
                val = icons[ map[(x,y)] ]
            except KeyError:
                val = icons['.']
            print(val, end='')
        print()

def add(tuple1, tuple2):
    '''Pairwise tuple addition'''
    return tuple([x + y for x, y in zip(tuple1, tuple2)])

def move(pos, dir):
    '''Attempt to move the item from position `pos` in direction `dir`. Return the element's new position.'''
    next_pos = add(pos, dir)
    #print(f'trying {pos} -> {next_pos}')
    try:
        if map[next_pos] == '#' or move(next_pos, dir) == next_pos:
            #print(f'{pos} -> {next_pos} fail')
            return pos
    except KeyError:
        pass

    #print(f'{pos} -> {next_pos} ok')
    map[next_pos] = map.pop(pos)
    return next_pos

def score():
    return sum([ k[0]+100*k[1] for k,v in map.items() if v == 'O' ])

map = {}
for y,row in enumerate([list(i) for i in inputs[ : inputs.index('') ] ]):
    for x,cell in enumerate(row):
        if cell in ['#','O','@']:
            map[(x,y)] = cell
map_size = (x+1,y+1)
robot_start = [k for k,v in map.items() if v == '@'][0]

dirs = {'^':(0,-1), '>':(1,0), 'v':(0,1), '<':(-1,0)}  # (x = column, y = row)
moves = [ dirs[move] for i in inputs[ inputs.index('') : ] for move in list(i) ]

pos = robot_start
view()
for i,m in enumerate(moves):
    print(f'{i+1}/{len(moves)}')
    pos = move(pos, m)
view()

# submit answer
aoc.submit(2024, 15, 1, score())


#
# part 2
#

aoc.task(2024, 15, 2)

# The 'map' becomes a list of objects (wall, block, robot). Each object is a list(value, list(*coordinates)).
# Now we have to check if the entire tree can be moved before we actually do it, instead of just recursing over a simple row and begin moving as soon as the deepest item is checked.

#inputs = aoc.examples(2024, 15, lines=True)[6]  # correct answer: unknown
#inputs = aoc.examples(2024, 15, lines=True)[0]  # correct answer: 9021
inputs = aoc.get_input(2024, 15, lines=True)

def get_map(pos):
    '''Return the map index + object on a given position. Eg: get_map((5,6)) -> [24, '#', [(4, 6), (5, 6)]]'''
    try:
        return [ [i, *m] for i, m in enumerate(map) if pos in m[1]][0]
    except IndexError:
        return None

def view():
    '''Info print'''
    icons = {'#':'⬛️', 'O':'📦', '@':'🤖', '.':'⬜️'}
    map_expand = [ [icons['.']]*map_size[0] for _ in range(map_size[1]) ]
    for obj in map:
        for pos in obj[1]:
            map_expand[pos[1]][pos[0]] = icons[ obj[0] ]
    for line in map_expand:
        print(''.join(line))
    print()

def add(*tuples):
    '''Pairwise tuple addition'''
    return tuple([sum(items) for items in zip(*tuples)])

def check_move(id, dir):
    '''Check if an object can be moved. Returns which objects would have to be moved, or False.'''
    obj = map[id] # eg ['@', [(10, 3)]]
    to_move = [id]
    obstructors = [ get_map(add(p, dir)) for p in obj[1]]
    obstructors = [ o for o in obstructors if o is not None and o[0] != id ]
    for obstructor_id, obstructor_type in set([ (o[0],o[1]) for o in obstructors ]):
        #print(f'checking {obstructor_id} {obstructor_type}')
        if obstructor_type == '#':
            return False
        moveable = check_move(obstructor_id, dir)
        if moveable is False:
            return False
        to_move.extend(moveable)
    return to_move

def do_move(ids, dir):
    for obj_id in list(set(ids)):
        for pos_id, pos in enumerate(map[obj_id][1]):
            map[obj_id][1][pos_id] = add(pos, dir)

def score():
    return sum([ o[1][0][0]+100*o[1][0][1] for o in map if o[0] == 'O' ])

dirs = {'^':(0,-1), '>':(1,0), 'v':(0,1), '<':(-1,0)}  # (x = column, y = row)
moves = [ dirs[move] for i in inputs[ inputs.index('') : ] for move in list(i) ]

map = []
for y,row in enumerate([list(i) for i in inputs[ : inputs.index('') ] ]):
    for x,cell in enumerate(row):
        if cell in '#O':
            map.append([ cell, [(x*2, y), (x*2+1, y)] ])
        if cell == '@':
            map.append([ cell, [(x*2, y)] ])
map_size = (x*2+2,y+1)
robot_id = [i for i,o in enumerate(map) if o[0] == '@'][0]

view()
for i,m in enumerate(moves):
    if i%100 == 0:
        print(f'{i/len(moves)*100:.0f}%', end='\r')
    moveable = check_move(robot_id, m)
    if moveable:
        do_move(moveable, m)
view()

print(f'score: {score()}')

# submit answer
aoc.submit(2024, 15, 2, score())

# push to git
# aoc.push_git(2024, 15)