from visual.graph import *

y0 =  0   # starting position
v0 =  5   # v is velocity in m/s
a  = -1   # a is the acceleration in m/s/s
t  =  0   # starting time in seconds
dt =  .125   # delta t, the change in time

def displacement(t):
    return y0 + v0*t + a*t*t/2.0

graph = gdisplay()
curve = gcurve()

# For a slightly fancier graph replace the above lines with these:
#graph = gdisplay(title="Uniform Acceleration", xtitle="displacement", ytitle="time")
#curve = gcurve(color=(1,1,0))

nextstep = displacement(t)
while nextstep>=0 :
      
      y = nextstep
      nextstep = displacement(t+dt)
      print t,y
      curve.plot(pos=(t,y))
      t = t+dt
