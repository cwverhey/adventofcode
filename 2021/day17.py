#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 17: Trick Shot

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(17, 2021)
task['example']
task['real']


import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# parse input string to list of target coordinates
def parse_task(tasklist):
    r = re.findall('^target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$', tasklist[0])
    return [int(x) for x in r[0]]

parse_task(task['example'])

# find all valid y velocities
#
# A valid initial y-velocity is within [-target_y_min .. target_y_min]
#
# A positive initial y-velocity of `n` starts upward, reaches its high point at
# y=n*(n+1)/2 and t=n, then starts descending, with the velocity becoming -n
# at y=0 and t=2*n. The remaining number of steps `t` to the first point after
# y=target_y_max can be found from y = n*(n+1)/2 - (n+t)*(n+t+1)/2:
#
#   t = 0.5 * ( math.sqrt(4*n^2 + 4*n - 8*y + 1) + 2*n - 1 )
#
# It's sufficient for positive n, to calculate the step ceil(t) to verify if it
# will reach the target and when.
#
# The valid negative n will be the inverse of the valid positive n, reaching a
# peak of 0, reaching the target 2*n steps before their positive counterpart.
#
def find_valid_initial_y_velocities(tasklist, verbose=True, get_best=False):
    
    def check_n(n):
        
        nonlocal valid_n
        
        if n > 0: peak = int(n*(n+1)/2)
        else: peak = 0
        
        target_max_reached = 1 + 0.5 * ( math.sqrt(4*n**2 + 4*n - 8*target[3] + 1) + 2*n - 1 )
        target_min_reached = 1 + 0.5 * ( math.sqrt(4*n**2 + 4*n - 8*target[2] + 1) + 2*n - 1 )
        
        if verbose: print(f'n: {n}, peak: y={peak}, target top reached t={target_max_reached:.4}, target bottom reached t={target_min_reached:.4}')
        
        for t in range(math.ceil(target_max_reached), math.floor(target_min_reached)+1):
            if get_best: return(n, peak)
            try: valid_n[t].append(n)
            except KeyError: valid_n[t] = [n]

    # get target limits
    target = parse_task(tasklist) # target = [x_min, x_max, y_min, y_max]
    
    # store valid n per t where it reaches target
    valid_n = {}
    
    # verify positive n
    for n in range(-target[2],-1,-1):
        ret = check_n(n)
        if get_best and ret: return ret

    # verify negative n
    for n in [-x-1 for x in sorted(list(set(sum(valid_n.values(),[]))))]:
        check_n(n)
            
    return valid_n

valid_n = find_valid_initial_y_velocities(task['example'])
find_valid_initial_y_velocities(task['example'], get_best=True)


def sim_y(velocity, steps=10):
    y = 0
    for t in range(steps):
        print(f't={t} y={y}')
        y += velocity
        velocity -= 1
        
sim_y(9, 30)


def sim_x(velocity, steps=10):
    x = 0
    for t in range(steps):
        print(f't={t} x={x}')
        x += velocity
        velocity -= np.sign(velocity)
        
sim_x(7)


def sim_plot(coorlist, tasklist, dim=(5,5)):
    
    target = parse_task(tasklist) # target = [x_min, x_max, y_min, y_max]
    
    def get_coords(x_v, y_v):
        x = y = 0
        coor_x = []
        coor_y = []
        
        for i in range(1000):
            coor_x.append(x)
            coor_y.append(y)
            x += x_v
            y += y_v
            x_v -= np.sign(x_v)
            y_v -= 1
            if x > target[1] or y < target[2]: break
        
        return(coor_x, coor_y)
        
    fig = plt.figure(figsize=dim)
    fig.set_dpi(100)
    ax = fig.add_subplot()
    for x_v, y_v in coorlist:
        coor_x, coor_y = get_coords(x_v, y_v)
        ax.plot(coor_x, coor_y, '-o', color='black', linewidth=.5, markersize=1, alpha=.5)
    ax.add_patch(patches.Rectangle((target[0]-.5, target[2]-.5), target[1]-target[0]+1, target[3]-target[2]+1, edgecolor='r', facecolor='none', linewidth=.75, alpha=.75, zorder=2))
    plt.show()

sim_plot([(7,2),(7,3)], task['example'])

# find all valid x velocities
#
# x_v will always be <= target_x_max, and its triangle number must at least be target_x_min
#
def find_valid_initial_x_velocities(tasklist, verbose=True):

    target = parse_task(tasklist) # target = [x_min, x_max, y_min, y_max]
    
    # verify positive x
    valid_n_temp = {} # position is only at 1 specific time
    valid_n_stay = {} # position stays after time
    for n in range(target[1],0,-1):
        
        # check triangle number
        if n*(n+1)/2 < target[0]: break
        
        # run sim
        t = 0
        x = 0
        v = n
        
        while x <= target[1] and v > 0:
            t += 1
            x += v
            v -= 1
            if verbose:print(f'n: {n}, t={t}, x={x}, velocity={v}')
            
            if target[0] <= x <= target[1]:
                if v == 0:
                    try: valid_n_stay[t].append(n)
                    except KeyError: valid_n_stay[t] = [n]
                else:
                    try: valid_n_temp[t].append(n)
                    except KeyError: valid_n_temp[t] = [n]
    
    return ({'temp': valid_n_temp, 'stay': valid_n_stay})
    
find_valid_initial_x_velocities(task['example'])


def task17a(task, verbose=False):
    vel, peak = find_valid_initial_y_velocities(task, verbose, get_best=True)
    print('answer 17a:',peak)

task17a(task['example']) # 45
task17a(task['real']) # 5151


def task17b(task, verbose=False):
    
    # find valid initial velocities
    x = find_valid_initial_x_velocities(task, verbose=False)
    y = find_valid_initial_y_velocities(task, verbose=False)

    # get valid number of steps
    x_temp_steps = set(x['temp'].keys())
    x_stay_steps = set(x['stay'].keys())
    y_steps = set(y.keys())

    # find intersections between y and x_temp
    valid_xy = []
    for i in list(y_steps & x_temp_steps):
        valid_xy += [(x1, y1) for x1 in x['temp'][i] for y1 in y[i]]

    # find intersections between y and x_stay, where x_stay index <= y index
    for iy in y_steps:
        for ix in [x1 for x1 in x_stay_steps if x1 <= iy]:
            valid_xy += [(x2, y2) for x2 in x['stay'][ix] for y2 in y[iy]]

    # remove duplicates
    valid_xy = list(set(valid_xy))
    
    # output
    if verbose:
        print('x:\n',x)
        print()
        print('y:\n',y)
        print()
        print(valid_xy)
    
    print('answer 17b:',len(valid_xy))
    
    return valid_xy

task17b(task['example'], verbose=True) # 112
l = task17b(task['real']) # 968

# mooi ploatie
sim_plot(l, task['real'], (5,7))


# benchmark
benchmark("task17a(task['real'])", 1000)
benchmark("task17b(task['real'])", 1000)
