#----------------------------------------------------------------------
# MM1 - instruction set definitions
#----------------------------------------------------------------------
# bits     12 11 10  9| 8  7  6|  5  4  3|  2  1  0
# field    opcode     |  src1  |   src2  |   dest


#Instruction decode masks
OPCODE_MASK = 15 << 9
SRC1_MASK   = 7  << 6
SRC2_MASK   = 7  << 3
DEST_MASK   = 7
LD_SRC_MASK = 63 << 3
ST_DEST_MASK= 63
JUMP_DEST_MASK = 63

#opcodes
ADD=0
SUB=1
MUL=2
DIV=3
INC=4
LD =5
ST =6
MOV=7
JMP=8
JZ =9 
JN =10
HALT=15
