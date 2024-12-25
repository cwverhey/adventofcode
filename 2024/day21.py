#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

aoc.task(2024, 21)

#inputs = aoc.examples(2024, 21)[3]  # correct answer at 2 robots on directional keypads: 126384
inputs = aoc.get_input(2024, 21)  # 163086 at 2, 198466286401228 at 25


from functools import cache

# assumption: the best path to a key is always one from those with the shortest paths
# assumption: the best path has the least variation of directions (eg > > ^ is better than > ^ >)
# assumption: at the end of every command line, all robots end back on A

numpad = ('789','456','123','X0A')
dirpad = ('X^A','<v>')
directions = {'^':(0,-1), '>':(1,0), 'v':(0,1), '<':(-1,0)}
moves = [{True:'>',False:'<'},{True:'v',False:'^'}]

def coordinate(keypad, value):
    '''(x,y)'''
    for y,row in enumerate(keypad):
        if value in row:
            return (row.index(value),y)

def add(pos1, pos2):
    '''(x,y)+(x,y)'''
    return (pos1[0]+pos2[0], pos1[1]+pos2[1])

def subtract(pos1, pos2):
    '''(x,y)-(x,y)'''
    return (pos1[0]-pos2[0], pos1[1]-pos2[1])

def path_values(keypad, startpos, path):
    '''keypad values from a certain start position along a sequence of keypresses'''
    pos = startpos
    poss = [ keypad[ pos[1] ][ pos[0] ] ]
    for p in path:
        pos = add(pos,directions[p])
        poss.append(keypad[ pos[1] ][ pos[0] ])
    return poss

@cache
def keypress_options(keypad, startval, endval):
    '''options for keypresses to get from value a to b'''
    startpos = coordinate(keypad, startval)
    endpos = coordinate(keypad, endval)
    diff = subtract(endpos, startpos)
    hor = [ moves[0][ diff[0]>0 ] ] * abs(diff[0])
    ver = [ moves[1][ diff[1]>0 ] ] * abs(diff[1])
    options = []
    for option in [[*hor,*ver],[*ver,*hor]]:
        if 'X' not in path_values(keypad, startpos, option) and [*option,'A'] not in options:
            options.append([*option,'A'])
    return options

@cache
def min_code_length(code, keypad, depth):
    '''minimal amount of keypresses at top level (directional keypad that you are using), to get certain keypresses at a certain depth'''
    #print(code)
    start = 'A'
    length = 0
    for c in code:
        #print(c)
        options = [o for o in keypress_options(keypad, start, c)]
        if depth:
            length += min([ min_code_length(tuple(o), dirpad, depth-1) for o in options])
        else:
            length += min([len(o) for o in options])
        start = c
    return length

#
# part 1
#
cum_complexity = 0
for i, code in enumerate(inputs):
    print(f'{i+1}/{len(inputs)}')
    length = min_code_length(tuple(code), numpad, 2)
    print(code, length)
    code_num = int(code[:-1])
    cum_complexity += length*code_num
print(cum_complexity)

# submit answer
aoc.submit(2024, 21, 1, cum_complexity)

#
# part 2
#
cum_complexity = 0
for i, code in enumerate(inputs):
    print(f'{i+1}/{len(inputs)}')
    length = min_code_length(tuple(code), numpad, 25)
    print(code, length)
    code_num = int(code[:-1])
    cum_complexity += length*code_num
print(cum_complexity)

# submit answer
aoc.submit(2024, 21, 2, cum_complexity)

# push to git
# aoc.push_git(2024, 21)