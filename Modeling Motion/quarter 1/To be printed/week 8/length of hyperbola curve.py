from math import *
from visual import *
deltax = .00001
x=1.
xfinal = 4.
length = 0.
sum = 0.
while x<=xfinal:
    slope = (-1/x**2) #the derivative of 1/x 
    sum =  deltax*sqrt(1+slope**2)#=volume of this disc(cylinder Volume = 1/3*pi*r^3)
    length += sum
    x+=deltax
print length
