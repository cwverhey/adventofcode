#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(16)

input = '''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''.split('\n')

input = get_input(16, lines=True)

# parse input
grid = np.reshape( np.array( [*''.join(input)] ), (len(input),len(input[0])))
nrows,ncols = grid.shape

# beam directions when encountering a deflector
deflections = { # headings: ^ -2, < -1, > +1, v +2
    '|':  { -2: [[-1,0]],       -1: [[-1,0],[1,0]], 1: [[-1,0],[1,0]], 2: [[1,0]]        },
    '-':  { -2: [[0,-1],[0,1]], -1: [[0,-1]],       1: [[0,1]],        2: [[0,-1],[0,1]] },
    '/':  { -2: [[0,1]],        -1: [[1,0]],        1: [[-1,0]],       2: [[0,-1]]       },
    '\\': { -2: [[0,-1]],       -1: [[-1,0]],       1: [[1,0]],        2: [[0,1]]        }
}

# trace the beams
history = np.empty(shape=grid.shape, dtype=object) # per tile, a list of directions in which an beam has *entered* the tile
for r,row in enumerate(history):
    for c,val in enumerate(row):
        history[r,c] = []

beams = [[0, -1, 0, +1]] # row, column, row direction, column direction

def addbeam(beam):
    global history
    global newbeams

    # check if inside grid
    if not (0 <= beam[0] < nrows and 0 <= beam[1] < ncols):
        return
    
    # check if not visited before
    dir = beam[2]*2 + beam[3]
    if dir in history[ beam[0], beam[1] ]:
        return
    
    # add as new beam
    newbeams.append( beam )
    history[ beam[0], beam[1] ].append(dir)

while beams:
    newbeams = []
    for beam in beams:
        step = grid[beam[0],beam[1]]
        #print(beam[0], beam[1], step)
        if step == '.':
            addbeam( [beam[0]+beam[2], beam[1]+beam[3], beam[2], beam[3]] )
        else:
            for deflect in deflections[ step ][ beam[2]*2 + beam[3] ]:
                addbeam( [beam[0]+deflect[0], beam[1]+deflect[1], deflect[0], deflect[1]] )
    beams = newbeams

"""
    for i in range(len(grid)):
        x = grid[i].copy()
        for b in beams:
            if b[0] == i:
                try:
                    direction = b[2]*2 + b[3]
                    x[b[1]] = {-2: '↑', -1: '˿', 1: '˃', 2: '↓'}[direction]
                except IndexError:
                    pass
        print(''.join(x))
    print()

for row in history:
    print(''.join([ '#' if len(val) else ' ' for val in row ]))
    for val in row:
        if len(val):
            print('#', end='')
        else
        print(val, end='')
    print()
"""

energized_tiles = sum([1 for (r,c),v in np.ndenumerate(history) if v])

submit(16, 1, energized_tiles) # 7860


#
# part 2
#
get_task(16)

input = '''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....'''.split('\n')

input = get_input(16, lines=True)

# parse input
grid = np.reshape( np.array( [*''.join(input)] ), (len(input),len(input[0])))
nrows,ncols = grid.shape

# helpers
deflections = { # headings: ^ -2, < -1, > +1, v +2
    '|':  { -2: [[-1,0]],       -1: [[-1,0],[1,0]], 1: [[-1,0],[1,0]], 2: [[1,0]]        },
    '-':  { -2: [[0,-1],[0,1]], -1: [[0,-1]],       1: [[0,1]],        2: [[0,-1],[0,1]] },
    '/':  { -2: [[0,1]],        -1: [[1,0]],        1: [[-1,0]],       2: [[0,-1]]       },
    '\\': { -2: [[0,-1]],       -1: [[-1,0]],       1: [[1,0]],        2: [[0,1]]        }
}


def addbeam(beam):
    global history
    global newbeams

    # check if inside grid
    if not (0 <= beam[0] < nrows and 0 <= beam[1] < ncols):
        return
    
    # check if not visited before
    dir = beam[2]*2 + beam[3]
    if dir in history[ beam[0], beam[1] ]:
        return
    
    # add as new beam
    newbeams.append( beam )
    history[ beam[0], beam[1] ].append(dir)


def energized_tile_count(startbeam):
    global history
    global newbeams

    # keep track of visited cells
    history = np.empty(shape=grid.shape, dtype=object) # per tile, a list of directions in which a beam *entered* the tile before
    for r,row in enumerate(history):
        for c,val in enumerate(row):
            history[r,c] = []
    history[startbeam[0],startbeam[1]].append(startbeam[2]*2 + startbeam[3])

    # trace the beam(s)
    beams = [startbeam] # row, column, row direction, column direction
    while beams:
        newbeams = []
        for beam in beams:
            step = grid[beam[0],beam[1]]
            #print(beam, step)
            if step == '.':
                addbeam( [beam[0]+beam[2], beam[1]+beam[3], beam[2], beam[3]] )
            else:
                for deflect in deflections[ step ][ beam[2]*2 + beam[3] ]:
                    addbeam( [beam[0]+deflect[0], beam[1]+deflect[1], deflect[0], deflect[1]] )
        beams = newbeams

    # count how many tiles are energized
    return sum([1 for (r,c),v in np.ndenumerate(history) if v])

starttiles = []
starttiles.extend([ [0, i, +1, 0] for i in range(ncols) ]) # from north
starttiles.extend([ [nrows-1, i, -1, 0] for i in range(ncols) ]) # from south
starttiles.extend([ [i, 0, 0, +1] for i in range(nrows) ]) # from west
starttiles.extend([ [i, ncols-1, 0, -1] for i in range(nrows) ]) # from east

maxlen = 0
for starttile in starttiles:
    print(starttile)
    maxlen = max(maxlen, energized_tile_count(starttile))

submit(16, 2, maxlen) # 8331