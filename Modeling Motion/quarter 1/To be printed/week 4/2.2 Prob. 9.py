from math import *
def function(x):
    return x**2.
xinitial = 0
xfinal = 10000
numberofsteps = 200000
deltax = float(xfinal-xinitial)/numberofsteps
total = 0
k=0
while total<=10.000:
    x1 = xinitial+(k-1)*deltax
    xr = xinitial+k*deltax
    y1 = (function(x1))
    yr = (function(xr))
    segment = sqrt((xr-x1)**2+(yr-y1)**2)
    total= total+segment
    k+=1
print xr,yr,total
