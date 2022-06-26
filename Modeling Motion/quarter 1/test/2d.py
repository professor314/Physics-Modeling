from math import *
from visual.graph import *

graph1 = gdisplay(x=0, y=0, width=600, height=600, 
          title='2d', xtitle='t', ytitle='y', 
          xmax=10., xmin=-1., ymax=1000, ymin=-1)
yplot = gcurve(color=color.red)
tinitial = 0
tfinal =10
t=tinitial
y=20    #initial value of y
deltat=.005
while t<=tfinal:
    yprime = (100*e**t)/(1+e**t)
    deltay = deltat*yprime
    yplot.plot(pos=(t,y))
    t=t+deltat
    y=y+deltay

