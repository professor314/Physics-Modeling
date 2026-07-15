from visual.graph import *

a = gcurve(color=color.blue)
b = gcurve(color=color.red)
c= gcurve(color=color.green)

avalue=1000
bvalue=0
pheta=0
phetamax=100
deltavalue = 2
b.plot(pos=(pheta,bvalue))
a.plot(pos=(pheta,avalue))
c.plot(pos=(pheta,avalue+bvalue))
while bvalue<=1000:
    pheta=pheta+pi/32
    bvalue=deltavalue*pheta+bvalue
    avalue=avalue-deltavalue*pheta
    b.plot(pos=(pheta,bvalue))
    a.plot(pos=(pheta,avalue))
    c.plot(pos=(pheta,avalue+bvalue))
    
    
