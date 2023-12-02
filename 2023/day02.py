#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(2)

# which games would have been possible if the bag had been loaded with 
# only 12 red cubes, 13 green cubes, and 14 blue cubes. _What is the sum of the
# IDs of those games?_
input = get_input(2, lines=True)

id_sum = 0

for i in input:
    max_shown = {'red':0, 'green': 0, 'blue': 0}
    parts = i.split(':')

    reveals = re.findall('(\d+) (\w+)', parts[1])
    for r in reveals:
        max_shown[ r[1] ] = max( int(r[0]), max_shown[ r[1] ] )

    if max_shown['red'] <= 12 and max_shown['green'] <= 13 and max_shown['blue'] <= 14:
        id = int( re.search('\d+', parts[0]).group() )
        id_sum += id

submit(2, 1, id_sum)


#
# part 2
#
get_task(2)

id_power = 0

for i in input:
    max_shown = {'red':0, 'green': 0, 'blue': 0}
    parts = i.split(':')

    reveals = re.findall('(\d+) (\w+)', parts[1])
    for r in reveals:
        max_shown[ r[1] ] = max( int(r[0]), max_shown[ r[1] ] )

    id_power += max_shown['red'] * max_shown['green'] * max_shown['blue']

submit(2, 2, id_power)