from pythonhomework import *

class Decoder:
    def __init__(self,x0,x1,y0,y1,y2,y3):
        x0not = Wire()
        x1not = Wire()

        Inverter(x0,x0not)
        Inverter(x1,x1not)

        AndGate(x0not,x1not,y0)
        AndGate(x0,x1not,y1)
        AndGate(x0not,x1,y2)
        AndGate(x0,x1,y3)

class HalfAdder:
    def __init__(self,A,B,Sum,Carry):
        W0 = Wire()
        W1=Wire()
        OrGate(A,B,W0)
        AndGate(A,B,Carry)
        Inverter(Carry,W1)
        AndGate(W0,W1,Sum)

class FullAdder:
    def __init__(self,A,B,Carry,Sum,Overflow):
        W2=Wire()
        W3=Wire()
        W4=Wire()
        HalfAdder(B,Carry,W2,W3)
        HalfAdder(A,W2,Sum,W4)
        OrGate(W4,W3,Overflow)
A=Wire()
B=Wire()
Sum=Wire()
Carry=Wire()
Overflow = Wire()
fulladder = FullAdder(A,B,Carry,Sum,Overflow)

print A,B,Carry,'   |',Sum,Overflow
A.setto(1)
print A,B,Carry,'   |',Sum,Overflow
A.setto(0)
B.setto(1)
print A,B,Carry,'   |',Sum,Overflow
A.setto(1)
print A,B,Carry,'   |',Sum,Overflow
