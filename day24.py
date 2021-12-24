#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 24: Arithmetic Logic Unit

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

tasks = getAoC(24, 2021, example='all')


import re
import numpy as np
import pandas as pd


def parse_task(task):

    parsed = []
    for instruction in task:
        r = re.match('(.{3}) (\w)\s?(.*)?',instruction)
        r = list(r.groups())
        if not r[2].islower() and r[2] != '': r[2] = int(r[2])
        parsed.append(r)
    return parsed
# parse_task(tasks['example'][1])


def multiverseALU(instructions, aggregate=False, verbose=False):


    mem = pd.DataFrame([[0,0,0,0,0]], columns=['w','x','y','z','serial'])


    for index,ins in enumerate(instructions):


        # get current values for cmd, a and b
        cmd = ins[0] # command, eg: 'inp'
        a = ins[1]   # column for a, eg: 'z'

        if ins[2] in ['w','x','y','z']:
            b = mem[ins[2]] # b column of values from memory
        else:
            b = ins[2] # b single raw value


        # operations
        if cmd == 'inp':

            # simplify
            if aggregate:
                mem = mem.groupby(['w','x','y','z'],as_index=False).agg({'serial':aggregate})

            newvalue = [1,2,3,4,5,6,7,8,9]
            memlen = len(mem)
            mem = pd.concat([mem]*9)
            mem[a] = np.repeat(newvalue, memlen)
            mem['serial'] = mem['serial'] * 10 + mem[a]

            # simplify
            if aggregate:
                mem = mem.groupby(['w','x','y','z'],as_index=False).agg({'serial':aggregate})

        elif cmd == 'mul':
            mem[a] *= b

        elif cmd == 'add':
            mem[a] += b

        elif cmd == 'mod':
            mem[a] %= b

        elif cmd == 'div':
            mem[a] //= b

        elif cmd == 'eql':
            mem[a] = (mem[a] == b) * 1

        else:
            raise SystemExit('ERROR unknown command: [{}] in instruction line {}'.format(' '.join([str(x) for x in ins]), index))


        # output
        if verbose:
            print('**{}** {}\n'.format(index, ' '.join([str(x) for x in ins])))
            print(mem)
            print()


    return mem


def task24a(task, verbose=False):

    task = parse_task(task)

    results = multiverseALU(task, aggregate='max', verbose=verbose)

    outcomes = results.serial[results.z.eq(0)]
    answer = max(outcomes)

    print('answer 24a:',answer)

# task24a(tasks['real'], verbose=True)  # 59692994994998


def task24b(task, verbose=False):

    task = parse_task(task)

    results = multiverseALU(task, aggregate='min', verbose=verbose)

    outcomes = results.serial[results.z.eq(0)]
    answer = min(outcomes)

    print('answer 24b:', answer)

# task24b(tasks['real'], verbose=True)  # 16181111641521


# benchmark
benchmark("task24a(tasks['real'])", 1)
benchmark("task24b(tasks['real'])", 1)
