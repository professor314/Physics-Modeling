from spring import *
from visual import curve

#make a curve to trace the path of the pendulum
curve=curve(radius=.01,color=color.red)


#make a rod for the pendulum to appear to hang from
Rod = cylinder(radius=0.05,length=1,axis=(0,0,-1))

scene.center=(0,-2,0)
scene.range=5


#This class has a spring fixed at one end with a mass attached to the other
pend = SpringPendulum()
pend.theta = 3*pi/4            # angle relative to vertical
pend.velocity = vector(0,0,1) # give an initial push in the z direction
pend.length=2.0                # length pendulum is extended out to
pend.spring.rest_length=2.0    # length the spring tries to be
pend.spring.damping=-.15       # how much friction dampens the motion
pend.spring.k=10.0
pend.bob.mass=1
pend.steps=100 # number of Euler steps between animation frames

# can also set the position of the pendulum's bob like this
# pend.pos=(0,-10,0)


t=0
dt=1.0/16 #time intervals between animation frames

while True:
    # each call to simulate will do pend.steps Euler steps before    
    # updating the position of the pendulum
    pend.simulate(dt) 
    curve.append(pos=pend.pos)
    t += dt
    rate(1/dt)
