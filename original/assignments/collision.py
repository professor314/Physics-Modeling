# collision.py
from visual import*
from billiards import ball

           
scene.range=30
dt=(1.0/64.0)
t=0

ball1=ball()
ball1.graphic.color=(1,0,0)
ball1.setvelocity(3,0)
ball1.setposition(-10,0)
ball1.graphic.radius=3

ball2=ball()
ball2.graphic.color=(0,1,0)
ball2.setvelocity(-3,0)
ball2.setposition(10,0)
ball1.graphic.radius=1

def interact(b1,b2):
    if b1.graphic.radius+b2.graphic.radius >= abs(b1.position-b2.position):
        b1.collision(b2)
        b2.collision(b1)

while t<10:
    ball1.step(dt)
    ball2.step(dt)
    interact(ball1,ball2)
    rate(2/dt)
    t+=dt
    


