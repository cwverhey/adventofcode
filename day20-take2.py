#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 20

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(20, 2021)
task['example'] = [''.join(task['example'][:7])] + task['example'][7:]

task['example']
task['real']


import numpy as np
from matplotlib import pyplot as plt
from functools import reduce


def parse_task(task):
    
    t_in = task.copy()
    
    algo = np.array([1 if x == '#' else 0 for x in t_in.pop(0)], dtype='int8')
    t_in.pop(0)
    
    bitmap = []
    while t_in:
        bitmap.append([1 if x == '#' else 0 for x in t_in.pop(0)])
    bitmap = np.array(bitmap, dtype='int8')
    
    return(algo,bitmap)
# algo, bitmap = parse_task(task['example'])
# algo, bitmap = parse_task(task['real'])


def print_bitmap(bitmap):
    plt.imshow(bitmap, cmap='gray')
    plt.show()
# print_bitmap(bitmap)


def binlist2int(l):
    return reduce(lambda a, b: (a<<1) + int(b), l)
# binlist2int([1,0,1,0,1])


def apply_algo(x, algo):
    return (algo[x])
# apply_algo([123,456,12,46])


def run_algo3(algo, bitmap, verbose=True):
    
    stack = bitmap[0:-2,0:-2]*256 + bitmap[0:-2,1:-1]*128 + bitmap[0:-2,2:]*64 + bitmap[1:-1,0:-2]*32 + bitmap[1:-1,1:-1]*16 + bitmap[1:-1,2:]*8 + bitmap[2:,0:-2]*4 + bitmap[2:,1:-1]*2 + bitmap[2:,2:]
    
    bitmap = apply_algo((stack), algo)
    if verbose: print_bitmap(bitmap)

    return bitmap
# bitmap = run_algo3(algo, bitmap)


def task20a(task, verbose=True):
    
    algo, bitmap = parse_task(task)
    
    bitmap = np.pad(bitmap, 4)
    for i in range(2):
        bitmap = run_algo3(algo, bitmap, verbose)
        
    answer = sum(bitmap.flatten())
    
    print('answer 20a:',answer)


def task20b(task, verbose=True):
    
    algo, bitmap = parse_task(task)
    
    for i in range(25):
        bitmap = np.pad(bitmap, 4)
        for i2 in range(2):
            bitmap = run_algo3(algo, bitmap, verbose)
            
    answer = sum(bitmap.flatten())
    
    print('answer 20b:',answer)


# get answers
task20a(task['example'], verbose=False) # 35
task20a(task['real'], verbose=False) # 5819


task20b(task['example'], verbose=False) # 3351
task20b(task['real'], verbose=False) # 18516


# benchmark
benchmark("task20a(task['real'], verbose=False)", 200)
benchmark("task20b(task['real'], verbose=False)", 50)
