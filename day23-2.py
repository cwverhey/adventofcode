#!/usr/bin/env pypy3
# -*- coding: utf-8 -*-

# Day 23: Amphipod, part 2

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())

task = getAoC(23, 2021, example='all')
task['example'][11]
task['real'] = task['real'][:3] + ['  #D#C#B#A#','  #D#B#A#C#'] + task['real'][3:]


#
# set PRICE per step, per amphipod type
#

PRICE = {0: 1, 1: 10, 2: 100, 3: 1000}


#
# set CAVE cell ids
#

CAVE = [['#','#','#','#','#','#','#','#','#','#','#','#','#'],
        ['#', 16, 17, -1, 18, -1, 19, -1, 20, -1, 21, 22,'#'],
        ['#','#','#',  3,'#',  7,'#', 11,'#', 15,'#','#','#'],
        [' ',' ','#',  2,'#',  6,'#', 10,'#', 14,'#',' ',' '],
        [' ',' ','#',  1,'#',  5,'#',  9,'#', 13,'#',' ',' '],
        [' ',' ','#',  0,'#',  4,'#',  8,'#', 12,'#',' ',' '],
        [' ',' ','#','#','#','#','#','#','#','#','#',' ',' ']]

GROUPS = [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15],[16,17,18,19,20,21,22]]

SOLUTION = [0]*4+[1]*4+[2]*4+[3]*4


#
# create a dataset of PATHS containing the distance between each set of cells, and which cells are on its path
#

# coordinates per cell
ID_COORDS = {}
for r,row in enumerate(CAVE):
    for c,cell in enumerate(row):
        if cell in range(22+1):
            ID_COORDS[cell] = (r,c)
ID_COORDS = [ID_COORDS[n] for n in range(22+1)]

# path lengths to each cell for one cell
def cell_explorer(cellid, verbose=False):
    my_coor = ID_COORDS[cellid]
    my_val = CAVE[my_coor[0]][my_coor[1]]
    if verbose: print('coor:', my_coor)
    if verbose: print('value:', my_val)

    def walk_into(init_coor, distance, parent, blockades):
        points = {}
        for new_direction in [[-1,0],[1,0],[0,-1],[0,1]]:
            coor = (init_coor[0]+new_direction[0],init_coor[1]+new_direction[1])
            val = CAVE[coor[0]][coor[1]]
            if verbose: print('\t'*distance, coor, '=',val)
            if val != '#' and coor != parent:
                if val != -1:
                    points.update({int(val): (distance+1, blockades)})
                    subblocks = blockades + [int(val)]
                else:
                    subblocks = blockades
                if verbose: print('\t'*distance, 'walk into, distance =',distance+1, 'parent =',init_coor, 'blockades =',subblocks)
                points.update(walk_into(coor, distance+1, init_coor, subblocks))

        return points

    points = walk_into(my_coor, 0, my_coor, [])

    return dict(sorted(points.items()))
# cell_explorer(16, verbose=True)

# path lengths and obstacles between all cells
PATHS = [cell_explorer(n) for n in range(22+1)]
PATH_DISTANCES = [[PATHS[i][j][0] if j in PATHS[i].keys() else -1 for j in range(22+1)] for i in range(22+1)]
PATH_BARRIERS = [[PATHS[i][j][1] if j in PATHS[i].keys() else -1 for j in range(22+1)] for i in range(22+1)]

skipbarriers = {0:[2,3], 1:[3], 4:[6,7], 5:[7], 8:[10,11], 9:[11], 12:[14,15], 13:[15]}
for i in range(22+1):
    for j in range(22+1):
        if isinstance(PATH_BARRIERS[i][j], list):
            skips = []
            if i in skipbarriers.keys(): skips += skipbarriers[i]
            if j in skipbarriers.keys(): skips += skipbarriers[j]
            PATH_BARRIERS[i][j] = [x for x in PATH_BARRIERS[i][j] if x not in skips]


#
# load game state from task, return board
#

def load_board(joblist):

    lut = {'A': 0, 'B': 1, 'C': 2, 'D': 3, '.': -1}

    board = []
    for cellid in range(22+1):
        coor = ID_COORDS[cellid]
        raw = joblist[coor[0]][coor[1]]
        board.append(lut[raw])
    return board
# board = load_board(task['example'][11])


#
# print the cave, or the board
#

def print_cave(board=False):

    lut = {0: ' A ', 1: ' B ', 2: ' C ', 3: ' D ', -1: ' . '}

    text = ''
    for row in range(len(CAVE)):
        for col in range(len(CAVE[0])):
            if board is False:
                if CAVE[row][col] == '#':
                    text += '███'
                else:
                    text += str(CAVE[row][col]).rjust(2) + ' '
            else:
                cell = CAVE[row][col]
                if cell == '#':
                    text += '███'
                elif cell == -1:
                    text += '   '
                else:
                    text += lut[board[cell]]

        text += '\n'

    print(text, end='')

# shortcut
def p(cost,board):
    print_cave(board)
    print('cost =',cost, flush=False)
    print(flush=True)

# print_cave()
# print_cave(board)
# p([0],board)


#
# task
#

def task23b(joblist, verbose=False):


    # load paths and board
    board = load_board(joblist)
    cost = 0
    best_solution = 999999999


    #
    # check if a path between two cells is free or if it is occupied
    #
    def check_path(pos_from, pos_to):

        # check if target is free
        if board[pos_to] != -1: return False

        # check if inbetween points are free
        for pos in PATH_BARRIERS[pos_from][pos_to]:
            if board[pos] != -1:
                return False

        return True


    #
    # find first free position for each 'home'
    #
    def get_free_homes(board):
        free = [True,True,True,True]
        for i in range(4):
            group = GROUPS[i]
            for j in group:
                if board[j] == -1:
                    free[i] = j
                    break
                if board[j] != i:
                    free[i] = False
                    break
        return free


    #
    # move an amphipod to a new position on the board (!need to check_path first!)
    #
    def move_amphipod(oldpos, newpos, distance):
        nonlocal cost
        cost += PRICE[board[oldpos]] * distance
        board[newpos] = board[oldpos]
        board[oldpos] = -1


    #
    # find and backtrack all options for current board
    #
    def try_all_options(debug=False):

        nonlocal cost, best_solution

        # show board state
        if debug:
            p(cost, board)
            print('', flush=False)

        # get options for current board state for every amphipod
        move_opts_home = []
        move_opts = []
        free_homes = get_free_homes(board)
        for pos in range(22+1):

            # pos = cave field ID, val = amphipod atype on that field
            val = board[pos]

            # is there no amphipod on this position
            if val == -1:
                continue

            # is he in a 'home' and the one above is occupied?
            if pos < 15 and board[pos+1] != -1 and pos not in [3,7,11]:
                continue

            # is a home for this type available
            if free_homes[val] is not False:

                # is he already at home
                if val == pos//4:
                    continue

                # can he get home right away
                if check_path(pos, free_homes[val]):
                    move_opts_home.append((pos, free_homes[val], PATH_DISTANCES[pos][free_homes[val]]))
                    continue

            # check all places in the hallway that he can go
            if pos < 16 and not move_opts_home:
                for n in range(16,22+1):  # n = next field
                    if check_path(pos, n):
                        move_opts.append((pos, n, PATH_DISTANCES[pos][n], val))

        # if we can move one home, that is definitely the best move we can make: do it; otherwise try the other options
        if move_opts_home:
            move_opts = [move_opts_home[0]]

        # try out options
        if debug: print('option list:\n',move_opts, flush=False)
        for o in move_opts:

            # apply option
            if debug: print(o[0], '->', o[1], flush=False)
            move_amphipod(o[0], o[1], o[2])

            # recurse into option
            if cost < best_solution:
               try_all_options(debug)
            else:
                if debug: print('over budget!', flush=False)

            # backtrack
            if debug: print(o[0], '<-', o[1], flush=False)
            move_amphipod(o[1], o[0], -o[2])

        # did we find a solution?
        if not move_opts and board[:16] == SOLUTION and cost < best_solution:

            best_solution = cost


    # make it so
    try_all_options(verbose)
    answer = best_solution
    print('answer 23b:',answer)

# task23b(task['example'][11])  # 44169
# task23b(task['real'])  # 48304


# benchmark
benchmark("task23b(task['example'][11])", 1)
benchmark("task23b(task['real'])", 1)
