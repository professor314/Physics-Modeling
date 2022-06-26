from processor  import *
from assembler  import *
import sys

DEBUG=False # setting to True enables single-stepping
max_instructions=150 # prevent inifinite loops by stopping after this many instructions

# The filename of the assembly language program
program_file = "falling.py"
#make a memory to hold the program and its output
memory     = Memory(64)


#load program from assembly language file into memory
load_program(program_file,memory)

#Make an instance of an MM1 supercomputer ;o) passing it a reference
#  to the memory
mm1 = MM1Processor(memory)


# Show contents of memory before executing the program
print ' '*22+"Memory Dump"
memory.dump()

# Execute instructions until the processor halts (executes a HALT instruction)
instructions=0
while mm1.status is not 'halted' and instructions<max_instructions:
    if DEBUG:
        raw_input() # wait for user to press <Enter>
        mm1.regfile.dump()
    mm1.execute_next_instruction()
    instructions+=1

# Now print the final values of the registers and memory contents
print
print "Register Dump"
mm1.regfile.dump()

print ' '*22+"Memory Dump"
memory.dump()
