from math import *
from visual.graph import *
graph1 = gdisplay(x=0, y=0, width=600, height=600)
curve = gcurve(color=color.red)

for j in range(1,10):
    tinitial = 0
    tfinal =1
    t = tinitial
    y = 0
    numberofsteps = 2**(j-1)
    deltat = (tfinal-tinitial)/float(numberofsteps)
    curve.plot(pos=(t,y))
    for k in range(numberofsteps):
       yprime = 4/(1+t**2)
       deltay = yprime*deltat
       curve.plot(pos=(t,y))
       t=t+deltat
       y=y+deltay
    yprime=round(y,5)
    print y, yprime, t
               
