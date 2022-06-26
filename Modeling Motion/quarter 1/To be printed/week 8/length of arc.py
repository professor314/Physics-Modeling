from math import *
from visual import *
deltax = .0000001
x=1.
xfinal = 2.
length = 0.
sum = 0.
while x<=xfinal:
    slope = (-2*x)/(2*sqrt(4-x**2)) #the derivative of 1/x 
    sum =  deltax*sqrt(1+(slope**2)) #the length of this small segment
    length += sum
    x+=deltax
print slope,sum,length
