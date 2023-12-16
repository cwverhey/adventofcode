#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(15)

input = ['HASH']
input = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')

input = get_input(15, raw=True).strip().split(',')

hashsum = 0
for i in input:
    hash = 0
    for char in [*i]:
        hash += ord(char)
        hash *= 17
        hash %= 256
    hashsum += hash

submit(15, 1, hashsum)

#
# part 2
#
get_task(15)

input = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')

input = get_input(15, raw=True).strip().split(',')

def hash_str(str):
    hash = 0
    for char in [*str]:
        hash += ord(char)
        hash *= 17
        hash %= 256
    return hash

assert sys.version_info >= (3, 6) # require ordered dictionaries
boxes = defaultdict(lambda: {})
for i in input:
    if '=' in i:
        label = i[:-2]
        box = hash_str(label)
        lens_strength = int(i[-1])
        boxes[box][label] = lens_strength
    else:
        label = i[:-1]
        box = hash_str(label)
        try:
            _= boxes[box].pop(label)
        except KeyError:
            pass

focusing_sum = 0
for box_number, contents in boxes.items():
    for i,val in enumerate(contents.values()):
        focusing_sum += (box_number+1) * (i+1) * val

submit(15, 2, focusing_sum) # 268497