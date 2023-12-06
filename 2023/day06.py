#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(6)

input = get_input(6, lines=True)

times = [ int(x) for x in re.findall('\d+', input[0]) ]
distances = [ int(x) for x in re.findall('\d+', input[1]) ]
races = list( zip(times, distances) )

ways_to_win_all = []
for race in races:
    ways_to_win = 0
    for holdtime in range(1, race[0]):
        distance = holdtime * (race[0]-holdtime)
        print(distance, distance > race[1])
        if distance > race[1]:
            ways_to_win += 1
    ways_to_win_all.append( ways_to_win )
    print()

answer = np.prod(ways_to_win_all)

submit(6, 1, answer)

#
# part 2
#
get_task(6)

input = get_input(6, lines=True)

starttime = time.time()

duration = int( ''.join( re.findall('\d', input[0]) ) )
record_distance = int( ''.join( re.findall('\d', input[1]) ) )

def is_win(holdtime):
    return holdtime * (duration-holdtime) > record_distance

limit = [ round(duration/2), round(duration/2) ]
assert( is_win(limit[0]) )

# find lower limit
stepsize = round( duration/100 )
while True:
    if is_win(limit[0] - stepsize):
        limit[0] -= stepsize
        #print(f'lower limit set to {limit[0]}')
    elif stepsize > 1:
        stepsize = round(stepsize / 10)
        if stepsize < 1:
            stepsize = 1
        #print(f'stepsize set to {stepsize}')
    else:
        #print(f'lower limit found at {limit[0]}')
        break

# find upper limit
stepsize = round( duration/100 )
while True:
    if is_win(limit[1] + stepsize):
        limit[1] += stepsize
        #print(f'upper limit set to {limit[1]}')
    elif stepsize > 1:
        stepsize = round(stepsize / 10)
        if stepsize < 1:
            stepsize = 1
        #print(f'stepsize set to {stepsize}')
    else:
        #print(f'upper limit found at {limit[1]}')
        break

ways_to_win = limit[1] - limit[0] + 1

endtime = time.time()
print('ways to win: {} (took {:.2f}ms)'.format(ways_to_win, (endtime-starttime)*1000))

submit(6, 2, ways_to_win)