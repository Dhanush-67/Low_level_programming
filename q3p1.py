from codetypes import *

CODE = [
    Mov(Reg(1), Word(0x09000000)),

    Cmp(Reg(0), Word(90)),
    B(Word(4), Cond.GE),

    Cmp(Reg(0), Word(85)),
    B(Word(9), Cond.GE),

    Cmp(Reg(0), Word(80)),
    B(Word(12), Cond.GE),

    # No A-range letter grade for inputs below 80.
    Bx(Reg(14)),

    # A+
    Mov(Reg(2), Word(65)),
    Strb(Reg(2), Reg(1), Word(0)),
    Mov(Reg(2), Word(43)),
    Strb(Reg(2), Reg(1), Word(0)),
    Mov(Reg(2), Word(10)),
    Strb(Reg(2), Reg(1), Word(0)),
    Bx(Reg(14)),

    # A
    Mov(Reg(2), Word(65)),
    Strb(Reg(2), Reg(1), Word(0)),
    Mov(Reg(2), Word(10)),
    Strb(Reg(2), Reg(1), Word(0)),
    Bx(Reg(14)),

    # A-
    Mov(Reg(2), Word(65)),
    Strb(Reg(2), Reg(1), Word(0)),
    Mov(Reg(2), Word(45)),
    Strb(Reg(2), Reg(1), Word(0)),
    Mov(Reg(2), Word(10)),
    Strb(Reg(2), Reg(1), Word(0)),
    Bx(Reg(14)),
]