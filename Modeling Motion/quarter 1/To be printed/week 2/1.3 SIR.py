t = 0
S = 45400
I = 2100
R = 2500
deltat = -.1
tmax=-3
while t>=tmax:
    Sprime = -.00001*S*I
    Iprime=.00001*S*I-I/14
    Rprime = I/14
    deltaS = Sprime*deltat
    deltaI = Iprime*deltat
    deltaR = Rprime * deltat
    S = S+deltaS
    I = I+deltaI
    R = R+deltaR
    t=t+deltat
print t,S,I,R
