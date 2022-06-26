from math import *
from visual import *
deltax = .0001
x=0.
xfinal = 6.
Volume = 0.
sum = 0.
while x<=xfinal:
    r =(.5*x)
    sum = r**2*pi*deltax #=volume of this disc(cylinder Volume = 1/3*pi*r^3)
    Volume += sum
    x+=deltax
    print Volume,x,r
