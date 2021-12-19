#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 4: Giant Squid

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(4, 2021)
task['example']
task['real']

import numpy as np


def get_input(task):
    
    input = task.copy()

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


def task4a(task):
    
    boards, draws = get_input(task)
    
    for draw in draws:
        
        winner = False
        
        for i in range(0, len(boards)):
            boards[i][boards[i]==draw] = -1
            if is_bingo(boards[i]):
                winner = True
                break
            
        if winner: break
    
    print('answer 4a:',bingo_score(boards[i], draw))

task4a(task['example']) # 4512
task4a(task['real']) # 27027


def task4b(task):
        
    boards, draws = get_input(task)
    
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

task4b(task['example']) # 1924
task4b(task['real']) # 36975


# benchmark
benchmark("task4a(task['real'])", 25)
benchmark("task4b(task['real'])", 25)
