# Assembly language source code for the MM1 processor simulator  # Python 3 fix
# This file contains assembly instructions, not Python code.
# It was originally saved with a .py extension but is meant to be read
# by assembler.py / simulator.py as input data.
#
# Original content:
# 01 LD 32 r0  #initial velocity = 0
# 02 LD 33 r1  #acceleration due to gravity
# 03 LD 34 r2  #time step 1 sec.
# 04 LD 35 r3  #height
# 05 LD 36 r4  #constant = 0
# 06 ADD r0 r1 r0 #calculates new velocity
# 07 SUB r3 r0 r3 #calculates new height
# 08 JN 10
# 09 JMP 06
# 10 LD r3 r4
# 11 MUL r0 r1 r0
# 12 JMP 06
# 32 DATA 0
# 33 DATA -1
# 34 DATA 1
# 35 DATA 30
# 36 DATA 0

PROGRAM = """
01 LD 32 r0  #initial velocity = 0
02 LD 33 r1  #acceleration due to gravity
03 LD 34 r2  #time step 1 sec.
04 LD 35 r3  #height
05 LD 36 r4  #constant = 0

06 ADD r0 r1 r0 #calculates new velocity
07 SUB r3 r0 r3 #calculates new height
08 JN 10
09 JMP 06
10 LD r3 r4
11 MUL r0 r1 r0
12 JMP 06

32 DATA 0
33 DATA -1
34 DATA 1
35 DATA 30
36 DATA 0
"""
