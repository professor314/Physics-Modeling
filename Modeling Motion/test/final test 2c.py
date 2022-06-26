from visual.graph import *
from math import *

graph1 = gdisplay(x=0, y=0, width=600, height=800, 
          title='2c', xtitle='time', ytitle='P(t)', 
          xmax=11., xmin=0, ymax=120, ymin=-2)
A = .25
t=0
deltat = .125
line = gcurve(color=color.cyan)
while t<=10:
    function = (100.*A*e**t)/(1.+A*e**t)
    line.plot(pos=(t,function))
    t+=deltat
