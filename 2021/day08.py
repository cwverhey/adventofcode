#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 8

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(8, 2021, example='all')

examples = [[],[]]
while(len(task['example'][1])):
    line = task['example'][1].pop(0) +' '+ task['example'][1].pop(0)
    examples[0].append(line)
while(len(task['example'][2])):
    line = task['example'][2].pop(0) +' '+ task['example'][2].pop(0)
    examples[1].append(line)
task['example'] = examples

task['example']
task['real']


def task_parse(task):
        
    # parse and sort
    parsed = []
    for line in task:
        
        line = [set(sorted(list(x))) for x in line.split(' ')]
        line = {'in': line[:10], 'out': line[-4:]}
        parsed.append(line)
        
    return parsed

#task_parse(task['example'][1])


def task8a(task):

    parsed = task_parse(task)    
    
    lengths = []
    for line in parsed:
        lengths += [len(x) for x in line['out']]
    
    answer = sum([lengths.count(x) for x in [2,4,3,7]])
    print('answer 8a:',answer)

#task8a(task['example'][1]) # 26
task8a(task['real']) # 303


def translate(line):

    # bin inputs by length
    #
    # 2 digits: 1
    # 3 digits: 7
    # 4 digits: 4
    # 5 digits: 2 3 5  
    # 6 digits: 0 6 9
    # 7 digits: 8
    #
    bins = {}
    for i in range(2,8): bins[i] = []
    for l in line['in']:
        bins[len(l)].append(l)
    
    # find true segments per number
    true = {}
    true[1] = bins[2][0]
    true[4] = bins[4][0]
    true[7] = bins[3][0]
    true[8] = bins[7][0]
    
    true[3] = [x for x in bins[5] if len(true[7] - x) == 0][0] # find 3: 7 - 3 = 0 segments, unique in bin
    bins[5] = [x for x in bins[5] if x != true[3]] # remove 3 from bin 5
    
    true[9] = true[3].union(true[4]) # find 9: 3 + 4 = 9
    bins[6] = [x for x in bins[6] if x != true[9]]
    
    true[5] = [x for x in bins[5] if len(x - true[9]) == 0][0] # find 5: 5 - 9 = 0 segments
    bins[5] = [x for x in bins[5] if x != true[5]]
    
    true[2] = bins[5][0] # find 2: only set left in bin[5]
    
    true[0] = [x for x in bins[6] if len(true[7] - x) == 0][0] # find 0: 7 - 0 = 0 segments
    bins[6] = [x for x in bins[6] if x != true[0]]
    
    true[6] = bins[6][0]  # find 6: only set left in bin[6]
    
    # create fast translate dict
    translate = {}
    for i in range(0,10):
        translate[''.join(sorted(true[i]))] = i
    
    #print(translate)
    
    sum = 0
    for l in line['out']:
        val = translate[''.join(sorted(l))]
        sum = sum*10+val
        
    return(sum)


def task8b(task):
    
    answer = sum([translate(line) for line in task_parse(task)])
    print('answer 8b:',answer)

#task8b(task['example'][1]) # 61229
task8b(task['real']) # 961734


# benchmark
benchmark("task8a(task['real'])", 100)
benchmark("task8b(task['real'])", 200)
