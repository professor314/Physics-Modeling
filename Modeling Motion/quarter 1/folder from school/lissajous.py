#--------------------------------------------------------
# Lissajous.py - Draws a cylindrical Lissajous
#                figure as an example of Visual Python's
#                curve object.
#--------------------------------------------------------
from visual import *

mything = curve(radius=1)
angle=0;
radius=20;

while angle<=18.1*pi:
    x=radius*cos(angle)
    y=radius*sin(angle)
    z=radius*sin((11/9.)*angle)
    angle = angle + pi/10

    red  =1+sin(pi/2+angle)/2
    green=1+sin(3*pi/2+angle)/2
    blue =1+sin(angle)/2

    mything.append(pos=(x,y,z),color=(red,green,blue))
    rate(30) #control the drawing speed
