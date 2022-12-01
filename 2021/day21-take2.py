#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 21: Dirac Dice

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(21, 2021)
task['example']
task['real']


import itertools
from collections import Counter
import numpy as np
import pandas as pd


def parse_task(task):
    p1 = re.findall(r'Player 1 starting position: (\d+)', task[0])
    p2 = re.findall(r'Player 2 starting position: (\d+)', task[1])
    return np.array([int(p1[0])-1, int(p2[0])-1])
# parse_task(task['example'])


class DeterministicDie:

    def __init__(self):
        self.value = -1

    def rollThrice(self):
        self.value += 3
        return 3*self.value

    def getDieRolls(self):
        return self.value + 1


def task21a(task, verbose=False):

    # starting state
    position = parse_task(task)
    score = np.array([0,0])
    die = DeterministicDie()
    playersturn = 0

    while 1:
        dieroll = die.rollThrice()
        if verbose: print(f'turn {playersturn} roll {dieroll} old_pos {position} old_score {score}', end=' ')

        position[playersturn] = (position[playersturn] + dieroll) % 10
        score[playersturn] += position[playersturn] + 1
        if verbose: print(f'new_pos {position} new_score {score}')

        if max(score) >= 1000: break
        playersturn = (playersturn + 1) % 2

    losingplayer = (playersturn + 1) % 2
    loserscore = score[losingplayer]
    dierolls = die.getDieRolls()

    if verbose: print(f'after {dierolls} rolls, scores are {score}')

    answer = loserscore * dierolls
    print('answer 21a:',answer)
#task21a(task['example'], verbose=True)  # 739785
#task21a(task['real'], verbose=True)  # 906093


def quantumDieOutcomeBuilder():

    combinations = np.array(list(itertools.product(range(1,4), range(1,4), range(1,4))))
    sums = np.sum(combinations, axis=1)
    tally = Counter(sums)
    return (np.array(list(tally.keys())), np.array(list(tally.values())))
# quantumDieOutcomeBuilder()


def getAllNextStates(worlds, player, dice, verbose=True):

    if verbose:
        print(worlds)
        print()

    # repeat lists to get length: worlds * dice outcomes
    df = pd.concat([worlds] * len(dice[0]), ignore_index=True)
    die_values = np.repeat(dice[0], len(worlds))
    die_occurrences = np.repeat(dice[1], len(worlds))

    if player == 0:
        df.p0 += die_values  # move player to new position
        df.p0 = df.p0 % 10
        df.s0 += df.p0 + 1   # add position to score
    else:
        df.p1 += die_values  # move player to new position
        df.p1 = df.p1 % 10
        df.s1 += df.p1 + 1   # add position to score

    # multiply occurences
    df.freq *= die_occurrences

    # merge identical states
    df = df.groupby(['s0','s1','p0','p1'], as_index=False).agg(freq=('freq', sum))

    if verbose: print(df)

    return df


def solveQuantumDie(task, threshold=21, verbose=False):

    #quantumworlds = np.array([[0,0,0,0,1]]); threshold = 15; verbose = True
    #quantumworlds = pd.DataFrame([[0,0,0,0,1]], columns=['s0','s1','p0','p1','freq'])
    #quantumworlds = pd.DataFrame([[0,0,0,0,1],[0,1,0,1,1]], columns=['s0','s1','p0','p1','freq'])

    startposition = parse_task(task)

    dieoutcomes = quantumDieOutcomeBuilder()
    quantumworlds = pd.DataFrame([[0, 0, startposition[0], startposition[1], 1]], columns=['s0','s1','p0','p1','freq'])
    playersturn = 0
    wins = [0,0]

    while 1:

        # get all possible outcomes for all possible games
        quantumworlds = getAllNextStates(quantumworlds, playersturn, dieoutcomes, verbose)

        # get how many times this player has won, remove those games
        if playersturn == 0:
            won_universes = quantumworlds.s0 >= threshold
        else:
            won_universes = quantumworlds.s1 >= threshold

        wins[playersturn] += quantumworlds.freq[won_universes].sum()
        quantumworlds.drop(quantumworlds[won_universes].index, inplace=True)

        # check how many quantumworlds haven't finished yet
        if verbose: print('universes left:',len(quantumworlds))

        # it's next player's turn!
        playersturn = (playersturn+1) % 2

        # are we done yet?
        if len(quantumworlds) == 0: break

    return wins
#solveQuantumDie(task['example'], threshold=10, verbose=True)


def task21b(task, verbose=False):

    wins = solveQuantumDie(task, 21, verbose=verbose)
    answer = max(wins)
    print('answer 21b:', answer)

# task21b(task['example'], verbose=False)  # 444356092776315
# task21b(task['real'], verbose=False)  # 274291038026362

# benchmark
benchmark("task21a(task['real'])", 100)
benchmark("task21b(task['real'])", 10)
