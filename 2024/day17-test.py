#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import argv


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


with open(argv[1], 'r') as f:
    INPUTS = f.read().split()

COOP = [0, 1, 2, 3, int(INPUTS[2]), int(INPUTS[5]), int(INPUTS[8])]  # 4,5,6 = A,B,C
PROGRAM = [int(i) for i in INPUTS[10].split(',')]

matches = [0]
for pos in range(len(PROGRAM)):
    #print(f'position: {pos}')
    target = PROGRAM[ len(PROGRAM) - 1 - pos ]  # count pos from the end
    matches = [ i for m in matches for i in range(m*8, m*8+8) if tryInitA(PROGRAM, COOP, i)[0] == target ]
    #print(matches)

answer = min(matches)

print(answer)