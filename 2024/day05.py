#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname('__file__')); import aoc

#
# part 1
#

aoc.task(2024, 5, 1)

# inputs = aoc.examples(2024, 5, lines=True)[0]  # correct answer: 143
inputs = aoc.get_input(2024, 5, lines=True)

orders = [ [int(x) for x in o.split('|')] for o in inputs[:inputs.index('')] ]
pagess = [ [int(x) for x in p.split(',')] for p in inputs[inputs.index('')+1:] ]

def sort_pages(pages, order):

    order = [o for o in order if o[0] in pages and o[1] in pages]
    print(pages, order)
    result = []

    for page in pages:
        left = 0
        right = len(result)
        #print(result, page, left, right)
        for o in order:
            if page == o[0] and o[1] in result:
                #print(f'{page} is before {o[1]}')
                right = min(right, result.index(o[1]))
                #print(f'right: {right}')
            elif page == o[1] and o[0] in result:
                #print(f'{page} is after {o[0]}')
                left = max(left, result.index(o[0])+1)
                #print(f'left: {left}')
        if left == right:
            result = result[:left] + [page] + result[left:]
            print(result)
        else:
            print('Failed to find a position for {page}')
            return False
        
    return result

cum_middle = 0
for pages in pagess:
    sorted = sort_pages(pages, orders)
    if sorted == pages:
        print('same!')
        cum_middle += pages[ int((len(pages)-1)/2) ]
    else:
        print('different!')


aoc.submit(2024, 5, 1, cum_middle)

#
# part 2
#

aoc.task(2024, 5, 2)

#inputs = aoc.examples(2024, 5, lines=True)[0]  # correct answer: 123
inputs = aoc.get_input(2024, 5, lines=True)

orders = [ [int(x) for x in o.split('|')] for o in inputs[:inputs.index('')] ]
pagess = [ [int(x) for x in p.split(',')] for p in inputs[inputs.index('')+1:] ]

cum_middle = 0
for pages in pagess:
    sorted = sort_pages(pages, orders)
    if sorted == pages:
        print('same!')
    else:
        print('different!')
        cum_middle += sorted[ int((len(sorted)-1)/2) ]

aoc.submit(2024, 5, 2, cum_middle)

aoc.push_git(2024, 5)