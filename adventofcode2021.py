#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import statistics
import numpy as np
from collections import Counter

def get_advent(day, numeric = False, raw = False, lines=False):
    url = 'https://adventofcode.com/2021/day/{}/input'.format(day)
    headers = {'cookie': open('/Users/caspar/.config/adventofcode2021-cookie.txt', 'r').read().strip()}
    result = requests.get(url, headers=headers).text
    if raw: return result
    if lines: return result.split('\n')[:-1]
    result = result.split()
    if numeric: result = [int(x) for x in result]
    return result

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

#
# Day 15: Chiton
#

import heapq

input_day15 = get_advent(15, lines=True)

def get_safest_path(input):
    
    # load input: map of risk per position
    risks = np.array([np.array([int(n) for n in line]) for line in input])
    risks = np.concatenate((risks, risks+1, risks+2, risks+3, risks+4), axis=1)
    risks = np.concatenate((risks, risks+1, risks+2, risks+3, risks+4), axis=0)
    risks = np.where(risks > 9, risks - 9, risks)
    
    # store optimal risk per cell
    opt_riskpath = np.full_like(risks, -1)
    
    # task heap queue of cells to expand
    tasks = []
    
    # add cell to task queue and set its risk in opt_riskpath
    def add_lowest_risk(previous_risk, x, y):
        if x < 0 or y < 0: return
        try:
            if opt_riskpath[x,y] == -1:
                lowest_risk = previous_risk + risks[x,y]
                opt_riskpath[x,y] = lowest_risk
                heapq.heappush(tasks, (lowest_risk,x,y))
        except:
            pass
        
    # setup for start
    opt_riskpath[0,0] = 0
    heapq.heappush(tasks, (0,0,0)) # risk: 0, x: 0, y: 0
    
    # run queue until final cell reached
    while opt_riskpath[-1,-1] == -1:
        risk,x,y = heapq.heappop(tasks)
        add_lowest_risk(risk, x-1, y)
        add_lowest_risk(risk, x+1, y)
        add_lowest_risk(risk, x, y-1)
        add_lowest_risk(risk, x, y+1)
    
    print('answer 15b:',opt_riskpath[-1,-1])

get_safest_path(input_day15)

import timeit
timeit.timeit(globals=globals(), stmt='get_safest_path(input_day15)', number=10)

#
# Day 16: Packet Decoder
#

def binlist2int(binlist):
    retval = 0
    for e in binlist:
        retval = (retval << 1) | e
    return retval

# input: list of ints eg [0,1,1,1,0,1,1,0], or string of hexadecimals eg "DE4DB33F" (if hexstr is set)
# full_ret: return full list of parameters instead of just the result
# verbosity: 0/1/2
# hexstr: input is string of hex values
def get_packet(input, full_ret=False, verbosity=0, hexstr=True):
    
    if hexstr:
        input = [int(c) for l in input for c in "{0:04b}".format(int(l,16))]
        
    def poptop(num):
        nonlocal input
        retval = input[:num]
        input = input[num:]
        return retval
    
    # packet header
    v = binlist2int(poptop(3))
    v_cum = v
    t = binlist2int(poptop(3)) # 4 = literal value, not 4: operator
    
    # packet body
    if t == 4:
        
        # literal value
        
        last_group = [1]
        number = []
        while last_group == [1]:
            last_group = poptop(1)
            number += poptop(4)
        value = binlist2int(number)
        value_type = 'literal'
        result = value
        
    else:
        
        # operator
        
        results = [] # container for numbers to operate on  
        
        if poptop(1) == [0]:
            # next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet
            total_length_of_subpackets = binlist2int(poptop(15))
            value = poptop(total_length_of_subpackets) # get subpackets
            value_type = 'subpackets_by_length'
            
            sub_input = value
            while len(sub_input) > 7:
                result = get_packet(sub_input, True, verbosity, False)
                results.append(result['result'])
                v_cum += result['v_cum']
                sub_input = result['remaining_input']
            
        else:
            # next 11 bits are a number that represents the number of sub-packets immediately contained by this packet
            value = binlist2int(poptop(11))
            value_type = 'subpackets_by_number'
            
            for i in range(value):
                result = get_packet(input, True, verbosity, False)
                results.append(result['result'])
                v_cum += result['v_cum']
                input = result['remaining_input']
                
        # perform operation
        operations = ['sum(r)', 'np.prod(r)', 'min(r)', 'max(r)', '(ノಠ益ಠ)ノ彡┻━┻', 'int(r[0] > r[1])', 'int(r[0] < r[1])', 'int(r[0] == r[1])']
        r = results
        result = eval(operations[t])
        
    retval = {'v':v, 'v_cum':v_cum, 't':t, 'type':value_type, 'value':value, 'remaining_input': input, 'result': result}
    
    if verbosity == 1: print({k:v for k,v in retval.items() if not (k == 'remaining_input' or (k == 'value' and t != 4))})
    if verbosity > 1: print(retval)
    
    if full_ret: return retval
    else: return retval['result']
        
# test inputs
get_packet('D2FE28', full_ret=True)
get_packet('38006F45291200')
get_packet('EE00D40C823060')
get_packet('8A004A801A8002F478')
get_packet('620080001611562C8802118E34')
get_packet('C0015000016115A2E0802F182340')
get_packet('A0016C880162017C3686B18A3D4780')

get_packet('C200B40A82') # 3
get_packet('04005AC33890') # 54
get_packet('880086C3E88112') # 7
get_packet('CE00C43D881120') # 9
get_packet('D8005AC2A8F0') # 1  
get_packet('F600BC2D8F', verbosity = 1) # 0
get_packet('9C005AC2F8F0', verbosity = 2) # 0
get_packet('9C0141080250320F1802104A08') # 1

# real input
input_day16 = get_advent(16)[0]
answer = get_packet(input_day16, full_ret=True)
print('answer 16a:',answer['v_cum'])
print('answer 16b:',answer['result'])

# time it
import timeit
timeit.timeit(globals=globals(), stmt='get_packet(input_day16)', number=1000)
