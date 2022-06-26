from visual import *
from math import *

scene.range = 5
scene.center = (5,0,0)


c3= box(pos=(0,2,1), size = (1,1,.01), color = color.red)          #red side
a1= box(pos=(0,2,4), size = (1,1,.01), color = color.orange)      #green side
#h= box(pos=(5,12.5,7.5), size = (5,.01,5), color = color.blue )  #orange side
#a4= box(pos=(10,-2.5,12.5), size = (5,.01,5), color = color.green)  #blue side
#a5= box(pos=(-2.5,10,12.5), size = (.01,5,5), color = color.yellow)#yellow side
#a6= box(pos=(12.5,10,12.5), size = (.01,5,5), color = color.white) #white side
b3= box(pos=(1,2,1), size = (1,1,.01), color = color.red)          #red side
b1= box(pos=(1,2,4), size = (1,1,.01), color = color.orange)      #green side
#b3= box(pos=(0,12.5,7.5), size = (5,.01,5), color = color.blue)   #orange side
#b4= box(pos=(5,-2.5,12.5), size = (5,.01,5), color = color.green)   #blue side
#b5= box(pos=(-2.5,5,12.5), size = (.01,5,5), color = color.yellow) #yellow side
#b6= box(pos=(12.5,5,12.5), size = (.01,5,5), color = color.white)  #white side
a3= box(pos=(2,2,1), size = (1,1,.01), color = color.red)         #red side
c1= box(pos=(2,2,4), size = (1,1,.01), color = color.orange)     #green side
#c3= box(pos=(10,12.5,7.5), size = (5,.01,5), color = color.blue)  #orange side
#c4= box(pos=(0,-2.5,12.5), size = (5,.01,5), color = color.green)   #blue side
#c5= box(pos=(-2.5,0,12.5), size = (.01,5,5), color = color.yellow) #yellow side
#c6= box(pos=(12.5,0,12.5), size = (.01,5,5), color = color.white)  #white side
f3= box(pos=(0,1,1), size = (1,1,.01), color = color.red)           #red side
d1= box(pos=(0,1,4), size = (1,1,.01), color = color.orange)       #green side
#d3= box(pos=(5,12.5,12.5), size = (5,.01,5), color = color.blue)  #orange side
#d4= box(pos=(0,-2.5,7.5), size = (5,.01,5), color = color.green)    #blue side
#d5= box(pos=(-2.5,5,7.5), size = (.01,5,5), color = color.yellow)  #yellow side
#d6= box(pos=(12.5,0,7.5), size = (.01,5,5), color = color.white)   #white side
e3= box(pos=(1,1,1), size = (1,1,.01), color = color.red)           #red side
e1= box(pos=(1,1,4), size = (1,1,.01), color = color.orange)       #green side
#e3= box(pos=(10,12.5,12.5), size = (5,.01,5), color = color.green) #orange side
#e4= box(pos=(5,-2.5,7.5), size = (5,.01,5), color = color.blue)    #blue side
#e5= box(pos=(-2.5,5,17.5), size = (.01,5,5), color = color.yellow) #yellow side
#e6= box(pos=(12.5,10,7.5), size = (.01,5,5), color = color.white)  #white side
d3= box(pos=(2,1,1), size = (1,1,.01), color = color.red)          #red side
f1= box(pos=(2,1,4), size = (1,1,.01), color = color.orange)      #green side
#f3= box(pos=(0,12.5,12.5), size = (5,.01,5), color = color.green)  #orange side
#f4= box(pos=(10,-2.5,7.5), size = (5,.01,5), color = color.blue)   #blue side
#f5= box(pos=(-2.5,10,17.5), size = (.01,5,5), color = color.yellow)#yellow side
#f6= box(pos=(12.5,5,7.5), size = (.01,5,5), color = color.white)   #white side
i3= box(pos=(0,0,1), size = (1,1,.01), color = color.red)          #red side
g1= box(pos=(0,0,4), size = (1,1,.01), color = color.orange)       #green side
#g3= box(pos=(10,12.5,17.5), size = (5,.01,5), color = color.green) #orange side
#g4= box(pos=(0,-2.5,17.5), size = (5,.01,5), color = color.blue)   #blue side
#g5= box(pos=(-2.5,10,7.5), size = (.01,5,5), color = color.yellow) #yellow side
#g6= box(pos=(12.5,0,17.5), size = (.01,5,5), color = color.white)  #white side
h3= box(pos=(1,0,1), size = (1,1,.01), color = color.red)          #red side
h1= box(pos=(1,0,4), size = (1,1,.01), color = color.orange)       #green side
#h3= box(pos=(0,12.5,17.5), size = (5,.01,5), color = color.green)  #orange side
#h4= box(pos=(5,-2.5,17.5), size = (5,.01,5), color = color.blue)   #blue side
#h5= box(pos=(-2.5,0,7.5), size = (.01,5,5), color = color.yellow)  #yellow side
#h6= box(pos=(12.5,5,17.5), size = (.01,5,5), color = color.white)  #white side
g3= box(pos=(2,0,1), size = (1,1,.01), color = color.red)         #red side
i1= box(pos=(2,0,4), size = (1,1,.01), color = color.orange )     #green side
#i3= box(pos=(5,12.5,17.5), size = (5,.01,5), color = color.green)  #orange side
#i4= box(pos=(10,-2.5,17.5), size = (5,.01,5), color = color.blue)  #blue side
#i5= box(pos=(-2.5,0,17.5), size = (.01,5,5), color = color.yellow) #yellow side
#i6= box(pos=(12.5,10,17.5), size = (.01,5,5), color = color.white) #white side
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
rate=.10
x=1
#have axis of rotation be center of cube on face that is turning,tell all 18 boxes to rotate
#around here pi radians, kind of like: cube.rotate(axis=(0,1,0), angle=cube.dir*cube.dtheta)
#only cubes are called by their position so the funcion will work for any smaller
#box that may be at that position
#def fnf():
    #x = 1
    #y = 1
    #z = 1
    #while x<20:
        #z = z+x
        #a1 =(pos = (x,y,z))
        #x = x+1
        #y=y+1
#fnf()
#object.rotate(angle=pi/4., axis=axis, origin=pos)
