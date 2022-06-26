#---------------------------------------------------------
#
# sir-limit.py - A simple differential equation model
#     of a measles-like epidemic.
#     A Python version of the TrueBasic SIR program
#     in "Calculus in Context" by Callahan and Hoffman.
#
# Translated (and commented!) by Barry Tolnas 1/5/04
#                             tolnasb@evergreen.edu
# Modified 1/11/04 by Barry - Added loop to run
#     simulation for several different values of deltat
#     and superimpose the curves to show numerical errors.
#
#---------------------------------------------------------
from visual.graph import *

graph = gdisplay()

for deltat in [5, 4, 3, 2, 1, 0.1, 0.001]:

  t = 0      # time
  S = 45400  # number of susceptibles
  I = 2100   # number infected
  R = 2500   # number recovered

  Scurve = gcurve()
  Icurve = gcurve(color=color.red)
  Rcurve = gcurve(color=color.green)
  Tcurve = gcurve(color=(.7,.7,1)) # total of S+I+R

  #Plot the initial values of S,I and R
  Scurve.plot(pos=(t,S))
  Icurve.plot(pos=(t,I))
  Rcurve.plot(pos=(t,R))
  Tcurve.plot(pos=(t,S+I+R)) #total should remain constant
                             #so we should see a horizontal
  while t<45:                #line at the top.
    #compute rate of change
    Sprime = -.00001 * S * I
    Iprime =  .00001 * S * I - I/14
    Rprime = I/14

    #compute amount of change (deltas)
    deltaS = Sprime * deltat
    deltaI = Iprime * deltat
    deltaR = Rprime * deltat

    #update variables
    t = t + deltat
    S = S + deltaS
    I = I + deltaI
    R = R + deltaR

    #Plot the current values of S,I,R
    
    Scurve.plot(pos=(t,S))
    Icurve.plot(pos=(t,I))
    Rcurve.plot(pos=(t,R))
    Tcurve.plot(pos=(t,S+I+R))
    
