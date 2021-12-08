#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from collections import Counter

def get_advent(day, numeric = False, raw = False, lines=False):
    url = 'https://adventofcode.com/2021/day/{}/input'.format(day)
    headers = {'cookie': open('/Users/caspar/Progs/adventofcode/adventofcode2021-cookie.txt', 'r').read().strip()}
    result = requests.get(url, headers=headers).text
    if raw: return result
    if lines: return result.split('\n')[:-1]
    result = result.split()
    if numeric: result = [int(x) for x in result]
    return result

#
# Day 1: Sonar Sweep
#

#
# 1a
#

#input = [199,200,208,210,200,207,240,269,260,263] # example input
input = get_advent(1, numeric = True)

answer = sum([1 for i in range(1, len(input)) if input[i] > input[i-1]])
print('answer 1a:',answer)

#
# 1b
#

windowsum = [sum(input[i:i+3]) for i in range(0, len(input)-2)]

answer = sum([1 for i in range(1, len(windowsum)) if windowsum[i] > windowsum[i-1]])
print('answer 1b:',answer)

#
# Day 2: Dive!
# 

#
# 2a
#

input = get_advent(2, raw=True).strip().split('\n')

forward = 0
depth = 0

for l in input:
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

#
# 2b
#

forward = 0
depth = 0
aim = 0

for l in input:
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

#
# Day 3: Binary Diagnostic
#

#
# 3a
#

import numpy as np

#input = ['00100','11110','10110','10111','10101','01111','00111','11100','10000','11001','00010','01010']
input = get_advent(3)

nparr = np.array([[int(c) for c in l] for l in input]).T

gammaStr = ['1' if np.mean(l)>0.5 else '0' for l in nparr]
epsilonStr = ['0' if l == '1' else '1' for l in gammaStr]

gammaNum = int(''.join(gammaStr), 2)
epsilonNum = int(''.join(epsilonStr), 2)

answer = gammaNum * epsilonNum
print('answer 3a:',answer)

#
# 3b
#

# oxy
oxygen = np.array([[c for c in l] for l in input])
for i in range(0,len(oxygen[0])):
    
    column = np.transpose(oxygen)[i]
    colMean = np.mean(column.astype(int))
    mostFrequent = '1' if(colMean >= 0.5) else '0'
    
    oxygen = [x for x in oxygen if x[i] == mostFrequent]
    
    if len(oxygen) == 1: break

oxygen = int(''.join(oxygen[0]),2)

# co2
co2 = np.array([[c for c in l] for l in input])
for i in range(0,len(co2[0])):
    
    column = np.transpose(co2)[i]
    colMean = np.mean(column.astype(int))
    leastFrequent = '0' if(colMean >= 0.5) else '1'
    
    co2 = [x for x in co2 if x[i] == leastFrequent]
    
    if len(co2) == 1: break

co2 = int(''.join(co2[0]),2)

answer = oxygen * co2
print('answer 3b:',answer)

#
# Day 4: Giant Squid
#

#
# 4a
#

def get_input():

    input = get_advent(4, raw=True).split('\n')

    draws = [int(x) for x in input.pop(0).split(',')]
    input.pop(0)
    
    boards = []
    boardIdx = 0
    for i in input:
        line = np.array(i.split()).astype(int)
        
        if(len(line) == 0):
            boardIdx += 1
        elif(len(boards) == boardIdx):
            boards.append([line])
        else:
            boards[boardIdx] = np.vstack([boards[boardIdx], line])
            
    return (boards, draws)

def is_bingo(b):

    for row in b:
        if np.sum(row) == -1 * len(row):
            return True
        
    for col in b.T:
        if np.sum(col) == -1 * len(col):
            return True
        
    return False

def bingo_score(b, last_drawed):
    b[b==-1] = 0
    return np.sum(b) * last_drawed


boards, draws = get_input()

for draw in draws:
    
    winner = False
    
    for i in range(0, len(boards)):
        boards[i][boards[i]==draw] = -1
        if is_bingo(boards[i]):
            winner = True
            break
        
    if winner: break

print('answer 4a:',bingo_score(boards[i], draw))

#
# 4b
#

boards, draws = get_input()

unwon = set(range(0,len(boards)))

for draw in draws:
    
    winners = set()
    
    for i in unwon:
        boards[i][boards[i]==draw] = -1
        if is_bingo(boards[i]):
            winners.add(i)
        
    unwon = unwon - winners
    
    if len(unwon) == 0:
        last_winners = list(winners)
        break

for i in last_winners:
    print('answer 4b:',bingo_score(boards[i], draw))

#
# Day 5: Hydrothermal Venture
#

#
# 5a
#

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
    
input = get_advent(5, lines=True)

coords = []
for l in input:
    l = l.replace(' -> ', ',').split(',')
    coords.append([int(x) for x in l])

points = []
for c in coords:
    if c[0] == c[2] or c[1] == c[3]:
        points += getallpoints(c)
        
tally = Counter(points)

answer = len([t for t in tally.values() if t > 1])

print('answer 5a:',answer)

#
# 5b
#

points = []
for c in coords:
    points += getallpoints(c)
        
tally = Counter(points)

answer = len([t for t in tally.values() if t > 1])

print('answer 5b:',answer)

#
# Day 6: Lanternfish
#

#
# 6a
#

#fish = [3,4,3,1,2] # example data

input = get_advent(6)
fish = [int(x) for x in input[0].split(',')]


for d in range(1, 80+1):
    
    fish = [x - 1 for x in fish] # decrease all fish age by 1
    fish += [8]*fish.count(-1) # add new fish as 8
    fish = [6 if x == -1 else x for x in fish] # reset fish with -1 days to 6
    answer = len(fish)
    if d == 80: print('after {} days: {} fish'.format(d, answer))
    

#
# 6b
#

import numpy as np

def day6_np(raw_input):
    
    fish = [3,4,3,1,2]
    fish = [int(x) for x in input.strip().split(',')]
    
    tally = Counter(fish)
    tally = np.array([np.array(x) for x in tally.items()]).T # age / count
    
    for day in range(1, 256+1):
        
        newfish = 0
        tally[0] -= 1 # decrease all fish age by 1
        
        for x in np.where(tally[0] == -1)[0]: # find columns where age is now -1
            newfish += tally[1,x] # remember to add this many new fish
            tally[0,x] = 6 # reset fish with -1 days to 6
        if newfish:
            newfish = np.array([[8],[newfish]]) # create column for new fish
            tally = np.hstack((tally,newfish)) # add new fish to tally
            
        if day in [80,256]:
           print('after {} days: {} fish'.format(day, sum(tally[1])))
    
        
def day6_list(raw_input):
    
    fish = [3,4,3,1,2] # example
    fish = [int(x) for x in input.strip().split(',')]
    
    tally = [fish.count(x) for x in range(0,8+1)]
    
    for day in range(1, 256+1):
        new = tally[0]  # remember how many fish will give birth
    
        tally.pop(0)    # shift all tallies 1 day down
        tally[6] += new # add fish that gave birth
        tally.insert(8, new)  # add newborn fish
    
        if day in [80,256]:
           print('after {} days: {} fish'.format(day, sum(tally)))

input = get_advent(6, raw=True)
day6_np(input)
day6_list(input)

import timeit

timeit.timeit(globals=globals(), stmt='day6_np(input)', number=5)*1000
timeit.timeit(globals=globals(), stmt='day6_list(input)', number=5)*1000

#
# Day 8: Seven Segment Search
#

input_day8 = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
'''.split('\n')[:-1]

input_day8 = ['acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf']

input_day8 = get_advent(8, lines=True)

# parse and sort
input = []
for line in input_day8:
    
    line = [set(sorted(list(x))) for x in line.split(' ')]
    line = {'in': line[:10], 'out': line[-4:]}
    input.append(line)

#
# 8a
#
    
lengths = []
for line in input:
    lengths += [len(x) for x in line['out']]

answer = sum([lengths.count(x) for x in [2,4,3,7]])
print('answer 8a:', answer)

#
# 8b
#

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

answer = sum([translate(line) for line in input])
print('answer 8b:', answer)
