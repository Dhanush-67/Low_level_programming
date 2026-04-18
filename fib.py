from codetypes import *


CODE = [
    Label("fib"),

    # If the emulator starts with SP = 0, wrap it once to 0xFFFFFFFC
    # before using it for any stores. Recursive calls skip this path.
    Cmp(Reg(13), Word(0)),
    Mov(Reg(12), Word(0)),
    B(LabelRef("fib_stack_ready"), Cond.NE),
    Sub(Reg(13), Reg(13), Word(4)),
    Mov(Reg(12), Word(1)),

    Label("fib_stack_ready"),
    # Save the caller-visible registers we use, plus LR and an init flag.
    Sub(Reg(13), Reg(13), Word(20)),
    Str(Reg(1), Reg(13), Word(0)),
    Str(Reg(2), Reg(13), Word(4)),
    Str(Reg(3), Reg(13), Word(8)),
    Str(Reg(12), Reg(13), Word(12)),
    Str(Reg(14), Reg(13), Word(16)),

    # Base case: fib(0) = 0 and fib(1) = 1.
    Cmp(Reg(0), Word(1)),
    B(LabelRef("fib_done"), Cond.LS),

    # Save n in R1, compute fib(n - 1), then fib(n - 2).
    Mov(Reg(1), Reg(0)),
    Sub(Reg(0), Reg(0), Word(1)),
    Bl(LabelRef("fib")),
    Mov(Reg(2), Reg(0)),
    Sub(Reg(0), Reg(1), Word(2)),
    Bl(LabelRef("fib")),
    Add(Reg(0), Reg(0), Reg(2)),

    Label("fib_done"),
    Ldr(Reg(1), Reg(13), Word(0)),
    Ldr(Reg(2), Reg(13), Word(4)),
    Ldr(Reg(3), Reg(13), Word(8)),
    Ldr(Reg(14), Reg(13), Word(16)),
    Ldr(Reg(12), Reg(13), Word(12)),
    Add(Reg(13), Reg(13), Word(20)),
    Cmp(Reg(12), Word(1)),
    Add(Reg(13), Reg(13), Word(4), Cond.EQ),
    Bx(Reg(14)),
]
