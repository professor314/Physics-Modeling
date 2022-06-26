from visual.graph import *
deltat = .1
x = 52
y = 25
t = 0

while t<10:
    deltax = (-4*x+2*y)*deltat
    deltay = (5*x-4*y+12)*deltat
    x= x + deltax
    y= y +deltay
    t=t+deltat
print t, x, y
