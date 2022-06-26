from math import *
from visual.graph import *
for j in range(1,19):
    tinitial = 0
    tfinal =37
    t = tinitial
    y = 1500
    numberofsteps = 2**(j-1)
    deltat = (tfinal-tinitial)/float(numberofsteps)
    for k in range(numberofsteps):
       yprime = .1*y*(1-y/1000.0)
       deltay = yprime*deltat
       t=t+deltat
       y=y+deltay
    yprime=round(y,5)
    print y, yprime
               
