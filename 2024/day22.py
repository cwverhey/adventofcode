#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 22, 1)

def mix_prune(value, secret):
    return (secret ^ value) % 16777216

def evolve(secret):
    secret = mix_prune(secret, secret * 64)
    secret = mix_prune(secret, secret // 32)
    secret = mix_prune(secret, secret * 2048)
    return secret


#inputs = aoc.examples(2024, 22)[1]  # correct answer: 37327623
inputs = aoc.get_input(2024, 22)  # 13234715490

inputs = [int(i) for i in inputs]

cum_2000 = 0
for i in inputs:
    for _ in range(2000):
        i = evolve(i)
    cum_2000 += i

# submit answer
aoc.submit(2024, 22, 1, cum_2000)


#
# part 2
#

aoc.task(2024, 22, 2)

from collections import defaultdict

def mix_prune(value, secret):
    return (secret ^ value) % 16777216

def evolve(secret):
    secret = mix_prune(secret, secret * 64)
    secret = mix_prune(secret, secret // 32)
    secret = mix_prune(secret, secret * 2048)
    return secret

def sequence_prices(secret):
    '''
    possible sequences and resulting sales price, for a single secret
    @output: {(-1, -1, 0, 2): 6, (6, -1, -1, 0): 4, (-3, 6, -1, -1): 4}
    '''
    # price per iteration
    prices = [secret%10]
    for _ in range(2000):
        secret = evolve(secret)
        prices.append(secret%10)

    # price difference per iteration (offset 1)
    diff = []
    for i in range(1, len(prices)):
        diff.append(prices[i]-prices[i-1])

    # price for each first occurrence of a diff-sequence
    sequences = {}
    for i in range(len(diff)-1, 2, -1):
        sequences[ tuple(diff[i-3:i+1]) ] = prices[i+1]
    return sequences


#inputs = aoc.examples(2024, 22)[5]  # correct answer: 23
inputs = aoc.get_input(2024, 22)  # 1490

# get total number of bananas for each sequence
bananas = defaultdict(lambda:0)
for secret in [int(i) for i in inputs]:
    for sequence,price in sequence_prices(secret).items():
        bananas[sequence] += price

# get outcome of best sequence
answer = max(bananas.values())

# submit answer
aoc.submit(2024, 22, 2, answer)

# push to git
# aoc.push_git(2024, 22)