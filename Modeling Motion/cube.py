from visual import *
from math import *

scene.range = 30
scene.center = (5,0,0)


a1= box(pos=(0,10,5), size = (5,5,.01), color = color.red) #red side
a2= box(pos=(0,10,20), size = (5,5,.01), color = color.green) #green side
a3= box(pos=(5,12.5,7.5), size = (5,.01,5), color = color.orange) #orange side
a4= box(pos=(10,-2.5,12.5), size = (5,.01,5), color = color.red) #blue side
a5= box(pos=(-2.5,10,12.5), size = (.01,5,5), color = color.yellow) #yellow side
a6= box(pos=(12.5,10,12.5), size = (.01,5,5), color = color.white) #white side
b1= box(pos=(5,10,5), size = (5,5,.01), color = color.blue) #red side
b2= box(pos=(5,10,20), size = (5,5,.01), color = color.green) #green side
b3= box(pos=(0,12.5,7.5), size = (5,.01,5), color = color.orange)#orange side
b4= box(pos=(5,-2.5,12.5), size = (5,.01,5), color = color.red)#blue side
b5= box(pos=(-2.5,5,12.5), size = (.01,5,5), color = color.yellow)#yellow side
b6= box(pos=(12.5,5,12.5), size = (.01,5,5), color = color.white)#white side
c1= box(pos=(10,10,5), size = (5,5,.01), color = color.blue) #red side
c2= box(pos=(10,10,20), size = (5,5,.01), color = color.green) #green side
c3= box(pos=(10,12.5,7.5), size = (5,.01,5), color = color.orange)#orange side
c4= box(pos=(0,-2.5,12.5), size = (5,.01,5), color = color.red)#blue side
c5= box(pos=(-2.5,0,12.5), size = (.01,5,5), color = color.yellow)#yellow side
c6= box(pos=(12.5,0,12.5), size = (.01,5,5), color = color.white)#white side
d1= box(pos=(0,5,5), size = (5,5,.01), color = color.red) #red side
d2= box(pos=(0,5,20), size = (5,5,.01), color = color.green) #green side
d3= box(pos=(5,12.5,12.5), size = (5,.01,5), color = color.orange)#orange side
d4= box(pos=(0,-2.5,7.5), size = (5,.01,5), color = color.red)#blue side
d5= box(pos=(-2.5,5,7.5), size = (.01,5,5), color = color.yellow)#yellow side
d6= box(pos=(12.5,0,7.5), size = (.01,5,5), color = color.white)#white side
e1= box(pos=(5,5,5), size = (5,5,.01), color = color.red) #red side
e2= box(pos=(5,5,20), size = (5,5,.01), color = color.green) #green side
e3= box(pos=(10,12.5,12.5), size = (5,.01,5), color = color.orange)#orange side
e4= box(pos=(5,-2.5,7.5), size = (5,.01,5), color = color.red)#blue side
e5= box(pos=(-2.5,5,17.5), size = (.01,5,5), color = color.yellow)#yellow side
e6= box(pos=(12.5,10,7.5), size = (.01,5,5), color = color.white)#white side
f1= box(pos=(10,5,5), size = (5,5,.01), color = color.red) #red side
f2= box(pos=(10,5,20), size = (5,5,.01), color = color.green) #green side
f3= box(pos=(0,12.5,12.5), size = (5,.01,5), color = color.orange)#orange side
f4= box(pos=(10,-2.5,7.5), size = (5,.01,5), color = color.red)#blue side
f5= box(pos=(-2.5,10,17.5), size = (.01,5,5), color = color.yellow)#yellow side
f6= box(pos=(12.5,5,7.5), size = (.01,5,5), color = color.white)#white side
g1= box(pos=(0,0,5), size = (5,5,.01), color = color.red) #red side
g2= box(pos=(0,0,20), size = (5,5,.01), color = color.green) #green side
g3= box(pos=(10,12.5,17.5), size = (5,.01,5), color = color.orange)#orange side
g4= box(pos=(0,-2.5,17.5), size = (5,.01,5), color = color.red)#blue side
g5= box(pos=(-2.5,10,7.5), size = (.01,5,5), color = color.yellow)#yellow side
g6= box(pos=(12.5,0,17.5), size = (.01,5,5), color = color.white)#white side
h1= box(pos=(5,0,5), size = (5,5,.01), color = color.red) #red side
h2= box(pos=(5,0,20), size = (5,5,.01), color = color.green) #green side
h3= box(pos=(0,12.5,17.5), size = (5,.01,5), color = color.orange)#orange side
h4= box(pos=(5,-2.5,17.5), size = (5,.01,5), color = color.red)#blue side
h5= box(pos=(-2.5,0,7.5), size = (.01,5,5), color = color.yellow)#yellow side
h6= box(pos=(12.5,5,17.5), size = (.01,5,5), color = color.white)#white side
i1= box(pos=(10,0,5), size = (5,5,.01), color = color.red) #red side
i2= box(pos=(10,0,20), size = (5,5,.01), color = color.green, ) #green side
i3= box(pos=(5,12.5,17.5), size = (5,.01,5), color = color.orange)#orange side
i4= box(pos=(10,-2.5,17.5), size = (5,.01,5), color = color.red)#blue side
i5= box(pos=(-2.5,0,17.5), size = (.01,5,5), color = color.yellow)#yellow side
i6= box(pos=(12.5,10,17.5), size = (.01,5,5), color = color.white)#white side
#Rename according to hexahedron matricity standard set, change colors so they
#differ by yellow.
#These are all initial values, size and color will stay the same, position
#will change as the following are applied:

#each of these functions will find the 18 boxes with the given positions and
#then change their positions accordingly following the trace of a circle in a
#particular direction

#def rightdown()
#def centerdown()
#def leftdown()
#def backcounterclockwise() #counter-clockwise looking at back face
#def centerrightcounterclockwise() #counter-clockwise looking through front face
#def frontcentercounterclockwise()
#def topcounterclockwise()
#def frontcentercounterclockwise() #center functions not needed.(centerup=left and right down
#def bottomcounterclockwise()


#have axis of rotation be center of cube on face that is turning,tell all 18 boxes to rotate
#around here pi radians, kind of like: cube.rotate(axis=(0,1,0), angle=cube.dir*cube.dtheta)
#only cubes are called by their position so the funcion will work for any smaller
#box that may be at that position




