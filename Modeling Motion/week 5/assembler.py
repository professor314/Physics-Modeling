from instructionset import *
import sys

DEBUG=False

def assemble(instruction):
    field = instruction.split()

    address = int(field[0])

    inst=field[1]
    if DEBUG: print "assembling",instruction

    if inst=="DATA":
        return address,int(field[2])

    elif   inst=='ADD':
        opcode=ADD
        src1=int(field[2][1:])
        src2=int(field[3][1:])
        dest=int(field[4][1:])

    elif   inst=='SUB':
        opcode=SUB
        src1=int(field[2][1:])
        src2=int(field[3][1:])
        dest=int(field[4][1:])

    elif inst=='MUL':
        opcode=MUL
        src1=int(field[2][1:])
        src2=int(field[3][1:])
        dest=int(field[4][1:])

    elif inst=='DIV':
        opcode=DIV
        src1=int(field[2][1:])
        src2=int(field[3][1:])
        dest=int(field[4][1:])

    elif inst=='INC':
        opcode=INC
        src1=0
        src2=0
        dest=int(field[2][1:])

    elif inst=='LD' :
        opcode=LD
        loadaddress = int(field[2])
        dest = int(field[3][1:])
        src1 = (loadaddress & (7<<3)) >> 3
        src2 = (loadaddress & 7)

    elif inst=='ST' :
        opcode=ST
        storeaddress = int(field[3])
        src1 = int(field[2][1:])
        src2 = (storeaddress & (7<<3)) >> 3
        dest = (storeaddress & 7)
        
    elif inst=='MOV' :
        opcode=MOV
        src1 = int(field[2][1:])
        src2 = 0
        dest = int(field[3][1:])
        
    elif inst=='JMP':
        opcode=JMP
        src1=0
        src2=int(field[2]) >> 3
        dest  =int(field[2]) & 7

    elif inst=='JZ':
        opcode=JZ
        src1=0
        src2=int(field[2]) >> 3
        dest  =int(field[2]) & 7

    elif inst=='JN':
        opcode=JN
        src1=0
        src2=int(field[2]) >> 3
        dest  =int(field[2]) & 7

    elif inst=='HALT':
        opcode=HALT
        src1=0; src2=0; dest=0

    elif inst=='BRA':
        opcode=BRA

    else:
        print "\nassembler: ERROR - Unrecognized instruction",inst
        sys.exit(0)

    machine_language = opcode<<9 | src1<<6 | src2<<3 | dest

    return address, machine_language

def load_program(filename,memory):
  print "Loading program from '"+filename+"'....",
  program = open(filename,'r')
  address=0
  for line in program:
      # ignore blank lines and comments
      if line[0] != '#' and line[0] != ' ' and line[0] != '\n': 
          if DEBUG: print "instruction:",line
          address,instruction = assemble(line)
          if DEBUG: print "load",address,"with",instruction
          memory.word[address]=instruction # load instruction into memory
  print "Done."
