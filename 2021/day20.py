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
    
    algo = [1 if x == '#' else 0 for x in t_in.pop(0)]
    t_in.pop(0)
    
    bitmap = []
    while t_in:
        bitmap.append([1 if x == '#' else 0 for x in t_in.pop(0)])
    bitmap = np.array(bitmap, dtype='bool')
    
    return(algo,bitmap)

# algo, bitmap = parse_task(task['example'])
# algo, bitmap = parse_task(task['real'])


def print_bitmap(bitmap):
    plt.imshow(bitmap, cmap='gray')
    plt.show()

# print_bitmap(bitmap)


def binlist2int(l):
    return reduce(lambda a, b: (a<<1) + int(b), l)


def run_algo(algo, bitmap, verbose=True):
    rows,cols = bitmap.shape
    
    new_bitmap = np.empty((rows-2,cols-2), dtype='bool')
    
    r = 1
    while r < rows-1:
        c = 1
        while c < cols-1:
            
            # get 9 blocks
            block = bitmap[r-1:r+2,c-1:c+2]
            #print(block)
            base10_number = binlist2int(block.flatten())
            new_bitmap[r-1,c-1] = algo[base10_number]
            
            c += 1
            
        r += 1

    
    if verbose: print_bitmap(new_bitmap)

    return(new_bitmap)
        
# bitmap = run_algo(algo, bitmap)

def task20a(task, verbose=True):
    
    algo, bitmap = parse_task(task)
    
    bitmap = np.pad(bitmap, 4)
    for _ in range(2):
        bitmap = run_algo(algo,bitmap, verbose)
        
    answer = sum(bitmap.flatten())
    
    print('answer 20a:',answer)

task20a(task['example']) # 35
task20a(task['real']) # 5819


def task20b(task, verbose=True):
    
    algo, bitmap = parse_task(task)
    
    for _ in range(25):
        bitmap = np.pad(bitmap, 4)
        for __ in range(2):
            bitmap = run_algo(algo, bitmap, verbose)
            
    answer = sum(bitmap.flatten())
    
    print('answer 20b:',answer)

task20b(task['example'], verbose=False) # 3351
task20b(task['real'], verbose=False) # 18516


# benchmark
benchmark("task20a(task['real'], verbose=False)", 1)
benchmark("task20b(task['real'], verbose=False)", 1)
