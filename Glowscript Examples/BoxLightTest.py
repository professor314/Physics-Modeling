from vpython import *
#Web VPython 3.2

# Mikhail Temkine, University of Toronto, April 2007
# Updated January 2022 to use attach_light

scene.forward = vector(-0.4,-0.3,-1)
r = 3
a1 = a2 = a3 = 0.0

arrow(pos=vector(0, 4, 0), axis=vector(0, 1, 0), color=color.red)
boxy = box(size=vector(3,3,3), color=vector(0.5, 0.5, 0.5), texture=textures.rough)
b1 = sphere(radius=0.3, pos=vector(r, 0, 0), color=color.magenta, emissive=True)
b2 = sphere(radius=0.3, pos=vector(0, 0, r), color=color.yellow, emissive=True)
b3 = arrow(radius=0.3, pos=vector(0, 0, r), color=color.green, emissive=True)
attach_light(b1)
attach_light(b2)
dist = distant_light(direction=b3.pos, color=b3.color)

while True:
    rate(100)
    b1.pos = r*vector(cos(a1), sin(a1), b1.pos.z)
    a1 += 0.02
    b2.pos = (r+0.4)*vector(b2.pos.x, sin(a2), cos(a2))
    a2 += 0.055
    dist.direction = b3.pos = (r+3)*vector(sin(a3), b3.pos.y, cos(a3))
    b3.axis = b3.pos * -0.3
    a3 += 0.033