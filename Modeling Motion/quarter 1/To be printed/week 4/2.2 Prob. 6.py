from math import *
def function(x):
    return sqrt(1.-(x**2))
xinitial = -1
xfinal = 1
numberofsteps = 2000000
deltax = .01
total = 0
k=0
while k<=numberofsteps:
    x1 = xinitial+(k-1)*deltax
    xr = xinitial+k*deltax
    y1 = (function(x1))
    yr = (function(xr))
    segment = sqrt((xr-x1)**2+(yr-y1)**2)
    total= total+segment
    k+=1
print numberofsteps, total
