#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 8, 1)
# 0-9a-zA-Z: frequency
# antinode: in line with 2 same-frequency antennae, with the first antenna being twice as far away as the other (what about in between nodes?)

import numpy as np
from collections import defaultdict
from pprint import pprint
import itertools

#inputs = aoc.examples(2024, 8)[0]  # correct answer: 14
inputs = aoc.get_input(2024, 8)

# load map and dict of antennae coordinates
map = np.array([list(line) for line in inputs])
for line in map:
    print(''.join(line))
frequencies = defaultdict(lambda: np.empty((0, 2), dtype=int))
for coord, val in np.ndenumerate(map):
    if val != '.':
        frequencies[str(val)] = np.append(frequencies[str(val)], [coord], axis=0)
pprint(frequencies)

# iterate over all combinations of 2 same-frequency antennae
antinodes = np.empty((0,2), int)
for antennae in frequencies.values():
    sets = list(itertools.combinations(antennae, 2))
    for ant1, ant2 in sets:
        antinodes = np.vstack([antinodes,
            ant1 - (ant2-ant1),
            ant2 - (ant1-ant2)
        ])

# remove duplicates and coordinates outside map
antinodes = np.unique(antinodes, axis=0)
antinodes = antinodes[ np.all((0 <= antinodes) & (antinodes < len(map)), axis=1) ]


# submit answer
aoc.submit(2024, 8, 1, len(antinodes))


#
# part 2
#

aoc.task(2024, 8, 2)

import numpy as np
from collections import defaultdict
from pprint import pprint
import itertools
from math import gcd

#inputs = aoc.examples(2024, 8)[0]  # correct answer: 34
inputs = aoc.get_input(2024, 8)

# load map and dict of antennae coordinates
map = np.array([list(line) for line in inputs])
for line in map:
    print(''.join(line))
frequencies = defaultdict(lambda: np.empty((0, 2), dtype=int))
for coord, val in np.ndenumerate(map):
    if val != '.':
        frequencies[str(val)] = np.append(frequencies[str(val)], [coord], axis=0)
pprint(frequencies)

# iterate over all combinations of 2 same-frequency antennae
antinodes = np.empty((0,2), int)
for antennae in frequencies.values():
    sets = list(itertools.combinations(antennae, 2))
    for ant1, ant2 in sets:
        # find smallest integer step from ant1 to ant2
        distance = ant1 - ant2
        step = distance // gcd(*distance)
        # step from ant1 to the edge
        pos = ant1.copy()
        while np.all((0 <= pos) & (pos < len(map))):
            antinodes = np.vstack([antinodes, pos])
            pos += step
        # -step from ant1 to the edge
        pos = ant1.copy()
        while np.all((0 <= pos) & (pos < len(map))):
            antinodes = np.vstack([antinodes, pos])
            pos -= step

# remove duplicates
antinodes = np.unique(antinodes, axis=0)

# submit answer
aoc.submit(2024, 8, 2, len(antinodes))

# push to git
aoc.push_git(2024, 8)