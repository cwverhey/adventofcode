#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(18)

input = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''.split('\n')

input = get_input(18, lines=True)

DIRECTIONS = {'U': (-1,0), 'D': (1,0), 'L': (0,-1), 'R': (0,1)}

def coord_sum(c1, c2):
    return (c1[0]+c2[0], c1[1]+c2[1])

def coord_mul(c1, mul):
    return (c1[0]*mul, c1[1]*mul)

# find the coordinates of the polygon's vertices
coords = []
coord = (0,0)
for i in input:
    dir,steps,color = i.split(' ')
    coord = coord_sum( coord, coord_mul(DIRECTIONS[dir], int(steps)) )
    coords.append(coord)
    print(i, coord)

# lace them up (https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem)
S = sum([ coords[i][0]*coords[i+1][1] - coords[i][1]*coords[i+1][0] for i in range(len(coords)-1)])  # ∑( X1*Y2 - Y1*X2 ... X(n-1)*Yn - Y(n-1)*Xn )
S += coords[-1][0]*coords[0][1] - coords[-1][1]*coords[0][0]  # + Xn*Y1 - Yn*X1
A = abs(S)/2  # A = 0.5*|S|
A += sum([int(i.split(' ')[1]) for i in input])/2+1  # + 0.5*edgepieces_count + 1 (Verhey's Theorema, unproven)
A = int(A)

submit(18, 1, A)  # 48400


#
# part 2
#

input = '''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''.split('\n')

input = get_input(18, lines=True)

DIRECTIONS = ((0,1), (1,0), (0,-1), (-1,0))

def coord_sum(c1, c2):
    return (c1[0]+c2[0], c1[1]+c2[1])

def coord_mul(c1, mul):
    return (c1[0]*mul, c1[1]*mul)

# find the coordinates of the polygon's vertices
coords = []
coord = (0,0)
for i in input:
    _,_,hex = i.split(' ')
    steps = int(hex[2:7], 16)
    dir = DIRECTIONS[ int(hex[7]) ]
    coord = coord_sum( coord, coord_mul(dir, int(steps)) )
    coords.append(coord)
    print(i, coord)

# lace them up (https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem)
S = sum([ coords[i][0]*coords[i+1][1] - coords[i][1]*coords[i+1][0] for i in range(len(coords)-1)])  # ∑( X1*Y2 - Y1*X2 ... X(n-1)*Yn - Y(n-1)*Xn )
S += coords[-1][0]*coords[0][1] - coords[-1][1]*coords[0][0]  # + Xn*Y1 - Yn*X1
A = abs(S)/2  # A = 0.5*|S|
A += sum([int(i.split(' ')[2][2:7], 16) for i in input])/2+1  # + 0.5*edgepieces_count + 1 (Verhey's Theorema, unproven)
A = int(A)

submit(18, 2, A)  # 72811019847283