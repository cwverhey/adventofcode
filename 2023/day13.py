#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(13)

input = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.\n
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''.split('\n')

input = get_input(13, lines=True)

# parse input
grids = []
newgrid = True
for i in input:
    if i == '':
        newgrid = True
    elif newgrid:
        grids.append( np.array([*i]) )
        newgrid = False
    else:
        grids[-1] = np.vstack( [ grids[-1], [*i] ] )

# keep score, iterate over grids
mirrors_hori = []
mirrors_vert = []
for grid in grids:

    # find horizontal mirrors
    for row in range(grid.shape[0]-1):
        # checking for mirror between rows {row} and {row+1}
        t = row
        b = row+1
        while(t >= 0 and b < grid.shape[0]):
            # break if row t != row b
            if any(grid[t] != grid[b]):
                break
            t -= 1
            b += 1
        else:
            mirrors_hori.append(row+1)

    # find vertical mirrors
    for col in range(grid.shape[1]-1):
        # checking for mirror between columns {col} and {col+1}
        l = col
        r = col+1
        while(l >= 0 and r < grid.shape[1]):
            # break if column l != column r
            if any(grid[:,l] != grid[:,r]):
                break
            l -= 1
            r += 1
        else:
            mirrors_vert.append(col+1)

print(mirrors_hori, mirrors_vert)

summary = sum(mirrors_vert) + 100 * sum(mirrors_hori)

submit(13, 1, summary) # 37975

#
# part 2
#

get_task(13)

input = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.\n
#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''.split('\n')

input = get_input(13, lines=True)

# parse input
grids = []
newgrid = True
for i in input:
    if i == '':
        newgrid = True
    elif newgrid:
        grids.append( np.array([*i]) )
        newgrid = False
    else:
        grids[-1] = np.vstack( [ grids[-1], [*i] ] )

# keep score, iterate over grids
mirrors_hori = []
mirrors_vert = []
for grid in grids:

    # find horizontal mirrors
    for row in range(grid.shape[0]-1):
        # checking for mirror between rows {row} and {row+1}
        t = row
        b = row+1
        smudges = 0
        while(t >= 0 and b < grid.shape[0]):
            smudges += sum(grid[t] != grid[b])
            if smudges > 1:
                break
            t -= 1
            b += 1
        else:
            if smudges == 1:
                mirrors_hori.append(row+1)

    # find vertical mirrors
    for col in range(grid.shape[1]-1):
        # checking for mirror between columns {col} and {col+1}
        l = col
        r = col+1
        smudges = 0
        while(l >= 0 and r < grid.shape[1]):
            smudges += sum(grid[:,l] != grid[:,r])
            if smudges > 1:
                break
            l -= 1
            r += 1
        else:
            if smudges == 1:
                mirrors_vert.append(col+1)

print(mirrors_hori, mirrors_vert)

summary = sum(mirrors_vert) + 100 * sum(mirrors_hori)

submit(13, 2, summary) # 32497
