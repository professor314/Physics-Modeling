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
