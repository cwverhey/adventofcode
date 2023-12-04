#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(4)

input = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.split('\n')

input = get_input(4, lines=True)

starttime = time.time()

points = 0
for line in input:
    parts = re.search(': (.*) \| (.*)', line).groups()
    win = [ int(x) for x in parts[0].split(' ') if x != '' ]
    have = [ int(x) for x in parts[1].split(' ') if x != '' ]
    havewin = len( list( set(win) & set(have) ) )
    if havewin:
        points += 2**(havewin-1)

print(f"answer: '{points}' in {round((time.time()-starttime)*1000)} ms")

submit(4, 1, points)


#
# part 2, attempt 1 (successful, but slow: 17 sec)
#
get_task(4)

input = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.split('\n')

input = get_input(4, lines=True)

starttime = time.time()

# get no. of matches per card
matches = [] # eg [4, 2, 2, 1, 0, 0]
for line in input:
    parts = re.search(': (.*) \| (.*)', line).groups()
    win = [ int(x) for x in parts[0].split(' ') if x != '' ]
    have = [ int(x) for x in parts[1].split(' ') if x != '' ]
    havewin = len( list( set(win) & set(have) ) )
    matches.append(havewin)

# start with list of bought scratchcards (all indices reduced by one)
scratchcards = list(range(len(matches))) # eg [0, 1, 2, 3, 4, 5]

# check list of cards from start to end, adding newly won cards to the end
idx = 0
while idx < len(scratchcards):
    cardnum = scratchcards[idx] # eg 0
    for wonidx in range(matches[cardnum]): # eg range(4)
        wonnum = cardnum + 1 + wonidx # eg 1
        if wonnum < len(matches):
            scratchcards.append(wonnum)
    idx += 1

print(f"answer: '{idx}' in {round((time.time()-starttime)*1000)} ms")

submit(4, 2, idx) # 10425665


#
# part 2, attempt 2 (less dumb, fast: 14 ms)
#
get_task(4)

input = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''.split('\n')

input = get_input(4, lines=True)

starttime = time.time()

# get number of cards for each card ID
cards = [1] * len(input)
for i,line in enumerate(input):
    parts = re.search(': (.*) \| (.*)', line).groups()
    winning = [ int(x) for x in parts[0].split(' ') if x != '' ]
    have = [ int(x) for x in parts[1].split(' ') if x != '' ]
    won = len( list( set(winning) & set(have) ) )
    
    prizes = list(range(i+1, i+won+1))
    for p in prizes:
        if p < len(input):
            cards[p] += cards[i]

# sum
cardsum = sum(cards)

print(f"answer: '{idx}' in {round((time.time()-starttime)*1000)} ms")