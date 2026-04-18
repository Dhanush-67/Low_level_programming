from codetypes import *

HEAP_START = 0xFF000000
HEAP_SIZE = 0x00800000


CODE = [
    Label("malloc"),
    #save SP along with other registers we will be using for this function and LR in stack
    Sub(Reg(13), Reg(13), Word(28)),
    Str(Reg(4), Reg(13), Word(0)),
    Str(Reg(5), Reg(13), Word(4)),
    Str(Reg(6), Reg(13), Word(8)),
    Str(Reg(7), Reg(13), Word(12)),
    Str(Reg(8), Reg(13), Word(16)),
    Str(Reg(9), Reg(13), Word(20)),
    Str(Reg(14), Reg(13), Word(24)),

    #If user asks for 0 bytes, then skip the rest of the steps
    Cmp(Reg(0), Word(0)),
    B(LabelRef("return_zero"), Cond.LE),

    #align the requested bytes with multiples of 4, else we will have issues when Ldr/Str
    #We also account for the header bytes so R8 = aligned bytes + 8
    Add(Reg(0), Reg(0), Word(3)),
    Mov(Reg(1), Word(4)),
    UDiv(Reg(0), Reg(0), Reg(1)),
    Mul(Reg(0), Reg(0), Reg(1)),
    Add(Reg(8), Reg(0), Word(8)),

    #Check if the heap was used before
    Mov(Reg(4), Word(0xFF000000)),
    Ldr(Reg(5), Reg(4), Word(0)),
    Cmp(Reg(5), Word(0)),

    #If heap was not used before set heap_size of first block to be the whole heap_size and  set flag to free
    B(LabelRef("ready"), Cond.NE),
    Mov(Reg(5), Word(HEAP_SIZE)),
    Str(Reg(5), Reg(4), Word(0)),
    Mov(Reg(1), Word(1)),
    Str(Reg(1), Reg(4), Word(4)),
    Label("ready"),

    #Set R9 to contain end of heap and R6 and R7 are local vars we will use for worst fit
    Mov(Reg(9), Word(HEAP_SIZE)),
    Add(Reg(9), Reg(4), Reg(9)),
    Mov(Reg(6), Word(0)),
    Mov(Reg(7), Word(0)),

    #Checks if we have reached end of heap, if true branch to finish scan by setting R6
    Label("malloc_loop"),
    Cmp(Reg(4), Reg(9)),
    B(LabelRef("malloc_return"), Cond.GE),

    #Stop the loop if the size of R4 is 0
    Ldr(Reg(5), Reg(4), Word(0)),
    Cmp(Reg(5), Word(0)),
    B(LabelRef("malloc_return"), Cond.EQ),

    #Get the flag indicating whether R4 which represents the current block is taken or not
    Ldr(Reg(1), Reg(4), Word(4)),
    Cmp(Reg(1), Word(1)),

    #If free, branch to see if the block is worst fit
    B(LabelRef("malloc_check"), Cond.EQ),
    Add(Reg(4), Reg(4), Reg(5)),
    B(LabelRef("malloc_loop")),

    #Checks if R5's size < R8 which contains num of bytes the user wanted
    # or R5's size < R7 which contains size of worst fit so far
    #if true then we move on
    Label("malloc_check"),
    Cmp(Reg(5), Reg(8)),
    B(LabelRef("malloc_store"), Cond.LT),
    Cmp(Reg(5), Reg(7)),
    B(LabelRef("malloc_store"), Cond.LE),

    #We store R7 with R5's size and R6 with R4's addy
    Mov(Reg(7), Reg(5)),
    Mov(Reg(6), Reg(4)),

    #We set R4 our header to point to next block of memory
    #by setting  R4 to R4 + size of R5
    Label("malloc_store"),
    Add(Reg(4), Reg(4), Reg(5)),
    B(LabelRef("malloc_loop")),

    #If R6 contains 0, return 0
    Label("malloc_return"),
    Cmp(Reg(6), Word(0)),
    B(LabelRef("return_zero"), Cond.EQ),

    # if block size is too small to split return the whole block
    Sub(Reg(5), Reg(7), Reg(8)),
    Cmp(Reg(5), Word(8)),
    B(LabelRef("malloc_store_block"), Cond.LT),

    # we write size of R8, that is the total size of block into size part of R6
    Str(Reg(8), Reg(6), Word(0)),
    #we mark R6's flag part as taken by setting it to 0
    Mov(Reg(1), Word(0)),
    Str(Reg(1), Reg(6), Word(4)),

    #Save addy of new block in R2 and set it's size as size of R5 which contains size of block after split
    # and also set it's flag to free
    Add(Reg(2), Reg(6), Reg(8)),
    Str(Reg(5), Reg(2), Word(0)),
    Mov(Reg(1), Word(1)),
    Str(Reg(1), Reg(2), Word(4)),

    #Sets R0 to addy to new block of memory, we add 8 to go to the payload part
    Add(Reg(0), Reg(6), Word(8)),
    B(LabelRef("malloc_registers")),

    Label("malloc_store_block"),
    Str(Reg(7), Reg(6), Word(0)),
    Mov(Reg(1), Word(0)),
    Str(Reg(1), Reg(6), Word(4)),

    Add(Reg(0), Reg(6), Word(8)),
    B(LabelRef("malloc_registers")),

    Label("return_zero"),
    Mov(Reg(0), Word(0)),

    Label("malloc_registers"),
    Ldr(Reg(4), Reg(13), Word(0)),
    Ldr(Reg(5), Reg(13), Word(4)),
    Ldr(Reg(6), Reg(13), Word(8)),
    Ldr(Reg(7), Reg(13), Word(12)),
    Ldr(Reg(8), Reg(13), Word(16)),
    Ldr(Reg(9), Reg(13), Word(20)),
    Ldr(Reg(14), Reg(13), Word(24)),
    Add(Reg(13), Reg(13), Word(28)),
    Bx(Reg(14)),

    Label("free"),
    Sub(Reg(13), Reg(13), Word(28)),
    Str(Reg(4), Reg(13), Word(0)),
    Str(Reg(5), Reg(13), Word(4)),
    Str(Reg(6), Reg(13), Word(8)),
    Str(Reg(7), Reg(13), Word(12)),
    Str(Reg(8), Reg(13), Word(16)),
    Str(Reg(9), Reg(13), Word(20)),
    Str(Reg(14), Reg(13), Word(24)),

    Cmp(Reg(0), Word(0)),
    B(LabelRef("free_registers"), Cond.EQ),

    Mov(Reg(8), Word(HEAP_START)),
    Ldr(Reg(5), Reg(8), Word(0)),
    Cmp(Reg(5), Word(0)),
    B(LabelRef("free_heap"), Cond.NE),


    Mov(Reg(5), Word(HEAP_SIZE)),
    Str(Reg(5), Reg(8), Word(0)),
    Mov(Reg(1), Word(1)),
    Str(Reg(1), Reg(8), Word(4)),

    Label("free_heap"),
    Mov(Reg(9), Word(HEAP_SIZE)),
    Add(Reg(9), Reg(8), Reg(9)),

    Sub(Reg(4), Reg(0), Word(8)),
    Ldr(Reg(5), Reg(4), Word(0)),
    Ldr(Reg(1), Reg(4), Word(4)),
    Cmp(Reg(1), Word(1)),
    B(LabelRef("free_registers"), Cond.EQ),
    Mov(Reg(1), Word(1)),
    Str(Reg(1), Reg(4), Word(4)),

    Label("free_registers"),
    Ldr(Reg(4), Reg(13), Word(0)),
    Ldr(Reg(5), Reg(13), Word(4)),
    Ldr(Reg(6), Reg(13), Word(8)),
    Ldr(Reg(7), Reg(13), Word(12)),
    Ldr(Reg(8), Reg(13), Word(16)),
    Ldr(Reg(9), Reg(13), Word(20)),
    Ldr(Reg(14), Reg(13), Word(24)),
    Add(Reg(13), Reg(13), Word(28)),
    Bx(Reg(14)),
]
