#-------------------------------------------------------
#
# sir.py - A simple differential equation model
#     of a measles-like epidemic.
#     Translated from the TrueBasic SIR program
#     in "Calculus in Context" by Callahan and Hoffman.
#
# Translated by Barry Tolnas, tolnasb@evergreen.edu
#------------------------------------------------------

t = 0      # time
S = 45400  # number of susceptibles
I = 2100   # number infected
R = 2500   # number recovered
deltat = 1 # time interval in days

#print initial values at time 0
print t, S, I, R

for k in [1,2,3]:

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

    #print out the results for this timestep
    print t, S, I, R
    
    
