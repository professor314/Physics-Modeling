from visual import *

mything = curve(radius=1)

angle=0;
radius=20;

while angle<=22.1*pi:
    radius = 5+20*cos(13/11.*angle)
    x=radius*cos(angle)
    y=radius*sin(angle)
    z=radius*sin((13/11.)*angle)
    angle = angle + pi/50

    red  =1+sin(pi/2+angle)/2
    green=1+sin(3*pi/2+angle)/2
    blue =1+sin(angle)/2

    mything.append(pos=(x,y,z),color=(red,green,blue))
    rate(120) #control the drawing speed

