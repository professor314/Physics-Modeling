from visual import *
from math import *

scene.range = 6
scene.center = (0,0,0)
debug = true

#side 1:
a1= box(pos=(0,2,4), size = (1,1,.01), color = color.orange) 
b1= box(pos=(1,2,4), size = (1,1,.01), color = color.orange)     
c1= box(pos=(2,2,4), size = (1,1,.01), color = color.orange)
d1= box(pos=(0,1,4), size = (1,1,.01), color = color.orange)
e1= box(pos=(1,1,4), size = (1,1,.01), color = color.orange)
f1= box(pos=(2,1,4), size = (1,1,.01), color = color.orange)
g1= box(pos=(0,0,4), size = (1,1,.01), color = color.orange)     
h1= box(pos=(1,0,4), size = (1,1,.01), color = color.orange)    
i1= box(pos=(2,0,4), size = (1,1,.01), color = color.orange)
#side 2:
a2= box(pos=(2.5,2,3.5), size = (.01,1,1), color = color.white) 
b2= box(pos=(2.5,2,2.5), size = (.01,1,1), color = color.white)
c2= box(pos=(2.5,2,1.5), size = (.01,1,1), color = color.white)
d2= box(pos=(2.5,1,3.5), size = (.01,1,1), color = color.white)
e2= box(pos=(2.5,1,2.5), size = (.01,1,1), color = color.white)
f2= box(pos=(2.5,1,1.5), size = (.01,1,1), color = color.white)
g2= box(pos=(2.5,0,3.5), size = (.01,1,1), color = color.white)
h2= box(pos=(2.5,0,2.5), size = (.01,1,1), color = color.white)
i2= box(pos=(2.5,0,1.5), size = (.01,1,1), color = color.white)
#side 3:
a3= box(pos=(2,2,1), size = (1,1,.01), color = color.red)     
b3= box(pos=(1,2,1), size = (1,1,.01), color = color.red)          
c3= box(pos=(0,2,1), size = (1,1,.01), color = color.red)          
d3= box(pos=(2,1,1), size = (1,1,.01), color = color.red)       
e3= box(pos=(1,1,1), size = (1,1,.01), color = color.red)       
f3= box(pos=(0,1,1), size = (1,1,.01), color = color.red)
g3= box(pos=(2,0,1), size = (1,1,.01), color = color.red)       
h3= box(pos=(1,0,1), size = (1,1,.01), color = color.red)          
i3= box(pos=(0,0,1), size = (1,1,.01), color = color.red)   
#side 4:
a4= box(pos=(-.5,2,1.5), size = (.01,1,1), color = color.yellow) 
b4= box(pos=(-.5,2,2.5), size = (.01,1,1), color = color.yellow)
c4= box(pos=(-.5,2,3.5), size = (.01,1,1), color = color.yellow)
d4= box(pos=(-.5,1,1.5), size = (.01,1,1), color = color.yellow)
e4= box(pos=(-.5,1,2.5), size = (.01,1,1), color = color.yellow) 
f4= box(pos=(-.5,1,3.5), size = (.01,1,1), color = color.yellow)
g4 = box(pos=(-.5,0,1.5), size = (.01,1,1), color = color.yellow)
h4= box(pos=(-.5,0,2.5), size = (.01,1,1), color = color.yellow) 
i4= box(pos=(-.5,0,3.5), size = (.01,1,1), color = color.yellow)
#side 5:
a5= box(pos=(0,2.5,1.5), size = (1,.01,1), color = color.blue) 
b5= box(pos=(1,2.5,1.5), size = (1,.01,1), color = color.blue) 
c5= box(pos=(2,2.5,1.5), size = (1,.01,1), color = color.blue) 
d5= box(pos=(0,2.5,2.5), size = (1,.01,1), color = color.blue)
e5= box(pos=(1,2.5,2.5), size = (1,.01,1), color = color.blue)
f5= box(pos=(2,2.5,2.5), size = (1,.01,1), color = color.blue) 
g5= box(pos=(0,2.5,3.5), size = (1,.01,1), color = color.blue)  
h5= box(pos=(1,2.5,3.5), size = (1,.01,1), color = color.blue)
i5= box(pos=(2,2.5,3.5), size = (1,.01,1), color = color.blue)
#side 6:
a6= box(pos=(0,-.5,3.5), size = (1,.01,1), color = color.green)
b6= box(pos=(1,-.5,3.5), size = (1,.01,1), color = color.green)
c6= box(pos=(2,-.5,3.5), size = (1,.01,1), color = color.green) 
d6= box(pos=(0,-.5,2.5), size = (1,.01,1), color = color.green)
e6= box(pos=(1,-.5,2.5), size = (1,.01,1), color = color.green)
f6= box(pos=(2,-.5,2.5), size = (1,.01,1), color = color.green) 
g6= box(pos=(0,-.5,1.5), size = (1,.01,1), color = color.green)
h6= box(pos=(1,-.5,1.5), size = (1,.01,1), color = color.green) 
i6= box(pos=(2,-.5,1.5), size = (1,.01,1), color = color.green)
facelets = (a1,a2,a3,a4,a5,a6,b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,c6,d1,d2,d3,d4,d5,d6,e1,e2,e3,e4,e5,e6,f1,f2,f3,f4,f5,f6,g1,g2,g3,g4,g5,g6,h1,h2,h3,h4,h5,h6,i1,i2,i3,i4,i5,i6)
#colors:
#orange side:
ca1= color.orange
cb1= color.orange    
cc1= color.orange
cd1= color.orange
ce1= color.orange
cf1= color.orange
cg1= color.orange    
ch1= color.orange    
ci1= color.orange
#white side:
ca2= color.white 
cb2= color.white
cc2= color.white
cd2= color.white
ce2= color.white
cf2= color.white
cg2= color.white
ch2= color.white
ci2= color.white
#red side:
ca3= color.red     
cb3= color.red          
cc3= color.red          
cd3= color.red       
ce3= color.red       
cf3= color.red
cg3= color.red       
ch3= color.red          
ci3= color.red   
#yellow side:
ca4= color.yellow 
cb4= color.yellow
cc4= color.yellow
cd4= color.yellow
ce4= color.yellow 
cf4= color.yellow
cg4= color.yellow
ch4= color.yellow
ci4= color.yellow
#blue side:
ca5= color.blue 
cb5= color.blue 
cc5= color.blue 
cd5= color.blue
ce5= color.blue
cf5= color.blue 
cg5= color.blue  
ch5= color.blue
ci5= color.blue
#side 6:
ca6= color.green
cb6= color.green
cc6= color.green 
cd6= color.green
ce6= color.green
cf6= color.green 
cg6= color.green
ch6= color.green 
ci6= color.green
colors = (ca1,ca2,ca3,ca4,ca5,ca6,cb1,cb2,cb3,cb4,cb5,cb6,cc1,cc2,cc3,cc4,cc5,cc6,cd1,cd2,cd3,cd4,cd5,cd6,ce1,ce2,ce3,ce4,ce5,ce6,cf1,cf2,cf3,cf4,cf5,cf6,cg1,cg2,cg3,cg4,cg5,cg6,ch1,ch2,ch3,ch4,ch5,ch6,ci1,ci2,ci3,ci4,ci5,ci6)
#positions:
#side 1:
pa1= [0,2,4]
pb1= [1,2,4]    
pc1= [2,2,4]
pd1= [0,1,4]
pe1= [1,1,4]
pf1= [2,1,4]
pg1= [0,0,4]     
ph1= [1,0,4]    
pi1= [2,0,4]
#side 2:
pa2= [2.5,2,3.5] 
pb2= [2.5,2,2.5]
pc2= [2.5,2,1.5]
pd2= [2.5,1,3.5]
pe2= [2.5,1,2.5]
pf2= [2.5,1,1.5]
pg2= [2.5,0,3.5]
ph2= [2.5,0,2.5]
pi2= [2.5,0,1.5]
#side 3:
pa3= [2,2,1]     
pb3= [1,2,1]          
pc3= [0,2,1]          
pd3= [2,1,1]       
pe3= [1,1,1]       
pf3= [0,1,1]
pg3= [2,0,1]       
ph3= [1,0,1]          
pi3= [0,0,1]   
#side 4:
pa4= [-.5,2,1.5]
pb4= [-.5,2,2.5]
pc4= [-.5,2,3.5]
pd4= [-.5,1,1.5]
pe4= [-.5,1,2.5] 
pf4= [-.5,1,3.5]
pg4= [-.5,0,1.5]
ph4= [-.5,0,2.5]
pi4= [-.5,0,3.5]
#side 5:
pa5= [0,2.5,1.5] 
pb5= [1,2.5,1.5] 
pc5= [2,2.5,1.5] 
pd5= [0,2.5,2.5]
pe5= [1,2.5,2.5]
pf5= [2,2.5,2.5] 
pg5= [0,2.5,3.5]  
ph5= [1,2.5,3.5]
pi5= [2,2.5,3.5]
#side 6:
pa6= [0,-.5,3.5]
pb6= [1,-.5,3.5]
pc6= [2,-.5,3.5] 
pd6= [0,-.5,2.5]
pe6= [1,-.5,2.5]
pf6= [2,-.5,2.5] 
pg6= [0,-.5,1.5]
ph6= [1,-.5,1.5]
pi6= [2,-.5,1.5]
positions = (pa1,pa2,pa3,pa4,pa5,pa6,pb1,pb2,pb3,pb4,pb5,pb6,pc1,pc2,pc3,pc4,pc5,pc6,pd1,pd2,pd3,pd4,pd5,pd6,pe1,pe2,pe3,pe4,pe5,pe6,pf1,pf2,pf3,pf4,pf5,pf6,pg1,pg2,pg3,pg4,pg5,pg6,ph1,ph2,ph3,ph4,ph5,ph6,pi1,pi2,pi3,pi4,pi5,pi6)

#These are all initial values, size and color will stay the same, position
#will change as the following are applied:

#each of these functions will find the 18 or 12 boxes with the given positions and
#then change their positions accordingly following the trace of a circle in a
#particular direction    
def rightdown():
    m=0
    n=0
    if debug is true:print "initial",m,n
    positions1 = (pc1,pc5,pf1,pf5,pi1,pi5,pc5,pg3,pf5,pd3,pi5,pa3,pa2,pc2,pb2,pf2,pc2,pi2,pd2,pb2,pe2,pe2,pf2,ph2,pg2,pa2,ph2,pd2,pi2,ph2,pa3,pi6,pd3,pf6,pg3,pc6,pc6,pc1,pf6,pf1,pi6,pi1)
    while m<=53 and n<=40:
        if (positions1[n])[0] == facelets[m].pos.x and (positions1[n])[1] == facelets[m].pos.y and (positions1[n])[2] == facelets[m].pos.z:
            if debug is true:print facelets[m].pos.x , (positions1[n+1])[0]
            if debug is true:print facelets[m].pos.y , (positions1[n+1])[1]
            if debug is true:print facelets[m].pos.z , (positions1[n+1])[2]
            facelets[m].pos.x = (positions1[n+1])[0]
            facelets[m].pos.y = (positions1[n+1])[1]
            facelets[m].pos.z = (positions1[n+1])[2]
            if m != 53:
                m = m+1
            if m == 53:
                m = 0
                n = n+2
        if m != 53:
                m = m+1
                #if debug is true: print "not yet",m,n
        if m == 53:
                m = 0
                n = n+2
rightdown()
##    while m <= 53 and n <= 41:
##        #if debug is true:  print facelets[m].pos, positions1[n]
##        if positions1[n] == facelets[m].pos:
##            if debug is true:print "found one",m,n
##            facelets[m].pos = positions1[n+1] 
##            if m != 53:
##                m = m+1
##            if m == 53:
##                m = 0
##                n = n+2
##        if m != 53:
##                m = m+1
##                #if debug is true: print "not yet",m,n
##        if m == 53:
##                m = 0
##                n = n+2



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
