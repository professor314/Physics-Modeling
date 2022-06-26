from math import *
from visual.graph import *
graph1 = gdisplay(x=0, y=0, width=600, height=600, 
          title='N vs. t', xtitle='t', ytitle='N', 
          xmax=20., xmin=-20., ymax=1000, ymin=-1000)
last = 10
x=-20
ymin=0
xmin = -2
graph = gcurve(color = color.red)
while x<=last:
    y = (x**4)-(42*x**2)-80*x
    graph.plot(pos=(x,y))
    if y<ymin:
        ymin=y
        xmin = x
    x+=.01
print ymin,xmin
