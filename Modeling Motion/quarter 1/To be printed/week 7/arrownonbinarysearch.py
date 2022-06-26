from visual import *
from random import *
from visual.graph import *
graph=gdisplay()
errorg=gcurve(color=color.red)

myarrow = arrow(shaftwidth=0.01,length=5,color=color.red)
ground  = box(size=(50,.1,200),pos=(0,-.05,50),color=color.green)
target  = ring(pos=(0,1,100),radius=1,axis=(0,0,-1),thickness=.5,color=(1,1,0))

numblocks=20
width=target.pos.z/numblocks
for i in range(numblocks):
    z=i*target.pos.z/numblocks
    box(size=(width,.1,width),pos=(0,.01,z),axis=(1,0,1),color=(z/target.pos.z,1-z/target.pos.z,1))

scene.center=(myarrow.pos+target.pos)/2.0
scene.forward=(.1,0,1)
scene.range=3
scene.lights=[norm(vector(-1,1,-1))]


def distance(p1,p2):
    return mag(p1-p2)

def collision(torus,point):
    if mag(torus.pos-point)<torus.radius:
        if point.z>=torus.z:
            if (point.x-torus.pos.x)**2+(point.y-torus.pos.y)**2 < torus.radius**2:
                return True
    return False

def fire(arrow,v0,phi,theta):
    vx=0
    vy=v0*sin(phi)
    vz=v0*cos(phi)*sin(theta)
    v=vector(vx,vy,vz)
    arrow.axis=norm(v)

    dt=1.0/128
    a=vector(0,-9.8,0)
    arrow.point = arrow.pos+arrow.axis
    while arrow.point.y>=0 and not collision(target,arrow.point):
        v = v + a*dt
        arrow.pos += v*dt
        arrow.axis=norm(v)*5
        scene.center=arrow.pos
        arrow.point = arrow.pos+arrow.axis
        rate(100)

    

error=distance(target.pos,myarrow.pos+myarrow.axis)
v0=50


#60, .148
phi_upper=.3
phi_lower=0
phi=.25
theta=pi/2
theta_upper=pi
theta_lower=0
tries=0


while error >.1:
    tries +=1
    myarrow.pos=(0,0,0)
    fire(myarrow,v0,phi,theta)
    point = myarrow.point
    error=distance(target.pos,point)
    phi-=error*.0015

    print tries,phi,v0,error
    errorg.plot(pos=(tries,error))

