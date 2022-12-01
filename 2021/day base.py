#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day @

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

tasks = getAoC(@, 2021)
tasks['example']
tasks['real']


def task@a(task, verbose=False):

    print('answer @a:',answer)
#task@a(tasks['example'], verbose=True)  #
#task@a(tasks['real'], verbose=True)  #


def task@b(task, verbose=False):

    print('answer @b:', answer)
# task@b(tasks['example'], verbose=True)
# task@b(tasks['real'], verbose=True)

# benchmark
benchmark("task@a(tasks['real'])", 100)
benchmark("task@b(tasks['real'])", 100)
