from visual.graph import *
graph1 = gdisplay(x=0, y=0, width=600, height=600, 
          title='Time Vs. Population', xtitle='t', ytitle='Pop',
          xmax=102, xmin=0., ymax=100000000, ymin=0, background = color.white)
PopulationGraph = gcurve(color=color.red)
tinitial = 0
tfinal =100
t = tinitial
P =37500000
numberofsteps =10
deltat=float(tfinal-tinitial)/numberofsteps
t=tinitial
year = 1985+tfinal
PopulationGraph.plot(pos=(t,P))
while t <=tfinal:
    deltaP=.009*P
    P += deltaP*deltat
    t +=deltat
    PopulationGraph.plot(pos=(t,P))
print "population = ", P, "in the year", year
