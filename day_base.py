#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day @

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(@, 2021)
task['example']
task['real']


def task@a(task, verbose=False):

    print('answer @a:',answer)
#task@a(task['example'], verbose=True)  #
#task@a(task['real'], verbose=True)  #


def task@b(task, verbose=False):

    print('answer @b:', answer)
# task@b(task['example'], verbose=True)
# task@b(task['real'], verbose=True)

# benchmark
benchmark("task@a(task['real'])", 100)
benchmark("task@b(task['real'])", 100)
