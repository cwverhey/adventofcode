#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 06:11:47 2021

@author: caspar
"""

import requests

def get_advent(day, numeric = False, raw = False, lines=False):
    url = 'https://adventofcode.com/2021/day/{}/input'.format(day)
    headers = {'cookie': 'bla'}
    result = requests.get(url, headers=headers).text
    if raw: return result
    if lines: return result.split('\n')[:-1]
    result = result.split()
    if numeric: result = [int(x) for x in result]
    return result

#
# 1a
#

input = get_advent(1, numeric = True)
#input = [199,200,208,210,200,207,240,269,260,263]

answer = sum([1 for i in range(1, len(input)) if input[i] > input[i-1]])
print('answer 1a:',answer)

#
# 1b
#

windowsum = [sum(input[i:i+3]) for i in range(0, len(input)-2)]

answer = sum([1 for i in range(1, len(windowsum)) if windowsum[i] > windowsum[i-1]])
print('answer 1b:',answer)


#
# 2a
#

input = get_advent(2, raw=True).split('\n')[:-1]

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
# 3a
#

import numpy as np

input = get_advent(3)
#input = ['00100','11110','10110','10111','10101','01111','00111','11100','10000','11001','00010','01010']

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


#print('winner: {}, after draw: {}'.format(i,draw))

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

#print('last winner(s):',last_winners)

for i in last_winners:
    print('answer 4b:',bingo_score(boards[i], draw))
    
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
# 6a
#

fish = [3,4,3,1,2]

input = get_advent(6)
fish = [int(x) for x in input[0].split(',')]


for d in range(1, 256+1):
    
    fish = [x - 1 for x in fish] # decrease all fish age by 1
    fish += [8]*fish.count(-1) # add new fish as 8
    fish = [6 if x == -1 else x for x in fish] # reset fish with -1 days to 6
    answer = len(fish)
    print('after {} days: {} fish'.format(d, answer))
    

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

timeit.timeit(globals=globals(), stmt='day6_np(input)', number=5)*1000
timeit.timeit(globals=globals(), stmt='day6_list(input)', number=5)*1000
