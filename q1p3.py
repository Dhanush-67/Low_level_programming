from codetypes import *


CODE = [
    Word(0xE3510000), #cmp R1 and #0 and if they are equal sets the status flag Z = 1
    Word(0x03E05000), #this line executes only if Z == 1, which we check by setting conditional code to 0, it sets R5 to #-1
    Word(0x03E06000), #this line executes only if Z == 1, which we check by setting conditional code to 0, it sets R6 to #-1
    Word(0x1735F110),
    Word(0xE12FFF1E)
]