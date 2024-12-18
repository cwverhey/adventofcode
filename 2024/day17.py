#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os; sys.path.append(os.path.dirname(__file__)); import aoc

#
# part 1
#

aoc.task(2024, 17, 1)

# instruction (opcode), input (operand)
# instruction_pointer starts at 0, increases by 2 after each instruction except `jump`
# when reading opcode beyond program length, halt
#
# operands: 
# literal: operand == value
# combo: 0...3 == value 0...3, 4 = register A, 5 = register B, 6 = register C, 7 = invalid

def read():
    global pointer, program
    pointer += 1
    return program[pointer-1]


#inputs = aoc.examples(2024, 17)[0]  # correct answer: 4,6,3,5,6,3,5,2,1,0
inputs = aoc.get_input(2024, 17)

coop = {'0':0, '1':1, '2':2, '3':3, '4':int(inputs[2]), '5':int(inputs[5]), '6':int(inputs[8])}  # 4,5,6 = A,B,C
program = inputs[10].split(',')
pointer = 0
output = []
#print(pointer, output, coop)

try:
    while True:
        opcode = read()
        operand = read()
        if opcode == '0':
            # adv = division to A
            coop['4'] = coop['4'] // 2**coop[operand]
        elif opcode == '1':
            # bxl = bitwise XOR B^litop
            coop['5'] = coop['5'] ^ int(operand)
        elif opcode == '2':
            # bst = modulo 8
            coop['5'] = coop[operand] % 8
        elif opcode == '3':
            # jnz = nothing or jump
            if coop['4'] != 0:
                pointer = int(operand)
        elif opcode == '4':
            # bxc = bitwise XOR B^C
            coop['5'] = coop['5'] ^ coop['6']
        elif opcode == '5':
            # out = output
            output.append(coop[operand]%8)
        elif opcode == '6':
            # bdv = division to B
            coop['5'] = coop['4'] // 2**coop[operand]
            pass
        elif opcode == '7':
            coop['6'] = coop['4'] // 2**coop[operand]
        #print(pointer, output, coop)
except IndexError:
    pass

stdout = ','.join([str(i) for i in output])

# submit answer
aoc.submit(2024, 17, 1, stdout)


#
# part 2
#

aoc.task(2024, 17, 2)

def tryInitA(program, coop_in, a_in):
    coop = coop_in.copy()
    coop[4] = a_in
    pointer = 0
    output = []
    #print(pointer, output, coop)
    try:
        while True:
            opcode = program[pointer]
            operand = program[pointer+1]
            pointer += 2
            if opcode == 0:
                coop[4] = coop[4] // 2**coop[operand]
            elif opcode == 1:
                coop[5] = coop[5] ^ int(operand)
            elif opcode == 2:
                coop[5] = coop[operand] % 8
            elif opcode == 3:
                if coop[4] != 0:
                    pointer = int(operand)
            elif opcode == 4:
                coop[5] = coop[5] ^ coop[6]
            elif opcode == 5:
                val = coop[operand]%8
                output.append(val)
            elif opcode == 6:
                coop[5] = coop[4] // 2**coop[operand]
                pass
            elif opcode == 7:
                coop[6] = coop[4] // 2**coop[operand]
            #print(pointer, output, coop)
    except IndexError:
        return output

#inputs = aoc.examples(2024, 17)[1]  # correct answer: 117440
inputs = aoc.get_input(2024, 17)  # correct answer: 164541160582845

coop = [0, 1, 2, 3, int(inputs[2]), int(inputs[5]), int(inputs[8])]  # 4,5,6 = A,B,C
program = [int(i) for i in inputs[10].split(',')]

matches = [0]
for pos in range(len(program)):
    print(f'position: {pos}')
    target = program[ len(program) - 1 - pos ]  # count pos from the end
    matches = [ i for m in matches for i in range(m*8, m*8+8) if tryInitA(program, coop, i)[0] == target ]
    print(matches)

answer = min(matches)

# submit answer
aoc.submit(2024, 17, 2, answer)

# push to git
# aoc.push_git(2024, 17)