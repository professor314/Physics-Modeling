from  instructionset import *

# Turn on debug log
DEBUG = False
LOGINSTRUCTIONS=True
LOGDECODE=False
LOGREGISTERS=False
LOGALU=False

class ALU:
    def __init__(self):
        self.A=0
        self.B=0
        self.opcode=ADD
        self.output=0
        self.zero=1 # the zero flag is one whenever output is zero
        self.sign=0 # the sign flag is one whenever output is negative

    def evaluate(self):
        A = self.A; B=self.B
        if   self.opcode==ADD: self.output = A+B
        elif self.opcode==SUB: self.output = A-B
        elif self.opcode==MUL: self.output = A*B
        elif self.opcode==DIV: self.output = A/B

        #set the zero flag
        if self.output==0:
            self.zero = 1
            if DEBUG: print "ALU: setting zero flag"
        else:
            if DEBUG and self.zero==1: print "ALU: clearing zero flag"
            self.zero = 0

        #set the sign flag
        if self.output<0:
            self.sign = 1
            if DEBUG: print "ALU: setting sign flag"
        else:
            if DEBUG and self.sign==1: print "ALU: clearing sign flag"
            self.sign = 0


class Sequencer:
    def __init__(self,regfile,alu,memory):
        self.regfile = regfile
        self.alu = alu
        self.memory = memory
        self.program_counter=0
        self.status='ready'
        self.src1=0
        self.src2=0
        self.dest=0

    def fetch(self):
        if LOGINSTRUCTIONS: print "sequencer: Program Counter = -----> %2d <------" %self.program_counter
        self.memory.address = self.program_counter
        self.memory.read()
        self.instruction = self.memory.data
        self.program_counter+=1

    def decode(self):
        self.opcode = (self.instruction & OPCODE_MASK) >> 9 #mask off opcode bits

        if self.opcode==JZ or self.opcode==JMP or self.opcode==JN:
            self.dest   = (self.instruction & JUMP_DEST_MASK)

        elif self.opcode==LD:
            self.src1   = (self.instruction & LD_SRC_MASK) >> 3
            self.dest   = (self.instruction & DEST_MASK  )      #mask off DEST bits

        elif self.opcode==ST:
            self.src1   = (self.instruction & SRC1_MASK  ) >> 6 #mask off SRC1 bits
            self.dest   = (self.instruction & ST_DEST_MASK)

        else: # all other instructions
            self.src1   = (self.instruction & SRC1_MASK  ) >> 6 #mask off SRC1 bits
            self.src2   = (self.instruction & SRC2_MASK  ) >> 3 #mask off SRC2 bits
            self.dest   = (self.instruction & DEST_MASK  )      #mask off DEST bits

        if LOGDECODE: print "sequencer: decode",self.instruction,"->",self.opcode,self.src1,self.src2,self.dest


    def execute(self):
        if   self.opcode==LD:   self.doload()
        elif self.opcode==ST:   self.dostore()
        elif self.opcode==MOV:  self.domove()
        elif self.opcode==ADD:  self.doadd()
        elif self.opcode==SUB:  self.dosubtract()
        elif self.opcode==MUL:  self.domultiply()
        elif self.opcode==DIV:  self.dodivide()
        elif self.opcode==INC:  self.doincrement()
        elif self.opcode==JMP:  self.dojump()
        elif self.opcode==JZ:   self.dojumpifzero()
        elif self.opcode==JN:   self.dojumpifnegative()
        elif self.opcode==HALT: self.dohalt()

    def doload(self):
        #combine src1 and src2 to get memory address to load from
        self.memory.address = self.src1
        self.memory.read()

        if LOGINSTRUCTIONS: print "sequencer: loading",self.memory.data,"to reg"+str(self.dest)

        #store the data in the destination register
        self.regfile.write(self.dest,self.memory.data)

    def dostore(self):
        #combine src2 and dest to get memory address to store to
        self.memory.address = self.dest
        if LOGINSTRUCTIONS: print "sequencer: storing", self.regfile.read(self.src1),\
                                  "at address",self.memory.address
        self.memory.data = self.regfile.read(self.src1)
        self.memory.write()

    def domove(self):
        if LOGINSTRUCTIONS: print "sequencer: moving r"+str(self.src1)+" to r"+str(self.dest)
        value = self.regfile.read(self.src1)
        self.regfile.write(self.dest,value)

    def doadd(self):
        self.alu.A = self.regfile.read(self.src1)
        self.alu.B = self.regfile.read(self.src2)
        if LOGINSTRUCTIONS: print "sequencer: adding",self.alu.A,"+",self.alu.B
        self.alu.opcode = ADD
        self.alu.evaluate()
        self.regfile.write(self.dest,self.alu.output)

    def dosubtract(self):
        self.alu.A = self.regfile.read(self.src1)
        self.alu.B = self.regfile.read(self.src2)
        if LOGINSTRUCTIONS: print "sequencer: subtracting",self.alu.A,"-",self.alu.B
        self.alu.opcode = SUB
        self.alu.evaluate()
        self.regfile.write(self.dest,self.alu.output)

    def dodivide(self):
        if LOGINSTRUCTIONS: print "sequencer: dividing"
        self.alu.A = self.regfile.read(self.src1)
        self.alu.B = self.regfile.read(self.src2)
        self.alu.opcode = DIV
        self.alu.evaluate()
        self.regfile.write(self.dest,self.alu.output)

    def doincrement(self):
        if LOGINSTRUCTIONS: print "sequencer: incrementing r"+str(self.dest)
        self.alu.A = self.regfile.read(self.dest)
        self.alu.B = 1
        self.alu.opcode = ADD
        self.alu.evaluate()
        self.regfile.write(self.dest,self.alu.output)
        
    def domultiply(self):
        if LOGINSTRUCTIONS: print "sequencer: multiplying"
        self.alu.A = self.regfile.read(self.src1)
        self.alu.B = self.regfile.read(self.src2)
        self.alu.opcode = MUL
        self.alu.evaluate()
        self.regfile.write(self.dest,self.alu.output)

    def dojump(self):
        if LOGINSTRUCTIONS: print "sequencer: jumping to",self.dest
        self.program_counter=self.dest

    def dojumpifzero(self):
        if self.alu.zero:
            if LOGINSTRUCTIONS: print "sequencer: jump on zero to",self.dest
            self.program_counter=self.dest
        else: 
            if LOGINSTRUCTIONS: print "sequencer: jump if zero failed"
            
    def dojumpifnegative(self):
        if self.alu.sign:
            if LOGINSTRUCTIONS: print "sequencer: jump if negative to",self.dest
            self.program_counter=self.dest
        else: 
            if LOGINSTRUCTIONS: print "sequencer: jump if negative failed"
            
    def dohalt(self):
        if LOGINSTRUCTIONS: print "sequencer: halting"
        self.status='halted'
             
class RegisterFile:
    def __init__(self,size):
        self.register = [0]*size
        self.size = size

    def read(self,index):
        if LOGREGISTERS: print "regfile: read reg"+str(index)+"=="+str(self.register[index])
        if index<0 or index >=self.size:
            print "register file: READ ERROR, invalid register number",index,"*************"
        return self.register[index]

    def write(self,index,value):
        if LOGREGISTERS: print "regfile: wrote reg"+str(index)+"="+str(value)
        if index<0 or index >=self.size:
            print "register file: WRITE ERROR, invalid register number",index,"*************"
        self.register[index] = value

    def dump(self):
        for i in range(len(self.register)):
            print "%2d %5d" % (i,self.register[i])


class Memory:
    def __init__(self,size):
        self.word = [0]*size # one element for each memory location
        self.address=0
        self.data=0


    def write(self):
        self.word[self.address]=self.data

    def read(self):
        self.data =  self.word[self.address]

    def dump(self):
    	width = 8

	#print header (column addresses)
	print "    ",
        for col in range(width):
	    print "%5d" % col,
	print

	print '-'*55

	address=0
	for row in range(width):
	    print "%02d |" % int(row*width),
	    for col in range(width):
	    	print "%5d" % self.word[address],
		address += 1
	    print            

class MM1Processor:
    def __init__(self,memory):
        self.memory    = memory
        self.regfile   = RegisterFile(8)
        self.alu       = ALU()
        self.sequencer = Sequencer(self.regfile,self.alu,self.memory)
        self.status    = self.sequencer.status

    def execute_next_instruction(self):
        self.sequencer.fetch()
        self.sequencer.decode()
        self.sequencer.execute()
        self.status = self.sequencer.status
        
    def reset(self):
        self.status = 'ready'
        self.sequencer.status='ready'
