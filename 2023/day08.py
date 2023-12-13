#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(8)

input = '''RL\n
AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''.split('\n')

input = '''LLR\n
AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''.split('\n')

input = get_input(8, lines=True)

# parse input
network = {}
while i := input.pop():
    if i == '': break
    nodes = re.findall('\w{3}', i)
    network[ nodes[0] ] = ( nodes[1], nodes[2] )

LRmap = [0 if x == 'L' else 1 for x in [*input.pop()]]

# traverse the network
node = 'AAA' # current node
instruction = 0 # next LRmap instruction
stepcount = 0
while node != 'ZZZ':
    node = network[node][ LRmap[instruction] ]
    instruction = (instruction + 1) % len(LRmap)
    stepcount += 1
    # print(stepcount, node, instruction)

submit(8, 1, stepcount)


#
# part 2
#
get_task(8)

input = '''LR\n
11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''.split('\n')

input = get_input(8, lines=True)

# parse input
network = {}
while i := input.pop():
    if i == '': break
    nodes = re.findall('\w{3}', i)
    network[ nodes[0] ] = ( nodes[1], nodes[2] )

LRmap = [0 if x == 'L' else 1 for x in [*input.pop()]]

# initial nodes
nodes = [ {'node':x, 'first_z_stepcount': -1, 'z_distance': -1} for x in network.keys() if x.endswith('A') ] # current nodes
    # [ {'node': 'CBA', 'first_z_stepcount': -1, 'z_distance': -1}, = current node, stepcount on first **Z encounter, stepcounts to the next time **Z is encountered
    #   ... ]

# find first Z-node and distance to the next, for each starting node
for i,n in enumerate(nodes):

    # initial situation
    node = n['node']
    instruction = 0 # next LRmap instruction
    stepcount = 0
    first_z_node = ''
    print(stepcount, node, instruction)

    while True:
        # advance 1 step
        node = network[node][ LRmap[instruction] ]
        instruction = (instruction + 1) % len(LRmap)
        stepcount += 1
        # register if **Z node
        if node.endswith('Z'):
            print(stepcount, node, instruction)
            if first_z_node == '':
                # found first Z
                nodes[i]['first_z_stepcount'] = stepcount
                first_z_node = node
            else:
                # found second occurrence of a Z
                assert(first_z_node == node)
                nodes[i]['z_distance'] = stepcount - nodes[i]['first_z_stepcount']
                assert(nodes[i]['z_distance'] == nodes[i]['first_z_stepcount']) # unexpectedly, all **Z nodes seem to lead directly back to their corresponding **A node
                print()
                break

for n in nodes:
    print(n)

# find least common multiple
step = lcm(*[n['z_distance'] for n in nodes])

submit(8, 2, step) # 14631604759649