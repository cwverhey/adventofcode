#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 18: Snailfish

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(18, 2021, example='all')
task['example']
task['real']

import math

#
# snail math functions
#

# string to list and vice versa
def s2l(string):
    return [int(x) if x.isnumeric() else x for x in re.findall('(\[|\d+|,|\])', string)]

def l2s(parsed):
    return ''.join([str(x) for x in parsed])

s2l('[[1,2],[3,4]]') # ['[', '[', 1, ',', 2, ']', ',', '[', 3, ',', 4, ']', ']']
l2s(['[', '[', 1, ',', 2, ']', ',', '[', 3, ',', 4, ']', ']']) # '[[1,2],[3,4]]'

# explode
def try_explode(parsed, verbose=True):

    depth = 0
    exploded = False
    for i,v in enumerate(parsed):
        
        if depth == 5:
            
            exploded = True
            if verbose: print('explode!\nbefore:',l2s(parsed))
            
            exploder = parsed[i-1:i+4]
            pre = parsed[:i-1]
            post = parsed[i+4:]
            
            for i1, v1 in reversed(list(enumerate(pre))):
                if isinstance(v1,int):
                    pre[i1] += exploder[1]
                    break
            
            for i1, v1 in enumerate(post):
                if isinstance(v1,int):
                    post[i1] += exploder[3]
                    break
                
            parsed = pre + [0] + post
            if verbose: print('after :',l2s(parsed))
            break
        
        if v == '[': depth += 1
        elif v == ']': depth -= 1

    return(exploded, parsed)

try_explode(s2l('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')) # [[3,[2,[8,0]]],[9,[5,[7,0]]]]


# split
def try_split(parsed, verbose=True):
    
    split = False
    for i,v in enumerate(parsed):
        if isinstance(v, int) and v >= 10:
            
            split = True
            if verbose: print('split!\nbefore:',l2s(parsed))
            
            splitter = ['[', math.floor(v/2), ',', math.ceil(v/2), ']']
            
            parsed = parsed[:i] + splitter + parsed[i+1:]
            if verbose: print('after: ',l2s(parsed))
            break
        
    return(split, parsed)
    
try_split(s2l('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')) # [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]


# reduce
def reduce(parsed, verbose=True):
    cont = True
    while cont:
        cont, parsed = try_explode(parsed, verbose)
        
        if not cont:
            cont, parsed = try_split(parsed, verbose)
            
    if verbose: print('reduced: ',l2s(parsed))
            
    return parsed

reduce(s2l('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]')) # [[[[0,7],4],[[7,8],[6,0]]],[8,1]]


# single addition
def add(l1, l2, verbose=True):
    return reduce(['['] + l1 + [','] + l2 + [']'], verbose)

add(s2l('[[[[4,3],4],4],[7,[[8,4],9]]]'),s2l('[1,1]')) # [[[[0,7],4],[[7,8],[6,0]]],[8,1]]


# multiple ,iterative addition
def add_strings(stringlist, verbose=True):
    parsed = add(s2l(stringlist[0]),s2l(stringlist[1]), verbose)
    for i in range(2, len(stringlist)):
        parsed = add(parsed,s2l(stringlist[i]), verbose)
    return parsed

add_strings(task['example'][4]) # [[[[5,0],[7,4]],[5,5]],[6,6]]
l2s(add_strings(task['example'][5], verbose=False)) # [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]


# teacher's magnitude calculation
def get_magnitude(string):
    
    cont = True
    while(cont):
        r = re.findall('\[(\d+),(\d+)\]', string)
        for a, b in r:
            sumAB = 3*int(a) + 2*int(b)
            string = string.replace(f'[{a},{b}]', str(sumAB))
        if r == []: cont = False
            
    return int(string)

get_magnitude('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]') # 3488


# complete snail math assignment
def task18a(tasklist):
    
    parsed = add_strings(tasklist, verbose=False)
    string = l2s(parsed)
    answer = get_magnitude(string)
    
    print('answer 18a:', answer)

task18a(task['example'][7]) # 4140
task18a(task['real']) # 4235


# find biggest possible combo
def task18b(tasklist):

    maxval = 0
    for i1, t1 in enumerate(tasklist):
        for i2, t2 in enumerate(tasklist):
            if i1 != i2:
                val = get_magnitude(l2s(add(s2l(t1), s2l(t2), verbose=False)))
                if val > maxval: maxval = val
    print('answer 18b:',maxval)

task18b(task['example'][7]) # 3993
task18b(task['real']) # 4659

# benchmark
benchmark("task18a(task['real'])", 10)
benchmark("task18b(task['real'])", 4)
