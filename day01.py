#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 1: Sonar Sweep

WD = '/Users/caspar/Progs/adventofcode/'
exec(open(f'{WD}/AoC-functions.py').read())

task = getAoC(1, 2021)
task['example']
task['real']

def task1a(tasklist):
    answer = sum([1 for i in range(1, len(tasklist)) if tasklist[i] > tasklist[i-1]])
    print('answer 1a:',answer)

task1a(task['example']) # 7
task1a(task['real']) # 1154


def task1b(tasklist):
    windowsum = [sum(tasklist[i:i+3]) for i in range(0, len(tasklist)-2)]
    answer = sum([1 for i in range(1, len(windowsum)) if windowsum[i] > windowsum[i-1]])
    print('answer 1b:',answer)

task1b(task['example']) # 5
task1b(task['real']) # 1127


# benchmark
benchmark("task1a(task['real'])", 1000)
benchmark("task1b(task['real'])", 1000)
