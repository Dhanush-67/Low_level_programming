from codetypes import *


STDOUT = 0x09000000



CODE = [
    Label("main"),
    Mov(Reg(8), Word(0)),
    Mov(Reg(9), Word(STDOUT)),
    Add(Reg(9), Reg(9), Word(4)),#input
    Mov(Reg(10), Word(STDOUT)),#output
    Bl(LabelRef("tree_traverse")),
    Bx(Reg(14)),

    Label("tree_traverse"),
    Sub(Reg(13), Reg(13), Word(24)),
    Str(Reg(4), Reg(13), Word(0)),
    Str(Reg(5), Reg(13), Word(4)),
    Str(Reg(6), Reg(13), Word(8)),
    Str(Reg(7), Reg(13), Word(12)),
    Str(Reg(14), Reg(13), Word(16)),

    Label("skip_whitespace"),
    #with every iteration, R9 (input) contains next char
    Ldr(Reg(0), Reg(9), Word(0)),

    #end if we reach eof
    Add(Reg(1), Reg(0), Word(1)),
    Cmp(Reg(1), Word(0)),

    B(LabelRef("tree_registers"), Cond.EQ),

    #Skip if it's a whitespace
    Cmp(Reg(0), Word(32)),
    B(LabelRef("skip_whitespace"), Cond.EQ),

    #skip new line char
    Cmp(Reg(0), Word(10)),
    B(LabelRef("skip_whitespace"), Cond.EQ),

    Cmp(Reg(0), Word(88)),
    B(LabelRef("x"), Cond.EQ),

    Str(Reg(0), Reg(13), Word(20)),
    Bl(LabelRef("tree_traverse")),
    Bl(LabelRef("tree_traverse")),
    Ldr(Reg(0), Reg(13), Word(20)),
    Bl(LabelRef("print_char")),
    B(LabelRef("tree_registers")),

    Label("x"),
    Mov(Reg(0), Word(88)),
    Bl(LabelRef("print_char")),

    

    Label("tree_registers"),
    Ldr(Reg(4), Reg(13), Word(0)),
    Ldr(Reg(5), Reg(13), Word(4)),
    Ldr(Reg(6), Reg(13), Word(8)),
    Ldr(Reg(7), Reg(13), Word(12)),
    Ldr(Reg(14), Reg(13), Word(16)),
    Add(Reg(13), Reg(13), Word(24)),
    Bx(Reg(14)),

    Label("add_space"),
    Cmp(Reg(8), Word(0)),

    Mov(Reg(8), Word(1), Cond.EQ),
    Bx(Reg(14), Cond.EQ),

    Mov(Reg(2), Word(32)),
    Strb(Reg(2), Reg(10), Word(0)),
    Bx(Reg(14)),

    Label("print_char"),
    Sub(Reg(13), Reg(13), Word(8)),
    Str(Reg(0), Reg(13), Word(0)),
    Str(Reg(14), Reg(13), Word(4)),

    Bl(LabelRef("add_space")),

    Ldr(Reg(0), Reg(13), Word(0)),
    Strb(Reg(0), Reg(10), Word(0)),
    Ldr(Reg(14), Reg(13), Word(4)),
    Add(Reg(13), Reg(13), Word(8)),
    Bx(Reg(14)),
]
