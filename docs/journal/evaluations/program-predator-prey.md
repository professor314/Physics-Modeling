---
title: "Predator-Prey Simulation (Lotka-Volterra)"
author: Sean Connolly
date: 2004
course: Modeling Motion
original_file: program.rtf
notes: "A predator-prey (rabbits and foxes) simulation using Euler's method. This appears to be a test or homework submission printed to RTF."
---

# Predator-Prey Simulation (Lotka-Volterra)

This program models a predator-prey relationship between rabbits and foxes using the Lotka-Volterra equations solved with Euler's method.

```python
#This is my program:

r=150
f=10
a=.6
b=-.04
c=-.2
d=.002
rprime=(a+b*f)*r
fprime=(c+d*r)*f
t=0
finalt = 20
deltat=.0001
rnew =0
fnew= 0
rmax=r
fmax=f
rmin=0
fmin=0
##deltatlist = [1,.1,.01,.001,.0001,.00001,.000001,.0000001]
##deltat=deltatlist[0]
##n=0
##
##while deltatlist[n]!=deltatlist[7]: 
while t < finalt:
    rnew=r+rprime*deltat
    fnew=f+fprime*deltat
    if rnew>=r:
        rmax = rnew
    if fnew >= f:
        fmax =fnew
    if rnew<=r:
        rmin=rnew
    if fnew<=f:
        fmin=fnew
    r = rnew
    f = fnew
    t=t+deltat
    rprime = (a+(b*f))*r
    fprime = (c+(d*r))*f
    
##n=n+1
##deltat=deltatlist[n]
print "rabbits =", r,",", "foxes =", f,",", "time = ", t, "deltat =", deltat, rmax, fmax, rmin, fmin
```

> *See also: [original/assignments/](../../original/assignments/) for related simulations.*
