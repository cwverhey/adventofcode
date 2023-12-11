#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(7)

input = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.split('\n')

input = get_input(7, lines=True)

LUT_typestrength = {'11111': 1, '1112': 2, '122': 3, '113': 4, '23': 5, '14': 6, '5': 7} # 1: high card, 2: 1p, 3: 2p, 4: 3oaC, 5: FH, 6: 4oaC, 7: 5oaC
LUT_cardstrength = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

# parse input line by line
hands = []
for i in input:
    i = i.split(' ')
    typestrength = LUT_typestrength[ ''.join(sorted( [ str(x) for x in Counter(i[0]).values() ])) ]
    cardstrength = [ LUT_cardstrength[x] for x in i[0] ]
    handstrength = typestrength*10**10 + sum([ s*100**x for x,s in enumerate(reversed(cardstrength)) ])
    hands.append( {'hand': i[0], 'bid': int(i[1]), 'hs': handstrength, 'ts': typestrength, 'cs': cardstrength} )

# rank hands
ranks = np.argsort( [hand['hs'] for hand in hands] ) # 0-based !!!
for i,r in enumerate(ranks):
    hands[r]['rank'] = i+1 # 1-based !!!

# debug
for i in ranks:
    hand = hands[i]
    print(i, hand['rank'], hand['hand'], hand['hs'], hand['bid'])

# total winnings
winnings = sum( [ hand['rank'] * hand['bid'] for hand in hands ] )
submit(7, 1, winnings) # 251927063 too high


#
# part 2
#
get_task(7)

input = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''.split('\n')

input = get_input(7, lines=True)

LUT_typestrength = {11111: 1, 1112: 2, 122: 3, 113: 4, 23: 5, 14: 6, 5: 7} # 1: high card, 2: 1p, 3: 2p, 4: 3oaC, 5: FH, 6: 4oaC, 7: 5oaC
LUT_cardstrength = {'J': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'Q': 11, 'K': 12, 'A': 13}

# parse input line by line
hands = []
for i in input:
    i = i.split(' ')
    jacks = i[0].count("J")
    type = ''.join(sorted( [ str(x) for x in Counter(i[0].replace('J','')).values() ]))
    if type == '': type = 0
    typestrength = LUT_typestrength[ int(type) + jacks ]
    cardstrength = [ LUT_cardstrength[x] for x in i[0] ]
    handstrength = typestrength*10**10 + sum([ s*100**x for x,s in enumerate(reversed(cardstrength)) ])
    hands.append( {'hand': i[0], 'bid': int(i[1]), 'hs': handstrength, 'ts': typestrength, 'cs': cardstrength} )

# rank hands
ranks = np.argsort( [hand['hs'] for hand in hands] ) # 0-based !!!
for i,r in enumerate(ranks):
    hands[r]['rank'] = i+1 # 1-based !!!

# debug
for i in ranks:
    hand = hands[i]
    print(i, hand['rank'], hand['hand'], hand['hs'], hand['bid'])

# total winnings
winnings = sum( [ hand['rank'] * hand['bid'] for hand in hands ] )
submit(7, 2, winnings) # 255632664