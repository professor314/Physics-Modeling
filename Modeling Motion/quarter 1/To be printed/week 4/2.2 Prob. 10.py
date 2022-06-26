from math import *
def function(x):
    return x**3.
xinitial = 0
xfinal = 1
numberofsteps = 200
deltax = float(xfinal-xinitial)/numberofsteps
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
