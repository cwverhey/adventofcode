#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 5: Hydrothermal Venture

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(5, 2021)
task['example']
task['real']

from collections import Counter


def getallpoints(c):
    x_step = 1 if c[0] <= c[2] else -1
    y_step = 1 if c[1] <= c[3] else -1
    x = list(range(c[0], c[2]+x_step, x_step))
    y = list(range(c[1], c[3]+y_step, y_step))
    
    if(len(x) == 1 or len(y) == 1):
        return [(x_,y_) for x_ in x for y_ in y]
    else:
        return [(x[i],y[i]) for i in range(0,len(x))]
    

def task5a(task):
        
    coords = []
    for l in task:
        l = l.replace(' -> ', ',').split(',')
        coords.append([int(x) for x in l])
    
    points = []
    for c in coords:
        if c[0] == c[2] or c[1] == c[3]:
            points += getallpoints(c)
            
    tally = Counter(points)
    
    answer = len([t for t in tally.values() if t > 1])
    print('answer 5a:',answer)

task5a(task['example']) # 5
task5a(task['real']) # 8060


def task5b(task):
    
    coords = []
    for l in task:
        l = l.replace(' -> ', ',').split(',')
        coords.append([int(x) for x in l])
    
    points = []
    for c in coords:
        points += getallpoints(c)
            
    tally = Counter(points)
    
    answer = len([t for t in tally.values() if t > 1])
    print('answer 5b:',answer)

task5b(task['example']) # 12
task5b(task['real']) # 21577


# benchmark
benchmark("task5a(task['real'])", 100)
benchmark("task5b(task['real'])", 100)
