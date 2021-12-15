#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from collections import Counter
import json
from datetime import datetime
from datetime import date
import statistics
import numpy as np

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

import timeit
timeit.timeit(globals=globals(), stmt='sum([translate(line) for line in input])', number=10)

#
# Day 10: Syntax Scoring
#

input_day10 = '''
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''

input_day10 = get_advent(10,raw=True)

lines = input_day10.strip().split('\n')

#
# 10a
#

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
    
answer = sum([check_line(l)['score'] for l in lines])
print('answer 10a:', answer)

#
# 10b
#

points_b = {'(':1,'[':2,'{':3,'<':4}

scores = []
for l in lines:
    
    check = check_line(l)
    
    # check if line is correct
    if check['score'] != 0: continue
    
    score = 0
    for c in reversed(check['stack']):
        print(c)
        score *= 5
        score += points_b[c]
    print()
    scores.append(score)

answer = statistics.median(scores)
print('answer 10b:', answer)

#
# Day 12: Passage Pathing
#

# get input by line
input_day12 = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end
'''.split('\n')[:-1]

input_day12 = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
'''.split('\n')[:-1]

input_day12 = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
'''.split('\n')[:-1]

input_day12 = get_advent(12, lines=True)

# get set of cave names, eg {'start', 'end', 'A'}
caves = set([c for line in input_day12 for c in line.split('-')])

# get list of cave connections per cave, eg {'start':['A'], 'A':['start','end'], 'end':['A']}
connections = {c:[] for c in caves}
for line in input_day12:
    c = line.split('-')
    if(c[1] != 'start'): connections[c[0]].append(c[1])
    if(c[0] != 'start'): connections[c[1]].append(c[0])

# 12a

def complete_routesA(route):
    
    if(route[-1] == 'end'):
        
        # we found a complete route
        print(route)
        
        # return path
        return([route])
        
    else:
        
        # store successful paths
        paths = []

        # get list of all possible next caves
        next_ = [c for c in connections[route[-1]] if c.isupper() or c not in route]
    
        # enter, then exit every next cave (backtracking)
        for n in next_:
            paths += complete_routesA(route+[n])
            
        # return successful paths
        return(paths)

routes = complete_routesA(['start'])
print('answer 12a:', len(routes))

# 12b

def complete_routesB(route):
    
    if(route[-1] == 'end'):
        
        # we found a complete route
        # print(route)
        
        # return path
        return([route])
        
    else:
        
        # successful paths
        paths = []

        # get list of all possible next caves
        # first, check if we already visisted a small cave twice
        tally = Counter([c for c in route if c.islower()]).values()
        if(len(tally) == 0 or max(tally) > 1):
            
            # already visisted a small cave twice
            next_ = [c for c in connections[route[-1]] if c.isupper() or c not in route]

        else:
            
            # not yet visited a small cave twice
            next_ = connections[route[-1]]

        # enter, then exit every next cave (backtracking)
        for n in next_:
            paths += complete_routesB(route+[n])
            
        # return successful paths
        return(paths)

routes = complete_routesB(['start'])
print('answer 12b:', len(routes))

import timeit
timeit.timeit(globals=globals(), stmt='print(len(complete_routesB(["start"])))', number=10)

#
# Day 14: Extended Polymerization
#

input_day14 = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''.strip().split('\n')

input_day14 = get_advent(14, lines=True)

# process input into `template` and `rules`
input = input_day14.copy()
template = input.pop(0)
input.pop(0)
rules = {x[0]:x[0][0]+x[1]+x[0][1] for x in [x.split(' -> ') for x in input]}

#
# 14a
#

# take one iteration of inserting values between all pairs
def insert_step(in_):
    out = ''
    for i in range(len(in_)-1):
        #print('pair:',in_[i:i+2])
        out += rules[in_[i:i+2]][:-1]
    out += in_[i+1]
    return out

# take 10 steps
polymer = template
for i in range(10):
    polymer = insert_step(polymer)
    #print(polymer)
    
len(polymer)

# tally
tally = Counter(polymer)

# print answer
answer = max(tally.values())-min(tally.values())
print('answer 14a:', answer)

#
# 14b
#

# sum values of 2 dicts: {'A':12, 'B':5} + {'C':3, 'A':6} = {'A':18, 'B':5, 'C':3 }
def sum_dicts(x, y):
    return {k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)}

# get a tally for the entire tree under a given string, up to a given depth
# requires `rules` to contain all pair insertion rules
def get_tally(template, rules, goal_depth, verbose = True):
    
    # function to calc tally of (tree under) (sub)pattern (recurses)
    def get_subpattern_tally(pattern, goal_depth, curr_depth, verbose):
        
        nonlocal tally_cache
    
        if verbose: print('\t'*curr_depth, pattern, sep='')
    
        # return tally of pattern if we're deep enough, except last letter: it will be counted with next subpattern
        if(goal_depth == curr_depth): return Counter(pattern[:-1])
    
        # init new subtally
        tallies = {}
        
        # add tallies from all subpairs
        for i in range(len(pattern)-1):
            
            subpattern = rules[ pattern[i:i+2] ]
            
            try:
                subtally = tally_cache[curr_depth][subpattern]
                
            except KeyError:
                subtally = get_subpattern_tally(subpattern, goal_depth, curr_depth+1, verbose)
                tally_cache[curr_depth][subpattern] = subtally
                
            if verbose: print('\t'*(curr_depth+1),subtally, sep='')
            tallies = sum_dicts(tallies, subtally)
        
        # return subtally
        return tallies
    
    # init cache for solved tallies (avoids recursing into subpatterns we've done before)
    tally_cache = {i:{} for i in range(goal_depth+1)}
    
    # get tallies recursively
    tallies = get_subpattern_tally(template, goal_depth, 0, verbose)
    
    # add last character from template to tally (to avoid double counting, the last letter of subpatterns isn't counted)
    tallies = sum_dicts(tallies, {template[-1]:1})
    
    # return final tally
    return tallies


# run cached recursive tally function and get answer
tally = get_tally(template, rules, 40, verbose=False)
answer = max(tally.values())-min(tally.values())
print('answer 14b:', answer)

# time
def time():
    tally = get_tally(template, rules, 40, verbose=False)
    answer = max(tally.values())-min(tally.values())
    print('answer 14b:', answer)
    
import timeit
timeit.timeit(globals=globals(), stmt='time()', number=10)


#
# 14b, take 2 (after seeing Apie's solution)
#

def get_tally(input_lines, depth, verbosity=0):
        
    # load template and rules
    # ex. template: 'NNCB'
    # ex. rules2D: {'NS': ['NP', 'PS'], 'KV': ['KB', 'BV']}
    input = input_lines.copy()
    template = input.pop(0)
    input.pop(0)
    rules2D = {x[0]:[x[0][0]+x[1], x[1]+x[0][1]] for x in [x.split(' -> ') for x in input]}
    if verbosity > 0: print(f'polymer template: {template}\n')
    if verbosity > 1: print(f'pair insertion rules: {rules2D}\n')

    # tally how often each pair occurs
    pair_tally = Counter([template[i:i+2] for i in range(len(template)-1)])
    if verbosity > 1: print(f'initial pair_tally: {pair_tally}\n')
    
    # loop, to expand each pair into two new pairs
    for n in range(1,depth+1):
        new_pair_tally = Counter()
        for pair,count in pair_tally.items():
            if verbosity > 2: print("{0} * {1} = {0} * {2} + {0} * {3}".format(count, pair, rules2D[pair][0], rules2D[pair][1] ))
            new_pair_tally[rules2D[pair][0]] += count
            new_pair_tally[rules2D[pair][1]] += count
        pair_tally = new_pair_tally
        if verbosity > 1: print(f'pair_tally after {n} iterations: {new_pair_tally}\n')

    # count how often each letter occurs as the first item in a pair + last letter in pattern
    letter_tally = Counter({template[-1:]:1})
    for pair,count in pair_tally.items():
        letter_tally[pair[0]] += count
    if verbosity > 0: print(f'letter_tally: {letter_tally}\n')

    # calculate answer
    answer = max(letter_tally.values()) - min(letter_tally.values())
    if verbosity > -1: print(f'answer 14b: {answer}')

    # return
    return letter_tally

input_day14 = get_advent(14, lines=True)
get_tally(input_day14, 40)

import timeit
timeit.timeit(globals=globals(), stmt='get_tally_skinny(input_day14, 40)', number=1000)

#
# 14b, take 2b (speeding things up a tiny bit more)
#

def get_tally_skinny(input_lines, depth):
    input = input_lines.copy()
    template = input.pop(0)
    input.pop(0)
    rules2D = {x[0]:[x[0][0]+x[1], x[1]+x[0][1]] for x in [x.split(' -> ') for x in input]}
    pair_tally = Counter([template[i:i+2] for i in range(len(template)-1)])
    for n in range(1,depth+1):
        new_pair_tally = Counter()
        for pair,count in pair_tally.items():
            new_pair_tally[rules2D[pair][0]] += count
            new_pair_tally[rules2D[pair][1]] += count
        pair_tally = new_pair_tally
    letter_tally = Counter({template[-1:]:1})
    for pair,count in pair_tally.items():
        letter_tally[pair[0]] += count
    return max(letter_tally.values()) - min(letter_tally.values())

input_day14 = get_advent(14, lines=True)
get_tally_skinny(input_day14, 40)

import timeit
timeit.timeit(globals=globals(), stmt='get_tally_skinny(input_day14, 40)', number=1000)

