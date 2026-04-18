from codetypes import *

#Change made to the file was changing multiline comments using """ """ to single line comments using # as multiline comments were causing an error
CODE = [
    #Add R5 R0 R1
    Word(0xE0805001),
    
    # E = 1110 (al)
    # 0 = 0000 (00 - data ops, 0 - I, 0 - part of opcode add)
    # 8 = 1000 (100 part of opcode add, 0 - S)
    # 0 = 0000 (R0, which is operand 1)
    # 5 = 0101 (R5, which is our destination register)
    # 0 = 0000 (no shift or rotate)
    # 0 = 0000 (no shift or rotate)
    # 1 = 0001 (R1, which is our second op)
    # BXLR

    Word(0xE12FFF1E)

    # E = 1110 (al)
    # 1 = 0001
    # 2 = 0010
    # F = 1111
    # F = 1111
    # F = 1111
    # 1 = 0001
    # E = 1110 (LR we are returning by branching to LR, which has the instruction to stop)
]
