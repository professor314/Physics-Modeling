from digital import *

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

        


x0=Wire()
x1=Wire()
y0=Wire()
y1=Wire()
y2=Wire()
y3=Wire()

decoder = Decoder(x0,x1,y0,y1,y2,y3)

print "Inputs | Outputs"
print x0,x1,'   |',y3,y2,y1,y0
x0.setto(1)
print x0,x1,'   |',y3,y2,y1,y0
x0.setto(0)
x1.setto(1)
print x0,x1,'   |',y3,y2,y1,y0
x0.setto(1)
print x0,x1,'   |',y3,y2,y1,y0
