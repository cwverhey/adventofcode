#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Day 22: Reactor Reboot

try:
    exec(open('AoC-functions.py').read())
except (NameError,FileNotFoundError):
    PATH = '/Users/caspar/Progs/adventofcode/'
    exec(open(f'{PATH}/AoC-functions.py').read())


task = getAoC(22, 2021, example='all')
task['example']
task['real']


import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import


#A x 0-10 y 0-10 z 0-10
#B x 2-5 y 2-5 z 2-5
#
#split A into 6 parts:
#    x 0-1 y 0-10 z 0-10
#    x 6-10 y 0-10 z 0-10
#    x 2-5 y 0-1 z 0-10
#    x 2-5 y 6-10 z 0-10
#    x 2-5 y 2-5 z 0-1
#    x 2-5 y 2-5 z 6-10
def split_cuboid(cuboid, mask, verbose=False):

    # check for overlap
    if cuboid[0] > mask[1] or cuboid[1] < mask[0] or cuboid[2] > mask[3] or cuboid[3] < mask[2] or cuboid[4] > mask[5] or cuboid[5] < mask[4]:
        if verbose: print('no overlap')
        return cuboid

    if verbose: print('overlap')
    split_cuboids = []

    # add left and right pancakes to new split_cuboid, and shrink original cuboid
    if cuboid[0] < mask[0]:
        split_cuboids.append([cuboid[0], mask[0]-1, cuboid[2], cuboid[3], cuboid[4], cuboid[5]])
        cuboid[0] = mask[0]
        #if verbose: plot_examples(np.array(split_cuboids))

    if cuboid[1] > mask[1]:
        split_cuboids.append([mask[1]+1, cuboid[1], cuboid[2], cuboid[3], cuboid[4], cuboid[5]])
        cuboid[1] = mask[1]
        #if verbose: plot_examples(np.array(split_cuboids))

    # front and back walls
    if cuboid[2] < mask[2]:
        split_cuboids.append([cuboid[0], cuboid[1], cuboid[2], mask[2]-1, cuboid[4], cuboid[5]])
        cuboid[2] = mask[2]
        #if verbose: plot_examples(np.array(split_cuboids))

    if cuboid[3] > mask[3]:
        split_cuboids.append([cuboid[0], cuboid[1], mask[3]+1, cuboid[3], cuboid[4], cuboid[5]])
        cuboid[3] = mask[3]
        #if verbose: plot_examples(np.array(split_cuboids))

    # top and bottom caps
    if cuboid[4] < mask[4]:
        split_cuboids.append([cuboid[0], cuboid[1], cuboid[2], cuboid[3], cuboid[4], mask[4]-1])
        #if verbose: plot_examples(np.array(split_cuboids))

    if cuboid[5] > mask[5]:
        split_cuboids.append([cuboid[0], cuboid[1], cuboid[2], cuboid[3], mask[5]+1, cuboid[5]])
        #if verbose: plot_examples(np.array(split_cuboids))

    return np.array(split_cuboids)

#split_cuboid([0,10,0,10,0,10], [2,5,2,5,2,5])  # m inside c
#split_cuboid([0,6,0,6,0,6], [1,5,1,5,1,5])  # m inside c
#split_cuboid([0,2,0,2,0,2], [0,1,0,1,0,1])  # m on edge of c
#split_cuboid([5,10,5,10,5,10], [0,1,0,1,0,1])  # m under in c
#split_cuboid([5,10,5,10,5,10], [11,12,11,12,11,12])  # m above c
#split_cuboid([5,10,5,10,5,10], [1,12,1,12,1,12])  # m around c


def plot_cuboids(cuboids_in):

    cuboids = cuboids_in.copy()

    print('in:')
    print(cuboids)

    # shift towards (0,0,0)
    cuboids[:,5] -= min(cuboids[:,4])
    cuboids[:,4] -= min(cuboids[:,4])
    cuboids[:,3] -= min(cuboids[:,2])
    cuboids[:,2] -= min(cuboids[:,2])
    cuboids[:,1] -= min(cuboids[:,0])
    cuboids[:,0] -= min(cuboids[:,0])

    print('out:')
    print(cuboids)

    # prepare some coordinates
    x, y, z = np.indices((max(cuboids[:,1])+1, max(cuboids[:,3])+1, max(cuboids[:,5])+1))

    # draw cuboids
    cubes = []
    for cu in cuboids:
        print(cu)
        cubes.append( (cu[0] <= x) & (x <=  cu[1]) & (cu[2] <= y) & (y <= cu[3]) & (cu[4] <= z) & (z <= cu[5]) )
    print()

    # combine the objects into a single boolean array
    voxelarray = False
    for cu in cubes:
        voxelarray = voxelarray | cu

    # set the colors of each object
    colors = np.empty(voxelarray.shape, dtype=object)
    allcolors = ['#88000044', '#FF000044', '#00880044', '#00FF0044', '#00008844', '#0000FF44']
    for i,cu in enumerate(cubes):
        colors[cu] = allcolors[i%len(allcolors)]

    # and plot everything
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

    plt.show()


def parse_input(joblist, limit50 = False):

    jobs = []

    for j in joblist:
        m = re.match('(\w+) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)',j)
        job = [int(m.groups(0)[1]), int(m.groups(0)[2]), int(m.groups(0)[3]), int(m.groups(0)[4]), int(m.groups(0)[5]), int(m.groups(0)[6]), m.groups(0)[0]=='on']

        if limit50:
            if job[0] > 50 or job[1] < -50 or job[2] > 50 or job[3] < -50 or job[4] > 50 or job[5] < -50:
                continue  # outside of scope
            else:
                for i in range(0,6,2):
                    job[i] = max(job[i], -50)
                for i in range(1,6,2):
                    job[i] = min(job[i], 50)

        jobs.append(job)

    return jobs

#parse_input(task['example'][0], limit50=True)
#parse_input(task['example'][1], limit50=True)
#parse_input(task['real'], limit50=True)


def dumb_list(cuboids):

    xyzlist = []
    for c in cuboids:
        for x in range(c[0],c[1]+1):
            for y in range(c[2],c[3]+1):
                for z in range(c[4],c[5]+1):
                    xyzlist.append([x,y,z])
    return xyzlist

#cuboids = task22a(task['example'][0][:2], verbose=True)
#dumb_list(cuboids)


def task22a(joblist, verbose=False):

    jobs = parse_input(joblist, limit50 = True)

    cuboids = []
    for j in jobs:

        if verbose: print('\njob:', j)

        new_cuboids = []

        for c in cuboids:
            if verbose: print('\nintersect with:\n', c)

            new = split_cuboid(c, j[:6], verbose)
            if verbose: print('intersect result:\n', new)
            if len(new):
                new_cuboids.append(new)

        if j[6]:
            if verbose: print('append job:\n', j[:6])
            new_cuboids.append(j[:6])

        cuboids = np.vstack(new_cuboids)
        if verbose: print('cuboids:\n', cuboids)


    sumvolume = 0
    for c in cuboids:
        sumvolume += (c[1]-c[0]+1)*(c[3]-c[2]+1)*(c[5]-c[4]+1)
    print('answer 22a:',sumvolume)

    if verbose: plot_cuboids(cuboids)

#task22a(task['example'][0], verbose=True)  # 39
#task22a(task['example'][1], verbose=True)  # 590784
#task22a(task['real'], verbose=True)        # 615869


def task22b(joblist, verbose=False):

    jobs = parse_input(joblist, limit50 = False)

    cuboids = []
    for j in jobs:

        if verbose: print('\njob:', j)

        new_cuboids = []

        for c in cuboids:
            if verbose: print('\nintersect with:\n', c)

            new = split_cuboid(c, j[:6], verbose)
            if verbose: print('intersect result:\n', new)
            if len(new):
                new_cuboids.append(new)

        if j[6]:
            if verbose: print('append job:\n', j[:6])
            new_cuboids.append(j[:6])

        cuboids = np.vstack(new_cuboids)
        if verbose: print('cuboids:\n', cuboids)


    sumvolume = 0
    for c in cuboids:
        sumvolume += (c[1]-c[0]+1)*(c[3]-c[2]+1)*(c[5]-c[4]+1)

    print('answer 22b:', sumvolume)

#example3 = ['on x=-5..47,y=-31..22,z=-19..33', 'on x=-44..5,y=-27..21,z=-14..35', 'on x=-49..-1,y=-11..42,z=-10..38', 'on x=-20..34,y=-40..6,z=-44..1', 'off x=26..39,y=40..50,z=-2..11', 'on x=-41..5,y=-41..6,z=-36..8', 'off x=-43..-33,y=-45..-28,z=7..25', 'on x=-33..15,y=-32..19,z=-34..11', 'off x=35..47,y=-46..-34,z=-11..5', 'on x=-14..36,y=-6..44,z=-16..29', 'on x=-57795..-6158,y=29564..72030,z=20435..90618', 'on x=36731..105352,y=-21140..28532,z=16094..90401', 'on x=30999..107136,y=-53464..15513,z=8553..71215', 'on x=13528..83982,y=-99403..-27377,z=-24141..23996', 'on x=-72682..-12347,y=18159..111354,z=7391..80950', 'on x=-1060..80757,y=-65301..-20884,z=-103788..-16709', 'on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856', 'on x=-52752..22273,y=-49450..9096,z=54442..119054', 'on x=-29982..40483,y=-108474..-28371,z=-24328..38471', 'on x=-4958..62750,y=40422..118853,z=-7672..65583', 'on x=55694..108686,y=-43367..46958,z=-26781..48729', 'on x=-98497..-18186,y=-63569..3412,z=1232..88485', 'on x=-726..56291,y=-62629..13224,z=18033..85226', 'on x=-110886..-34664,y=-81338..-8658,z=8914..63723', 'on x=-55829..24974,y=-16897..54165,z=-121762..-28058', 'on x=-65152..-11147,y=22489..91432,z=-58782..1780', 'on x=-120100..-32970,y=-46592..27473,z=-11695..61039', 'on x=-18631..37533,y=-124565..-50804,z=-35667..28308', 'on x=-57817..18248,y=49321..117703,z=5745..55881', 'on x=14781..98692,y=-1341..70827,z=15753..70151', 'on x=-34419..55919,y=-19626..40991,z=39015..114138', 'on x=-60785..11593,y=-56135..2999,z=-95368..-26915', 'on x=-32178..58085,y=17647..101866,z=-91405..-8878', 'on x=-53655..12091,y=50097..105568,z=-75335..-4862', 'on x=-111166..-40997,y=-71714..2688,z=5609..50954', 'on x=-16602..70118,y=-98693..-44401,z=5197..76897', 'on x=16383..101554,y=4615..83635,z=-44907..18747', 'off x=-95822..-15171,y=-19987..48940,z=10804..104439', 'on x=-89813..-14614,y=16069..88491,z=-3297..45228', 'on x=41075..99376,y=-20427..49978,z=-52012..13762', 'on x=-21330..50085,y=-17944..62733,z=-112280..-30197', 'on x=-16478..35915,y=36008..118594,z=-7885..47086', 'off x=-98156..-27851,y=-49952..43171,z=-99005..-8456', 'off x=2032..69770,y=-71013..4824,z=7471..94418', 'on x=43670..120875,y=-42068..12382,z=-24787..38892', 'off x=37514..111226,y=-45862..25743,z=-16714..54663', 'off x=25699..97951,y=-30668..59918,z=-15349..69697', 'off x=-44271..17935,y=-9516..60759,z=49131..112598', 'on x=-61695..-5813,y=40978..94975,z=8655..80240', 'off x=-101086..-9439,y=-7088..67543,z=33935..83858', 'off x=18020..114017,y=-48931..32606,z=21474..89843', 'off x=-77139..10506,y=-89994..-18797,z=-80..59318', 'off x=8476..79288,y=-75520..11602,z=-96624..-24783', 'on x=-47488..-1262,y=24338..100707,z=16292..72967', 'off x=-84341..13987,y=2429..92914,z=-90671..-1318', 'off x=-37810..49457,y=-71013..-7894,z=-105357..-13188', 'off x=-27365..46395,y=31009..98017,z=15428..76570', 'off x=-70369..-16548,y=22648..78696,z=-1892..86821', 'on x=-53470..21291,y=-120233..-33476,z=-44150..38147', 'off x=-93533..-4276,y=-16170..68771,z=-104985..-24507']
#task22b(task['example'][0])  # 39
#task22b(task['example'][1])  # 39769202357779
#task22b(example3)            # 2758514936282235
#task22b(task['real'])        # 1323862415207825

# benchmark
benchmark("task22a(task['real'])", 100)
benchmark("task22b(task['real'])", 5)
