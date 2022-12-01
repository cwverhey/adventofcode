#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 19: Beacon Scanner (take 2)

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(19, 2021, example='all')
task['example'][5]
task['real']

import itertools
import numpy as np


#
#        Z
#        ^           (X, Y, Z)
#    X <   > Y
#
# indices: [0:A, 1:B, 2:C, 3:-A, 4:-B, 5:-C]
rotations = [
    (0,1,2), (0,2,4), (0,4,5), (0,5,1),
    (1,0,5), (1,5,3), (1,3,2), (1,2,0),
    (2,0,1), (2,1,3), (2,3,4), (2,4,0),
    (3,1,5), (3,5,4), (3,4,2), (3,2,1),
    (4,0,2), (4,2,3), (4,3,5), (4,5,0),
    (5,0,4), (5,4,3), (5,3,1), (5,1,0)
    ]


# text input to list of tuples
def parse_input(tasklist):
    
    task = tasklist.copy()
    parsed = [np.array([], np.int16)]
    
    task.pop(0)
    scanner = 0
    while(len(task)):
        line = task.pop(0)
        if line == '':
            if len(task):
                scanner += 1
                parsed.append(np.array([], np.int16))
                task.pop(0)
        else:
            parsed[scanner] = np.append(parsed[scanner], [int(n) for n in line.split(',')])
            
    parsed = [x.reshape((-1,3)) for x in parsed]
    return parsed
    
# parse_input(task['example'][5])


# get one of 6 possible dimensions of scanned beacons
# dimensions: [0:A, 1:B, 2:C, 3:-A, 4:-B, 5:-C]
def get_dim(beacons, dim):
    if dim <= 2:
        return beacons[:,dim]
    else:
        return -beacons[:,dim-3]

#get_dim(parse_input(task['example'][5])[0], 3)


def check_overlap(l1, l2):
    
    arr = np.array(np.meshgrid(l1, l2)).reshape(2,-1)
    arr = arr[0] - arr[1]
    tally = np.unique(arr, return_counts=True)
    
    return list(tally[0][tally[1] >= 12])


def reorient_scanlist(l_in, rotshifts):
    
    xl = get_dim(l_in, rotshifts[0][0])
    xl = [x+rotshifts[0][1] for x in xl]
    
    yl = get_dim(l_in, rotshifts[1][0])
    yl = [y+rotshifts[1][1] for y in yl]
    
    zl = get_dim(l_in, rotshifts[2][0])
    zl = [z+rotshifts[2][1] for z in zl]
    
    return np.vstack((xl,yl,zl)).T


def get_identical(l1, l2):
    
    stack = np.vstack((l1, l2))
    unique = np.unique(stack, axis=0)
    return (len(stack) - len(unique), unique)

# get_identical(merged_scans, scan_add_r)


def merge_beacons(task, verbose=True):
    
    # list of scanners, np-array[n,3] per scanner
    scans = parse_input(task)

    # scanner 0 is the reference in both position and rotation
    merged_scans = scans[0]
    scanner_coords = [(0,0,0)]
    
    # add remaining scanners one-by-one
    unmerged_scans = scans[1:]
    while len(unmerged_scans):
        
        scan_add = unmerged_scans.pop(0)
        success = False
        
        # compare x dimension of reference with 6 possible directions in scan_add
        valid_x = []
        for rot in range(6):
            for s in check_overlap(merged_scans[:,0], get_dim(scan_add, rot)):
                if verbose: print(rot, s)
                valid_x.append((rot,s))
        
        # compare y dimension of reference with 0 to 6 possible directions in scan_add that'd match with valid x-rotations
        valid_y = []
        for rot in list(set([r[1] for r in rotations if r[0] in [x[0] for x in valid_x]])):
            for s in check_overlap(merged_scans[:,1], get_dim(scan_add,rot)):
                if verbose: print(rot, s)
                valid_y.append((rot,s))
        
        # compare z dimension of reference with 0 to 6 possible directions in scan_add that'd match with valid x- and y-rotations
        potential_rotations = list(set(itertools.product([x[0] for x in valid_x], [y[0] for y in valid_y])))
        potential_z_rotations = [r[2] for r in rotations if (r[0],r[1]) in potential_rotations]
        valid_z = []
        for rot in potential_z_rotations:
            for s in check_overlap(merged_scans[:,2], get_dim(scan_add, rot)):
                if verbose: print(rot, s)
                valid_z.append((rot,s))
        
        # get valid combinations of single axis valid rotations
        potential_rotations = list(set(itertools.product(valid_x, valid_y, valid_z)))
        potential_rotations = [relpos for relpos in potential_rotations if (relpos[0][0],relpos[1][0],relpos[2][0]) in rotations]
        for rots in potential_rotations:
            scan_add_r = reorient_scanlist(scan_add, rots)
            identical = get_identical(merged_scans, scan_add_r)
            if(identical[0] >= 12):
                if verbose: print('valid rot:',rots)
                merged_scans = identical[1]
                scanner_coords.append((rots[0][1],rots[1][1],rots[2][1]))
                success = True
                break
            
        if not success:
            unmerged_scans.append(scan_add)
            
    return({'beacons':merged_scans,'scanners':scanner_coords})

#merge_beacons(task['example'][5])


def task19a(task, verbose=False):
    answer = len(merge_beacons(task, verbose)['beacons'])
    print('answer 19a:',answer)

#task19a(task['example'][5]) # 79
#task19a(task['real']) # 381


def task19b(task, verbose=False):
    
    scanners = merge_beacons(task, verbose)['scanners']
    
    maxdistance = 0
    for i1, sc1 in enumerate(scanners):
        for i2, sc2 in enumerate(scanners[i1+1:]):
            if verbose: print(sc1, '->', sc2)
            distance = abs(sc1[0]-sc2[0]) + abs(sc1[1]-sc2[1]) + abs(sc1[2]-sc2[2])
            maxdistance = max(maxdistance, distance)
    
    print('answer 19b:',maxdistance)

#task19b(task['example'][5]) # 3621
#task19b(task['real']) # 12201


# benchmark
benchmark("task19a(task['real'])", 50)
benchmark("task19b(task['real'])", 50)
