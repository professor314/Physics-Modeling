from math import *
from visual.graph import *
graph1 = gdisplay(x=0, y=0, width=600, height=600, 
          title='N vs. t', xtitle='t', ytitle='N', 
          xmax=50., xmin=-20., ymax=5, ymin=-5)
last = 1000
x=-20
graph = gcurve(color = color.red)
while x<=last:
    y = cos(x)
    graph.plot(pos=(x,y))
    x+=.001
