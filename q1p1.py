from codetypes import *

#Change made to the file was changing multiline comments using """ """ to single line comments using # as multiline comments were causing an error

CODE = [
    #mov PC LR (added a comma due to my string which acts as a second element in list which causes error without comma)
    Word(0xE1A0F00E)
        #E = 1110 (al)
        # 1 = 0001 (00 - data ops, 0 - I, 1 - part of opcode mov)
        # A = 1010 (101 - part of opcode mov, 0 - S)
        # 0 = 0000 (operand 1, not required for mov)
        # F = 1111 (register 15, which is PC which is our destination register)
        # 0 = 0000 (No shifting or rotating)
        # 0 = 0000 (No shifting or rotating)
        # E = 1110 (register 14, which is LR, which is our second operand, where we will place Rd)
]
