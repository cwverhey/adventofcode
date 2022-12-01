#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-

# Day 19: Beacon Scanner

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(19, 2021, example='all')
task['example'][5]
task['real']

import itertools

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
    parsed = [[]]
    
    task.pop(0)
    scanner = 0
    while(len(task)):
        line = task.pop(0)
        if line == '':
            if len(task):
                scanner += 1
                parsed.append([])
                task.pop(0)
        else:
            num = tuple([int(n) for n in line.split(',')])
            parsed[scanner].append(num)
            
    return parsed
    
#parse_input(task['example'][5])

# get one of 6 possible dimensions of scanned beacons
# dimensions: [0:A, 1:B, 2:C, 3:-A, 4:-B, 5:-C]
def get_dim(beacons, dim):
    if dim <= 2:
        return [x[dim] for x in beacons]
    else:
        return [-x[dim-3] for x in beacons]


def count_identical_unsorted_items(l1i, l2i):
    
    l1 = l1i.copy()
    l2 = l2i.copy()
    
    count = 0
    
    while(len(l1)):
        v1 = l1.pop()
        try:
            l2.pop(l2.index(v1))
            count += 1
        except: pass
    
    return count
    
#count_identical_unsorted_items([(1,2,3),(4,5,6)], [(4,5,6),(7,8,9)]) # 1


def count_identical_sorted_items(l1i, l2i):
    
    l1 = l1i.copy()
    l2 = l2i.copy()
    
    count = 0
    
    if not len(l2): return 0
    v2 = l2.pop()
    
    while(len(l1)):
        v1 = l1.pop()
        while(v1 < v2):
            if not len(l2): break
            v2 = l2.pop()
        if v1 == v2:
            count += 1
            if not len(l2): break
            v2 = l2.pop()
    
    return count

#count_identical_sorted_items([1,2,3,4,5,6,6,6,8,9], [0,5,6,6,7,9]) # 4


def try_shifting(l1, l2):
    
    valid_shifts = []
    
    lim_left = l1[0] - l2[-12]
    lim_right = l1[-12] - l2[0]
    
    for shift in range(lim_left, lim_right+1):
        
        l2_s = [x+shift for x in l2]
        common = count_identical_sorted_items(l1, l2_s)
        if common >= 12:
            valid_shifts.append(shift)
            
    return valid_shifts


def rotate_and_shift_beacon(beacons, rotshifts):
    
    xl = get_dim(beacons, rotshifts[0][0])
    xl = [x+rotshifts[0][1] for x in xl]
    
    yl = get_dim(beacons, rotshifts[1][0])
    yl = [y+rotshifts[1][1] for y in yl]
    
    zl = get_dim(beacons, rotshifts[2][0])
    zl = [z+rotshifts[2][1] for z in zl]
    
    out = [(xl[i],yl[i],zl[i]) for i in range(len(xl))]
    
    return out


def merge_beacons(task, verbose=True):
    
    scans = parse_input(task)
    
    merged_scans = scans[0]
    scanner_coords = [(0,0,0)]
    
    unmerged_scans = scans[1:]
    
    while len(unmerged_scans):
        
        scan1 = unmerged_scans.pop(0)
        success = False
        
        # get matches on x-axis of scan0 with any of 6 potential corresponding axes of scanner 1
        x0 = sorted(get_dim(merged_scans,0))
        valid_x = []
        for rot in range(6):
            x1 = sorted(get_dim(scan1,rot))
            for s in try_shifting(x0, x1):
                valid_x.append((rot,s))
        valid_x_rotations = [x[0] for x in valid_x]
        
        # get matches on y-axis
        y0 = sorted(get_dim(merged_scans,1))
        valid_y = []
        for rot in list(set([r[1] for r in rotations if r[0] in valid_x_rotations])):
            y1 = sorted(get_dim(scan1,rot))
            for s in try_shifting(y0, y1):
                valid_y.append((rot,s))
        valid_y_rotations = [y[0] for y in valid_y]
        
        # get matches on z-axis
        z0 = sorted(get_dim(merged_scans,2))
        potential_rotations = list(set(itertools.product(valid_x_rotations,valid_y_rotations)))
        potential_z_rotations = [r[2] for r in rotations if (r[0],r[1]) in potential_rotations]
        valid_z = []
        for rot in potential_z_rotations:
            z1 = sorted(get_dim(scan1,rot))
            for s in try_shifting(z0, z1):
                valid_z.append((rot,s))
        
        # get valid combinations of single axis valid rotations
        potential_rotations = list(set(itertools.product(valid_x, valid_y, valid_z)))
        potential_rotations = [relpos for relpos in potential_rotations if (relpos[0][0],relpos[1][0],relpos[2][0]) in rotations]
        for rots in potential_rotations:
            scan1_r = rotate_and_shift_beacon(scan1, rots)
            common = count_identical_unsorted_items(merged_scans, scan1_r)
            if(common >= 12):
                if verbose: print('valid rot:',rots)
                merged_scans = list(set(merged_scans + scan1_r))
                scanner_coords.append((rots[0][1],rots[1][1],rots[2][1]))
                success = True
                break
            
        if not success:
            unmerged_scans.append(scan1)
            
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
benchmark("task19a(task['real'])", 1)
benchmark("task19b(task['real'])", 1)
