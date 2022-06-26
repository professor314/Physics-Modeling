from math import *


x=1.
sum=0.
upperbound=8000000.

while x<=upperbound:
    sum=sum+(1/float(x**2))
    x=x+1
print sqrt(6.*sum)
