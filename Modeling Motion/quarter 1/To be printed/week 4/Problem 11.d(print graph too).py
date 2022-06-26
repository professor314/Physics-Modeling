from math import *
from visual.graph import *
graph1 = gdisplay(x=0, y=0, width=600, height=600, background = color.white)
curve = gcurve(color=color.red)

for j in range(1,10):
    tinitial = 0
    tfinal =10
    t = tinitial
    y = 9
    numberofsteps = 2**(j-1)
    deltat = (tfinal-tinitial)/float(numberofsteps)
    curve.plot(pos=(t,y))
    for k in range(numberofsteps):
       yprime = .2*y*(5-y)
       deltay = yprime*deltat
       curve.plot(pos=(t,y))
       t=t+deltat
       y=y+deltay
    yprime=round(y,5)
    print y, yprime, t
               
