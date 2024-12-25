#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 24, 1)

#inputs = aoc.examples(2024, 24, lines=True)[0]  # correct answer: 4
inputs = aoc.get_input(2024, 24, lines=True)  # 59336987801432

gates = {}
for i in inputs[ : inputs.index('') ]:
    g, v = i.split(': ')
    gates[g] = bool(int(v))

cmds = [cmd.split(' ') for cmd in inputs[ inputs.index('')+1 : ] ]
while cmds:
    for i,cmd in reversed(tuple(enumerate(cmds))):
        if cmd[0] in gates and cmd[2] in gates:
            cmds.pop(i)
            if cmd[1] == 'OR':
                gates[ cmd[4] ] = gates[ cmd[0] ] or gates[ cmd[2] ]
            elif cmd[1] == 'XOR':
                gates[ cmd[4] ] = gates[ cmd[0] ] ^ gates[ cmd[2] ]
            elif cmd[1] == 'AND':
                gates[ cmd[4] ] = gates[ cmd[0] ] and gates[ cmd[2] ]

answer = 0
for z in sorted([g for g in gates if g.startswith('z')], reverse=True):
    answer = answer*2 + gates[z]

# submit answer
aoc.submit(2024, 24, 1, answer)


#
# part 2
#

aoc.task(2024, 24, 2)

inputs = aoc.get_input(2024, 24, lines=True)

# split commands
# eg: cmds = [ ['rdf', 'XOR', 'nck', '->', 'z21'], ['y12', 'AND', 'x12', '->', 'stn'], ...]
cmds = [cmd.split(' ') for cmd in inputs[ inputs.index('')+1 : ] ]

# define nodes as either two inputs and logic operator, or as the XOR (SUM) or AND (CARRY) of two inputs
# eg: nodes = {'z21': [{'nck', 'rdf'}, 'XOR'], 'stn': 'CARRY_input_12', ...}
nodes = {}
for c in cmds:
    if c[0][0] in 'xy' and c[2][0] in 'xy' and c[0][0] != c[2][0] and int(c[0][1:]) == int(c[2][1:]) and c[1] == 'XOR':
        nodes[ c[4] ] = f'SUM_input_{int(c[0][1:])}'
    elif c[0][0] in 'xy' and c[2][0] in 'xy' and c[0][0] != c[2][0] and int(c[0][1:]) == int(c[2][1:]) and c[1] == 'AND':
        nodes[ c[4] ] = f'CARRY_input_{int(c[0][1:])}'
    else:
        nodes[ c[4] ] = [set([c[0],c[2]]), c[1]]

# get number of z-nodes
len_z = len([n for n in nodes if n.startswith('z')])

# proper input for a given Z
# eg: digit(3) == ['SUM_input_3', 'XOR', ['CARRY_input2', 'OR', ['SUM_input_2', 'AND', ['CARRY_input1', 'OR', ['SUM_input_1', 'AND', 'CARRY_input_0']]]]]
def digit(index, len_z):
    if index == 0:
        return 'SUM_input_0'
    elif index == len_z-1:
        return carry(index-1)
    else:
        return [f'SUM_input_{index}', 'XOR', carry(index-1)]

def carry(index):
    if index == 0:
        return 'CARRY_input_0'
    else:
        return [f'CARRY_input_{index}', 'OR', [f'SUM_input_{index}', 'AND', carry(index-1)]]

# check if actual value corresponds with proper input
def verify(tag, correct):
    fuckups = set()
    values = nodes[tag]
    if type(values) == str or type(correct) == str:
        if values != correct:
            print(f'{tag} has the wrong value: {values} instead of {correct}')
            fuckups.update([tag])
    elif values[1] != correct[1]:
        print(f'{tag} receives the wrong operation: {values[1]} instead of {correct[1]}')
        fuckups.update([tag])
    else:
        subnodes = sorted(values[0], key=lambda x: (type(nodes[x]).__name__, nodes[x]), reverse=True)
        fuckups.update(verify(subnodes[0], correct[0]))
        fuckups.update(verify(subnodes[1], correct[2]))
    return fuckups

fuckups = { fuckup for i in range(len_z) for fuckup in verify(f'z{i:02}', digit(i, len_z)) }
answer = ','.join(sorted(list(fuckups)))

# submit answer
aoc.submit(2024, 24, 2, answer)  # ctg,dmh,dvq,rpb,rpv,z11,z31,z38

# push to git
# aoc.push_git(2024, 24)