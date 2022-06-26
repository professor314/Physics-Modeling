from math import *
deltat = .0001
e = 200000
deltae = -.05*e
t = 1
while e>99999:
    e = e+deltat*deltae
    deltae=-.05*e
    t=t+deltat
print t, e
