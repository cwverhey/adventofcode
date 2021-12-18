#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 3: Binary Diagnostic

WD = '/Users/caspar/Progs/adventofcode/'
exec(open(f'{WD}/AoC-functions.py').read())

task = getAoC(3, 2021, asInt=False)
task['example']
task['real']

import numpy as np

def task3a(task):
    
    nparr = np.array([[int(c) for c in l] for l in task]).T
    
    gammaStr = ['1' if np.mean(l)>0.5 else '0' for l in nparr]
    epsilonStr = ['0' if l == '1' else '1' for l in gammaStr]
    
    gammaNum = int(''.join(gammaStr), 2)
    epsilonNum = int(''.join(epsilonStr), 2)
    
    answer = gammaNum * epsilonNum
    print('answer 3a:',answer)

task3a(task['example']) # 198
task3a(task['real']) # 2498354


def task3b(task):
    
    # oxy
    oxygen = np.array([[c for c in l] for l in task])
    for i in range(0,len(oxygen[0])):
        
        column = np.transpose(oxygen)[i]
        colMean = np.mean(column.astype(int))
        mostFrequent = '1' if(colMean >= 0.5) else '0'
        
        oxygen = [x for x in oxygen if x[i] == mostFrequent]
        
        if len(oxygen) == 1: break
    
    oxygen = int(''.join(oxygen[0]),2)
    
    # co2
    co2 = np.array([[c for c in l] for l in task])
    for i in range(0,len(co2[0])):
        
        column = np.transpose(co2)[i]
        colMean = np.mean(column.astype(int))
        leastFrequent = '0' if(colMean >= 0.5) else '1'
        
        co2 = [x for x in co2 if x[i] == leastFrequent]
        
        if len(co2) == 1: break
    
    co2 = int(''.join(co2[0]),2)
    
    answer = oxygen * co2
    
    print('answer 3b:',answer)

task3b(task['example']) # 230
task3b(task['real']) # 3277956


# benchmark
benchmark("task3a(task['real'])", 100)
benchmark("task3b(task['real'])", 100)
