
from math import *
##    print "type in the function you want to find the integral of"
##    function = raw_input()
##    print "type in the lower bound"
##    lower_bound = input()
##    print "type in the upper bound"
##    upper_bound = input()
##    print "type in the number of steps you wish to use"
##    numsteps = input()
##    if numsteps ==0:
##        print "you don't know what you are doing, type in something else"
##        numsteps = input()
##deltax = float((upper_bound - lower_bound))/numsteps
##    x = lower_bound
##    accumulation = 0
##    while x <= upper_bound:
##        deltaS = eval(function)*deltax
##        accumulation = accumulation+deltaS
##        x += deltax
##    print "area = ",accumulation

upper_bound = 3
lower_bound = 1
steps = 1000
accumulation = 0
numsteps = 40000

deltax = float((upper_bound - lower_bound))/numsteps
x = lower_bound+deltax/2
while x <= upper_bound:
    deltaS = sqrt(x**3+1)*deltax
    accumulation = accumulation+deltaS
    x += deltax
print "area = ",accumulation, "numsteps = ", numsteps
