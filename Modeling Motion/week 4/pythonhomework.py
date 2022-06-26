DEBUG=False

def debugprint(message):
    if DEBUG: print message

class Wire:
    def __init__(self, initial_value=0,name="unnamed wire"):
        self.name = name
        self.value=initial_value
        self.gates=[]

    def addGate(self,gate):
        self.gates.append(gate)

    def setto(self,signal):
        debugprint( self.name+" set to "+str(signal))
        self.value=signal
        
        for gate in self.gates:
            debugprint( "updating "+self.name)
            gate.update()

    # this allows the wires value to be printed
    def __repr__(self):
        return str(self.value)

class AndGate:
    def __init__(self,a,b,out,name="AND gate"):
        self.a=a
        self.b=b
        a.addGate(self)
        b.addGate(self)
        self.out=out
        self.name=name
        self.update()
        
    def update(self):
        debugprint( self.name+" updating")
        self.out.setto(self.a.value & self.b.value)
class OrGate:
    def __init__(self,a,b,out,name="Or gate"):
        self.a=a
        self.b=b
        a.addGate(self)
        b.addGate(self)
        self.out=out
        self.name=name
        self.update()

    def update(self):
        debugprint( self.name+" updating")
        self.out.setto(self.a.value | self.b.value)

class Inverter:
    def __init__(self,input,out,name="INVERTER"):
        self.input=input
        self.out=out
        input.addGate(self)
        self.name=name
        self.update()

    def update(self):
        debugprint( self.name+" updating")
        self.out.setto( ~self.input.value & 1)

class HalfAdder:
    def __init__(self,A,B,Sum,Carry):
        W0 = Wire()
        W1=Wire()
        OrGate(A,B,W0)
        AndGate(A,B,Carry)
        Inverter(Carry,W1)
        AndGate(W0,W1,Sum)

