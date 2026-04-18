from codetypes import *


CODE = [
    # Copy v from R0 so we can use it to patch the destination register field.
    Word(0xE1A01000),  # MOV R1, R0
    #E = 1110 AL
    #1 = 0001 00 data op, 0 = I(We are dealing with registers), 1 = part of MOV code
    #A = 1010 101 = part of MOV code, 0 = S(We don't want to affect status bit CPSR)
    #0 = 0000 = operand 1 is not required for MOV with registers
    #1 = 0001 = destination registers
    #00 = 0000 0000 (not required for data ops in registers)
    #0 = 0000 = seond operand which is R0

    # R2 = address of the second-to-last instruction (the ADD below).
    Word(0xE28F2010),  # ADD R2, PC, #16

    #     Binary:
    # 1110 0010 1000 1111 0010 0000 0001 0000

    # Field breakdown (ARM data-processing immediate format):

    # Bits 31:28 = 1110
    # Condition = AL (always)

    # Bits 27:26 = 00
    # Instruction class = data-processing

    # Bit 25 = 1
    # I bit = immediate Operand2

    # Bits 24:21 = 0100
    # Opcode = ADD

    # Bit 20 = 0
    # S bit = do not update flags

    # Bits 19:16 = 1111
    # Rn = R15 = PC

    # Bits 15:12 = 0010
    # Rd = R2

    # Bits 11:0 = 0000 0001 0000
    # Operand2 immediate encoding:

    # rotate_imm (11:8) = 0000, so no rotate
    # imm8 (7:0) = 00010000 = 16


    # Load the current ADD instruction word: 0xE08D0000.
    Word(0xE5923000),  # LDR R3, [R2]
    #E = 1110 Al
    #5 = 0101 madatory bits for ldr/str
    #9 = 1001 U = 1 for usnisgned L = 1 for loading
    #2 = R2
    #3 = R3
    #000 = needed for offset for ex [R2+#4]

    # 4096 = 1 << 12, so multiplying by it moves v into bits 15:12.
    Word(0xE3A04A01),  # MOV R4, #4096
    #E = 1110 Al
    #3 = 0011, 00 - data, 1 = I(We are dealing with immidiate), 1 - part of MOV
    #A = 1010 101 = part of MOV code, 0 = S(We don't want to affect status bit CPSR)
    #0 = 0000 We don't need operand 1
    #4 = 0100 R4
    #A = 1010 
    #0 = 0000
    #1 = 0001

    # R1 = v << 12
    Word(0xE0010194),  # MUL R1, R4, R1
    #Can also do: MOV R1, R1, LSL #12 instead of MUL R1 by R4 to shift bits left by 12

    # Patch the destination-register field of the ADD instruction.
    Word(0xE0833001),  # ADD R3, R3, R1

    # Store the modified instruction back into the code.
    Word(0xE5823000),  # STR R3, [R2]

    # Required second-to-last instruction.
    Word(0xE08D0000),  # ADD R0, R13, R0

    # Required last instruction.
    Word(0xE12FFF1E),  # BX R14
]
