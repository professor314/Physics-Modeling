from visual import *
from math import *

scene.range = 7.5
scene.center = (0,0,0)


homec3= box(pos=(0,2,1), size = (1,1,.01), color = color.red)          #red side
homea1= box(pos=(0,2,4), size = (1,1,.01), color = color.orange)      #green side
homeb5= box(pos=(1,2.5,1.5), size = (1,.01,1), color = color.blue )  #orange side
#homea4= box(pos=(2,-.5,2.5), size = (1,.01,1), color = color.green)  #blue side
#homea5= box(pos=(-.5,2,2.5), size = (.01,1,1), color = color.yellow)#yellow side
#homea6= box(pos=(2.5,2,2.5), size = (.01,1,1), color = color.white) #white side
homeb3= box(pos=(1,2,1), size = (1,1,.01), color = color.red)          #red side
homeb1= box(pos=(1,2,4), size = (1,1,.01), color = color.orange)      #green side
homea5= box(pos=(0,2.5,1.5), size = (1,.01,1), color = color.blue)   #orange side
#homeb4= box(pos=(1,-.5,2.5), size = (1,.01,1), color = color.green)   #blue side
#homeb5= box(pos=(-.5,1,2.5), size = (.01,1,1), color = color.yellow) #yellow side
#homeb6= box(pos=(2.5,1,2.5), size = (.01,1,1), color = color.white)  #white side
homea3= box(pos=(2,2,1), size = (1,1,.01), color = color.red)         #red side
homec1= box(pos=(2,2,4), size = (1,1,.01), color = color.orange)     #green sidehomeg5= box(pos=(2,2.5,1.5), size = (1,.01,1), color = color.blue)  #orange side
homec4= box(pos=(0,-.5,2.5), size = (1,.01,1), color = color.green)   #blue side
#homec5= box(pos=(-.5,0,2.5), size = (.01,1,1), color = color.yellow) #yellow side
#homec6= box(pos=(2.5,0,2.5), size = (.01,1,1), color = color.white)  #white side
homef3= box(pos=(0,1,1), size = (1,1,.01), color = color.red)           #red side
homed1= box(pos=(0,1,4), size = (1,1,.01), color = color.orange)       #green side
homeg5= box(pos=(1,2.5,2.5), size = (1,.01,1), color = color.blue)  #orange side
#homed4= box(pos=(0,-.5,1.5), size = (1,.01,1), color = color.green)    #blue side
#homed5= box(pos=(-.5,1,1.5), size = (.01,1,1), color = color.yellow)  #yellow side
#homed6= box(pos=(2.5,0,1.5), size = (.01,1,1), color = color.white)   #white side
homee3= box(pos=(1,1,1), size = (1,1,.01), color = color.red)           #red side
homee1= box(pos=(1,1,4), size = (1,1,.01), color = color.orange)       #green side
homef5= box(pos=(2,2.5,2.5), size = (1,.01,1), color = color.blue) #orange side
#homee4= box(pos=(1,-.5,1.5), size = (1,.01,1), color = color.green)    #blue side
#homee5= box(pos=(-.5,1,3.5), size = (.01,1,1), color = color.yellow) #yellow side
#homee6= box(pos=(2.5,2,1.5), size = (.01,1,1), color = color.white)  #white side
homed3= box(pos=(2,1,1), size = (1,1,.01), color = color.red)          #red side
homef1= box(pos=(2,1,4), size = (1,1,.01), color = color.orange)      #green side
homed5= box(pos=(0,2.5,2.5), size = (1,.01,1), color = color.blue)  #orange side
#homef4= box(pos=(2,-.5,1.5), size = (1,.01,1), color = color.green)   #blue side
#homef5= box(pos=(-.5,2,3.5), size = (.01,1,1), color = color.yellow)#yellow side
#homef6= box(pos=(2.5,1,1.5), size = (.01,1,1), color = color.white)   #white side
homei3= box(pos=(0,0,1), size = (1,1,.01), color = color.red)          #red side
homeg1= box(pos=(0,0,4), size = (1,1,.01), color = color.orange)       #green side
homei5= box(pos=(2,2.5,3.5), size = (1,.01,1), color = color.blue) #orange side
#homeg4= box(pos=(0,-.5,3.5), size = (1,.01,1), color = color.green)   #blue side
#homeg5= box(pos=(-.5,2,1.5), size = (.01,1,1), color = color.yellow) #yellow side
#homeg6= box(pos=(2.5,0,3.5), size = (.01,1,1), color = color.white)  #white side
homeh3= box(pos=(1,0,1), size = (1,1,.01), color = color.red)          #red side
homeh1= box(pos=(1,0,4), size = (1,1,.01), color = color.orange)       #green side
homeg5= box(pos=(0,2.5,3.5), size = (1,.01,1), color = color.blue)  #orange side
#homeh4= box(pos=(1,-.5,3.5), size = (1,.01,1), color = color.green)   #blue side
#homeh5= box(pos=(-.5,0,1.5), size = (.01,1,1), color = color.yellow)  #yellow side
#homeh6= box(pos=(2.5,1,3.5), size = (.01,1,1), color = color.white)  #white side
homeg3= box(pos=(2,0,1), size = (1,1,.01), color = color.red)         #red side
homei1= box(pos=(2,0,4), size = (1,1,.01), color = color.orange )     #green side
homeh5= box(pos=(1,2.5,3.5), size = (1,.01,1), color = color.blue)  #orange side
#homei4= box(pos=(2,-.5,3.5), size = (1,.01,1), color = color.green)  #blue side
#homei5= box(pos=(-.5,0,3.5), size = (.01,1,1), color = color.yellow) #yellow side
#homei6= box(pos=(2.5,2,3.5), size = (.01,1,1), color = color.white) #white side





#Rename according to hexahedron matricity standard set, change colors so they
#differ by yellow.
#These are all initial values, size and color will stay the same, position
#will change as the following are applied:
if a1.pos!=a3.pos:
    print "yes"
else:
    print "no"
#each of these functions will find the 20 boxes with the given positions and
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
