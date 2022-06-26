from math import *
for a in (1,2,3,4):
    upper_bound = a
    lower_bound = 0
    steps = 1000
    accumulation = 0
    numsteps = 100000
    deltax = float((upper_bound - lower_bound))/numsteps
    x = lower_bound
    while x <= a-.0000001:
        deltaS = sqrt(1+x**2)*deltax
        accumulation = accumulation+deltaS
        x += deltax
    print "length=",accumulation,"numsteps=",numsteps,"a=",a,x
