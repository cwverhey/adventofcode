#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from helper import *

#
# part 1
#
get_task(5)

input = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''.split('\n')

input = get_input(5, lines=True)

seeds = [ int(x) for x in re.findall('\d+', input[0]) ]
maps = []
for i in range(1, len(input)):
    if re.search('map:', input[i]):
        maps.append({'name': input[i], 'map': []})
    elif input[i] != '':
        maps[-1]['map'].append( [ int(x) for x in re.findall('\d+', input[i]) ] )

locations = []
for id in seeds:
    for conversion in maps:
        for m in conversion['map']:
            if m[1] <= id < m[1]+m[2]:
                id += m[0] - m[1]
                break
        # print(conversion['name'], id)
    locations.append(id)

submit(5, 1, min(locations)) # 178159714


#
# part 2
#
get_task(5)

input = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''.split('\n')

input = get_input(5, lines=True)

starttime = time.time()

# process input into `seeds` and `maps`
seeds = [ [int(x), int(y)] for x, y in re.findall('(\d+) (\d+)', input[0]) ]
maps = []
for i in range(1, len(input)):
    if re.search('map:', input[i]):
        maps.append({'name': input[i], 'map': []})
    elif input[i] != '':
        maps[-1]['map'].append( [ int(x) for x in re.findall('\d+', input[i]) ] )

# renumber seeds according to maps
ids = seeds
for conversion in maps:
    #print(conversion['name'], conversion['map'])
    #print('input ranges:', ids)

    # split input ranges into two if they span a map range boundary
    boundaries = unique( flatten( [[map[1],map[1]+map[2]] for map in conversion['map']] ) ) # first number of each source range (both the mapped ranges and the unmapped ranges in between)
    for b in boundaries:
        for i,id in enumerate(ids):
            if id[0] < b <= id[0]+id[1]-1:
                ids[i] = [id[0], b-id[0]]
                ids.append( [b, id[0]+id[1]-b] )
    #print('split input ranges:', ids)
    
    # try to find a suitable map for each input range, and renumber the input in place
    for i,id in enumerate(ids):
        for m in conversion['map']:
            if m[1] <= id[0] < m[1]+m[2]:
                id[0] += m[0] - m[1]
                break
    #print('output ranges:', ids)
    #print()

lowest_location_number = min( [x[0] for x in ids] )

endtime = time.time()
print('lowest location number: {} (took {}ms)'.format(lowest_location_number, round((endtime-starttime)*1000)))

submit(5, 2, lowest_location_number) # 100165128