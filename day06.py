#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 6

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(6, 2021)
task['example']
task['real']


def task2fish(task):
    return [int(x) for x in task[0].split(',')]


def task6a(task):
    
    fish = task2fish(task)
    
    for d in range(1, 80+1):
        
        fish = [x - 1 for x in fish] # decrease all fish age by 1
        fish += [8]*fish.count(-1) # add new fish as 8
        fish = [6 if x == -1 else x for x in fish] # reset fish with -1 days to 6
    
    answer = len(fish)
    print('answer 6a:',answer)

task6a(task['example']) # 5934
task6a(task['real']) # 359344


def task6b(task):
    
    fish = task2fish(task)
    
    tally = [fish.count(x) for x in range(0,8+1)]
    
    for day in range(1, 256+1):
        new = tally[0]  # remember how many fish will give birth
    
        tally.pop(0)    # shift all tallies 1 day down
        tally[6] += new # add fish that gave birth
        tally.insert(8, new)  # add newborn fish
    
    print('answer 6b:',sum(tally))

task6b(task['example']) # 26984457539
task6b(task['real']) # 1629570219571


# benchmark
benchmark("task6a(task['real'])", 10)
benchmark("task6b(task['real'])", 1000)
