#!/usr/bin/python
#-------------------------------------------------------
#
# logistic.py - A simple differential equation model
#     of a logistic equation.
#     Translated to Python from the TrueBasic program
#     in "Calculus in Context" by Callahan and Hoffman.
#
# Translated by Barry Tolnas, tolnasb@evergreen.edu
#------------------------------------------------------
from visual.graph import *

tinitial = 0
tfinal   = 75


graph = gdisplay()

for numberofsteps in range(1,11):
    t = tinitial
    y = 100
    deltat = (tfinal - tinitial)/numberofsteps

    ycurve = gcurve(color=(numberofsteps/10.0,0,1-numberofsteps/10.0))

    #print initial values at time 0
    print t, y
    ycurve.plot(pos=(t,y))



    for k in range(numberofsteps):

        #compute rate of change
        yprime = .1*y*(1-y/1000)
       
        #compute amount of change (deltas)
        deltay = yprime*deltat
        
        #update variables
        t = t + deltat
        y = y + deltay
        
        #print out the results for this timestep
        print t,y
        ycurve.plot(pos=(t,y))
