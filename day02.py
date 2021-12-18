#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 2: Dive!

WD = '/Users/caspar/Progs/adventofcode/'
exec(open(f'{WD}/AoC-functions.py').read())

task = getAoC(2, 2021)
task['example']
task['real']

def task2a(task):
    
    forward = 0
    depth = 0
    
    for l in task:
        i = l.split(' ')
        n = int(i[1])
        if i[0] == 'forward':
            forward += n
        elif i[0] == 'up':
            depth -= n
        else:
            depth += n
            
    answer = forward * depth
    print('answer 2a:',answer)

task2a(task['example']) # 150
task2a(task['real']) # 1728414


def task2b(task):

    forward = 0
    depth = 0
    aim = 0
    
    for l in task:
        i = l.split(' ')
        n = int(i[1])
        if i[0] == 'forward':
            forward += n
            depth += aim * n
        elif i[0] == 'up':
            aim -= n
        else:
            aim += n
            
    answer = forward * depth
    print('answer 2b:',answer)

task2b(task['example']) # 900
task2b(task['real']) # 1765720035


# benchmark
benchmark("task2a(task['real'])", 1000)
benchmark("task2b(task['real'])", 1000)
