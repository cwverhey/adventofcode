#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(20)

class Flipflop:
    def __init__(self, name, outputs):
        self.name = name
        self.state = False
        self.outputs = outputs
    def __str__(self):
        return f"% state: {self.state}, out: {self.outputs}"
    def input(self, input_sender, input_pulse):
        if input_pulse:
            return {}
        else:
            self.state = not self.state
            return [(self.name, o, self.state) for o in self.outputs]

class Conjunction:
    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = {i:False for i in inputs}
        self.outputs = outputs
    def __str__(self):
        return "& in: {}, out: {}".format( [(k,v) for k,v in self.inputs.items()], self.outputs)
    def input(self, input_sender, input_pulse):
        self.inputs[input_sender] = input_pulse
        return [(self.name, o, not all(self.inputs.values())) for o in self.outputs]

class Broadcaster:
    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs
    def __str__(self):
        return f"B out: {self.outputs}"
    def input(self, input_sender, input_pulse):
        return [(self.name, o, input_pulse) for o in self.outputs]

input = '''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''.split('\n')

input = '''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''.split('\n')

input = get_input(20, lines=True)

module_inputs = defaultdict(lambda:[])
for i in input:
    i = i.split(' -> ')
    for out in i[1].split(', '):
        module_inputs[out].append(i[0].replace('%','').replace('&',''))

modules = {}
for i in input:
    i = i.split(' -> ')
    i[1] = i[1].split(', ')
    if i[0] == 'broadcaster':
        modules[i[0]] = Broadcaster(i[0], i[1])
    elif i[0][0] == '%':
        modules[i[0][1:]] = Flipflop(i[0][1:], i[1])
    elif i[0][0] == '&':
        modules[i[0][1:]] = Conjunction(i[0][1:], module_inputs[ i[0][1:] ], i[1])

for name,obj in modules.items():
    print(f'{name}:\n{obj}\n')

pulsecount = {True: 0, False: 0}
for x in range(1000):
    print(f'push {x}')
    queue = [('button', 'broadcaster', False)]
    while queue:
            sender, target, pulse = queue.pop(0)
            #print('{} -{}-> {}'.format(sender, 'high' if pulse else 'low', target))
            pulsecount[pulse] += 1
            if target in modules.keys():
                queue.extend( modules[target].input(sender, pulse) )

pulseproduct = np.prod(list(pulsecount.values())) # 807069600
submit(20, 1, pulseproduct)