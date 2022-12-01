#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 10: Syntax Scoring

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(10, 2021, example=1)
task['example']
task['real']


import statistics


opener = {')':'(',']':'[','}':'{','>':'<'}
points = {')':3,']':57,'}':1197,'>':25137}


def check_line(line):
    
    stack = []
    
    for c in line:
        
        # put opening bracket on the stack
        if c in opener.values():
            stack.append(c)
            
        # pull closing bracket from the stack
        else:
            if not stack or stack.pop() != opener[c]:
                return({'score': points[c], 'stack': stack})
            
    return({'score': 0, 'stack': stack})
    

def task10a(task):
    
    answer = sum([check_line(l)['score'] for l in task])
    print('answer 10a:',answer)

#task10a(task['example']) # 26397
task10a(task['real']) # 318081


def task10b(task):
        
    points_b = {'(':1,'[':2,'{':3,'<':4}
    
    scores = []
    for l in task:
        
        check = check_line(l)
        
        # check if line is correct
        if check['score'] != 0: continue
        
        score = 0
        for c in reversed(check['stack']):
            score *= 5
            score += points_b[c]
        scores.append(score)
    
    answer = statistics.median(scores)
    print('answer 10b:',answer)

#task10b(task['example']) # 288957
task10b(task['real']) # 4361305341


# benchmark
benchmark("task10a(task['real'])", 1000)
benchmark("task10b(task['real'])", 1000)
