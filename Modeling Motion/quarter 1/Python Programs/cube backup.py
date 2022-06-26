from visual import *
from math import *
from visual.controls import *
from random import *
scene = display(x = 4000, y=500)
scene.range = 6
scene.center = (0,0,0)
##stereodepth = 2

#these controls don't work just yet but they will allow the user to use the mouse instead of having to do so much command typing
##c = controls(title='Possible Moves')
##right_down = button(pos = (0,0),width = 60, length =100, text = "right down", action = lambda: counter(right))
##right_up = button(pos = (60,0),width = 60, length =100, text = "right up", action = lambda: clock(right))
##left_down = button(pos = (0,40),width = 60, length =100, text = "left down", action = lambda: clock(left))
##left_up = button(pos = (60,40),width = 60, length =100, text = "left up", action = lambda: counter(left))
##bottom_left = button(pos = (120,40),width = 60, length =100, text = "bottom left", action = lambda: counter(left))
##bottom_right = button(pos = (120,40),width = 60, length =100, text = "bottom right", action = lambda: clodk(left))
##class cubelet:

#This next part is the physical cube.  The colors will eventually be predefined by the user when the program is able to solve a cube, but for now the initial position is the solved cube.  
#a loop may be able to create all of these, but for now this long list will do fine.
#side 1
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
#this next list of facelets will be rather important later:
facelets = (a1,a2,a3,a4,a5,a6,b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,c6,d1,d2,d3,d4,d5,d6,e1,e2,e3,e4,e5,e6,f1,f2,f3,f4,f5,f6,g1,g2,g3,g4,g5,g6,h1,h2,h3,h4,h5,h6,i1,i2,i3,i4,i5,i6)
#these next ones are imaginary facelets or home facelets.  These are used to remember the initial positions and/or colors of the "home" facelets.  The imaginary cubelets are just like the regular ones except you can't see them.  The program refers to them to decide what is supposed to be where
ia1= box(pos=(0,2,4), size = (1,1,.01), color = color.orange) 
ib1= box(pos=(1,2,4), size = (1,1,.01), color = color.orange)     
ic1= box(pos=(2,2,4), size = (1,1,.01), color = color.orange)
id1= box(pos=(0,1,4), size = (1,1,.01), color = color.orange)
ie1= box(pos=(1,1,4), size = (1,1,.01), color = color.orange)
if1= box(pos=(2,1,4), size = (1,1,.01), color = color.orange)
ig1= box(pos=(0,0,4), size = (1,1,.01), color = color.orange)     
ih1= box(pos=(1,0,4), size = (1,1,.01), color = color.orange)    
ii1= box(pos=(2,0,4), size = (1,1,.01), color = color.orange)
#side 2:
ia2= box(pos=(2.5,2,3.5), size = (.01,1,1), color = color.white) 
ib2= box(pos=(2.5,2,2.5), size = (.01,1,1), color = color.white)
ic2= box(pos=(2.5,2,1.5), size = (.01,1,1), color = color.white)
id2= box(pos=(2.5,1,3.5), size = (.01,1,1), color = color.white)
ie2= box(pos=(2.5,1,2.5), size = (.01,1,1), color = color.white)
if2= box(pos=(2.5,1,1.5), size = (.01,1,1), color = color.white)
ig2= box(pos=(2.5,0,3.5), size = (.01,1,1), color = color.white)
ih2= box(pos=(2.5,0,2.5), size = (.01,1,1), color = color.white)
ii2= box(pos=(2.5,0,1.5), size = (.01,1,1), color = color.white)
#side 3:
ia3= box(pos=(2,2,1), size = (1,1,.01), color = color.red)     
ib3= box(pos=(1,2,1), size = (1,1,.01), color = color.red)          
ic3= box(pos=(0,2,1), size = (1,1,.01), color = color.red)          
id3= box(pos=(2,1,1), size = (1,1,.01), color = color.red)       
ie3= box(pos=(1,1,1), size = (1,1,.01), color = color.red)       
if3= box(pos=(0,1,1), size = (1,1,.01), color = color.red)
ig3= box(pos=(2,0,1), size = (1,1,.01), color = color.red)       
ih3= box(pos=(1,0,1), size = (1,1,.01), color = color.red)          
ii3= box(pos=(0,0,1), size = (1,1,.01), color = color.red)   
#side 4:
ia4= box(pos=(-.5,2,1.5), size = (.01,1,1), color = color.yellow) 
ib4= box(pos=(-.5,2,2.5), size = (.01,1,1), color = color.yellow)
ic4= box(pos=(-.5,2,3.5), size = (.01,1,1), color = color.yellow)
id4= box(pos=(-.5,1,1.5), size = (.01,1,1), color = color.yellow)
ie4= box(pos=(-.5,1,2.5), size = (.01,1,1), color = color.yellow) 
if4= box(pos=(-.5,1,3.5), size = (.01,1,1), color = color.yellow)
ig4 = box(pos=(-.5,0,1.5), size = (.01,1,1), color = color.yellow)
ih4= box(pos=(-.5,0,2.5), size = (.01,1,1), color = color.yellow) 
ii4= box(pos=(-.5,0,3.5), size = (.01,1,1), color = color.yellow)
#side 5:
ia5= box(pos=(0,2.5,1.5), size = (1,.01,1), color = color.blue) 
ib5= box(pos=(1,2.5,1.5), size = (1,.01,1), color = color.blue) 
ic5= box(pos=(2,2.5,1.5), size = (1,.01,1), color = color.blue) 
id5= box(pos=(0,2.5,2.5), size = (1,.01,1), color = color.blue)
ie5= box(pos=(1,2.5,2.5), size = (1,.01,1), color = color.blue)
if5= box(pos=(2,2.5,2.5), size = (1,.01,1), color = color.blue) 
ig5= box(pos=(0,2.5,3.5), size = (1,.01,1), color = color.blue)  
ih5= box(pos=(1,2.5,3.5), size = (1,.01,1), color = color.blue)
ii5= box(pos=(2,2.5,3.5), size = (1,.01,1), color = color.blue)
#side 6:
ia6= box(pos=(0,-.5,3.5), size = (1,.01,1), color = color.green)
ib6= box(pos=(1,-.5,3.5), size = (1,.01,1), color = color.green)
ic6= box(pos=(2,-.5,3.5), size = (1,.01,1), color = color.green) 
id6= box(pos=(0,-.5,2.5), size = (1,.01,1), color = color.green)
ie6= box(pos=(1,-.5,2.5), size = (1,.01,1), color = color.green)
if6= box(pos=(2,-.5,2.5), size = (1,.01,1), color = color.green) 
ig6= box(pos=(0,-.5,1.5), size = (1,.01,1), color = color.green)
ih6= box(pos=(1,-.5,1.5), size = (1,.01,1), color = color.green) 
ii6= box(pos=(2,-.5,1.5), size = (1,.01,1), color = color.green)
imaginary_list = (ia1,ia2,ia3,ia4,ia5,ia6,ib1,ib2,ib3,ib4,ib5,ib6,ic1,ic2,ic3,ic4,ic5,ic6,id1,id2,id3,id4,id5,id6,ie1,ie2,ie3,ie4,ie5,ie6,if1,if2,if3,if4,if5,if6,ig1,ig2,ig3,ig4,ig5,ig6,ih1,ih2,ih3,ih4,ih5,ih6,ii1,ii2,ii3,ii4,ii5,ii6)
for k in imaginary_list: #this makes them invisible, hence imaginary
    k.visible =0

#this is just a list of all the positions of the cubes which isn't really needed now that I have imaginary cubes, but until I change the clock() function this needs to stay
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
#here is a handy list of the positions:
positions = (pa1,pa2,pa3,pa4,pa5,pa6,pb1,pb2,pb3,pb4,pb5,pb6,pc1,pc2,pc3,pc4,pc5,pc6,pd1,pd2,pd3,pd4,pd5,pd6,pe1,pe2,pe3,pe4,pe5,pe6,pf1,pf2,pf3,pf4,pf5,pf6,pg1,pg2,pg3,pg4,pg5,pg6,ph1,ph2,ph3,ph4,ph5,ph6,pi1,pi2,pi3,pi4,pi5,pi6)
#these are the six "x's" to be input into clock(x).  they are in a special order which will be explained later
bottom =(pa6,pc6,pb6,pf6,pc6,pi6,pd6,pb6,pe6,pe6,pf6,ph6,pg6,pa6,ph6,pd6,pi6,pg6,pg1,pg2,ph1,ph2,pi1,pi2,pg2,pg3,ph2,ph3,pi2,pi3,pg3,pg4,ph3,ph4,pi3,pi4,pg4,pg1,ph4,ph1,pi4,pi1)
top =   (pa5,pc5,pb5,pf5,pc5,pi5,pd5,pb5,pe5,pe5,pf5,ph5,pg5,pa5,ph5,pd5,pi5,pg5,pc3,pc2,pb3,pb2,pa3,pa2,pc2,pc1,pb2,pb1,pa2,pa1,pc1,pc4,pb1,pb4,pa1,pa4,pc4,pc3,pb4,pb3,pa4,pa3)
front = (pa1,pc1,pb1,pf1,pc1,pi1,pd1,pb1,pe1,pe1,pf1,ph1,pg1,pa1,ph1,pd1,pi1,pg1,pg5,pa2,ph5,pd2,pi5,pg2,pa2,pc6,pd2,pb6,pg2,pa6,pc6,pi4,pb6,pf4,pa6,pc4,pi4,pg5,pf4,ph5,pc4,pi5)
back =  (pa3,pc3,pb3,pf3,pc3,pi3,pd3,pb3,pe3,pe3,pf3,ph3,pg3,pa3,ph3,pd3,pi3,pg3,pi2,pc5,pf2,pb5,pc2,pa5,pc5,pa4,pb5,pd4,pa5,pg4,pa4,pg6,pd4,ph6,pg4,pi6,pg6,pi2,ph6,pf2,pi6,pc2)
left =  (pa1,pa6,pd1,pd6,pg1,pg6,pa5,pa1,pd5,pd1,pg5,pg1,pi3,pa5,pf3,pd5,pc3,pg5,pa4,pc4,pb4,pf4,pc4,pi4,pd4,pb4,pe4,pe4,pf4,ph4,pg4,pa4,ph4,pd4,pi4,pg4,pg6,pc3,pd6,pf3,pa6,pi3)
right = (pc1,pc5,pf1,pf5,pi1,pi5,pc5,pg3,pf5,pd3,pi5,pa3,pa2,pc2,pb2,pf2,pc2,pi2,pd2,pb2,pe2,pe2,pf2,ph2,pg2,pa2,ph2,pd2,pi2,pg2,pa3,pi6,pd3,pf6,pg3,pc6,pc6,pc1,pf6,pf1,pi6,pi1)
#this first function finds the boxes with the positions that change and then changes them according to what face of the cube you want to turn
def clock(x): #turn face 'x' clockwise
    #these are just so the function knows what list above to look at later
    if x ==top: face = top
    if x == bottom: face = bottom
    if x == left: face = left
    if x == right: face = right
    if x == back: face = back
    if x == front: face = front
    m=0
    n=0
    positions2 = x  #this gives x a more meaningful name
    #these empty lists are for saving the new coordinates of the facelets in
    faceletslistx = []
    faceletslisty = []
    faceletslistz = []
    sizes = []
    faceletsmove = [] #list of the facelets that this function will actually move 
    #this part quickly searches through facelets and decides which ones to move and to where
    while m<=53 and n<=40:
        if (positions2[n])[0] == facelets[m].pos.x and (positions2[n])[1] == facelets[m].pos.y and (positions2[n])[2] == facelets[m].pos.z:
            faceletsmove.append(facelets[m])
            faceletslistx.append((positions2[n+1])[0])
            faceletslisty.append((positions2[n+1])[1])
            faceletslistz.append((positions2[n+1])[2])          
            if m != 53:
                m = m+1
            elif m == 53:
                m = 0
                n = n+2
        elif m != 53:
                m = m+1
        elif m == 53:
                m = 0
                n = n+2
    n=0
    #this part does the actual moving(there are always 21 facelets that move)
    while n<21:
        faceletsmove[n].pos.x = faceletslistx[n]
        faceletsmove[n].pos.y = faceletslisty[n]
        faceletsmove[n].pos.z = faceletslistz[n]
        #this part is rather long and could profit from a loop since the lines are so similar
        if face == front:
            if faceletsmove[n].size == ia1.size:
                faceletsmove[n].size = ia1.size
            elif faceletsmove[n].size == ia5.size:
                faceletsmove[n].size = ia2.size
            elif faceletsmove[n].size == ia2.size:
                faceletsmove[n].size = ia6.size
            elif faceletsmove[n].size == ia6.size:
                faceletsmove[n].size = ia4.size
            elif faceletsmove[n].size == ia4.size:
                faceletsmove[n].size = ia5.size
        elif face == back:
            if faceletsmove[n].size == ia3.size:
                faceletsmove[n].size = ia3.size
            elif faceletsmove[n].size == ia5.size:
                faceletsmove[n].size = ia4.size
            elif faceletsmove[n].size == ia4.size:
                faceletsmove[n].size = ia6.size
            elif faceletsmove[n].size == ia6.size:
                faceletsmove[n].size = ia2.size
            elif faceletsmove[n].size == ia2.size:
                faceletsmove[n].size = ia5.size
        elif face == left:
            if faceletsmove[n].size == ia4.size:
                faceletsmove[n].size = ia4.size
            elif faceletsmove[n].size == ig5.size:
                faceletsmove[n].size = ia1.size
            elif faceletsmove[n].size == ia1.size:
                faceletsmove[n].size = ia6.size
            elif faceletsmove[n].size == ia6.size:
                faceletsmove[n].size = ia3.size
            elif faceletsmove[n].size == ia3.size:
                faceletsmove[n].size = ia5.size
        elif face == right:
            if faceletsmove[n].size == ia2.size:
                faceletsmove[n].size = ia2.size
            elif faceletsmove[n].size == ig5.size:
                faceletsmove[n].size = ia3.size
            elif faceletsmove[n].size == ia3.size:
                faceletsmove[n].size = ia6.size
            elif faceletsmove[n].size == ia6.size:
                faceletsmove[n].size = ia1.size
            elif faceletsmove[n].size == ia1.size:
                faceletsmove[n].size = ia5.size
        elif face == top:
            if faceletsmove[n].size == ia5.size:
                faceletsmove[n].size = ia5.size
            elif faceletsmove[n].size == ig3.size:
                faceletsmove[n].size = ia2.size
            elif faceletsmove[n].size == ia2.size:
                faceletsmove[n].size = ia1.size
            elif faceletsmove[n].size == ia1.size:
                faceletsmove[n].size = ia4.size
            elif faceletsmove[n].size == ia4.size:
                faceletsmove[n].size = ia3.size
        elif face == bottom:
            if faceletsmove[n].size == ia6.size:
                faceletsmove[n].size = ia6.size
            elif faceletsmove[n].size == ig1.size:
                faceletsmove[n].size = ia2.size
            elif faceletsmove[n].size == ia2.size:
                faceletsmove[n].size = ia3.size
            elif faceletsmove[n].size == ia3.size:
                faceletsmove[n].size = ia4.size
            elif faceletsmove[n].size == ia4.size:
                faceletsmove[n].size = ia5.size
        n=n+1
#a counter-clockwise turn is the same as 3 clockwise ones, if the computer couldn't do it so fast it would be more efficient to have a separate function here which is just the same as the above using different lists for directions
def counter(x):
    clock(x)
    clock(x)
    clock(x)
#this next function will actually mix up the cube with x quarter turns.  Note that it doesn't randomly decide colors to cubes, it moves them.  If it wasn't done this way it is very likely that the cube it creates is unsolvable. (take a real cube apart, put it together all mixed up and you will find that it is unsolvable)
def mix(x):
    #this function is rather strieght-forward, note only clockwise turns are used.  this is so an opposite move can't be made after a quarter turn, which is a rule for mixing up cubes in cube tournaments.  An x value of 22 mixes a cube up entirely.  Any x over 10000 takes to long, but can be done
    k = 1
    while k<=x:
        a = random()
        if a <=.1666666:
            clock(left)
        elif a>.1666666 and a<=.333333:
            clock(right)
        elif a >.333333 and a<=.5:
            clock(bottom)
        elif a >.5 and a<=.666666:
            clock(top)
        elif a > .666666 and a <=.833333:
            clock(back)
        else: clock(front)
        k =1+k
#this is the algorithm the computer will use to solve but it is far from finished, 
def cubelet_search(x):#will find what face the cubelet we are looking for is on
    k = 0
    search = []
    print "searching"
    while k <= 54:
        if x.pos == imaginary_list[k].pos and x.size == imaginary_list[k].size:
            k = 55
            if x.size == ia1.size:
                return search.append(front)
            elif x.size == ia2.size:
                return search.append(right)
            elif x.size == ia3.size:
                return search.append(back)
            elif x.size == ia4.size:
                return search.append(left)
            elif x.size == ia5.size:
                return search.append(top)
            elif x.size == ia6.size:
                return search.append(bottom)
            if x.pos == id4: search.append(1)
        else:
            k=k+1
#to solve a cube, first the colored cross must be made.  This doesn't work yet.
def cross1():
    a = cubelet_search(h1)
    print cubelet_search(h1)
    if a[2] == 1:
        while x.pos != id4.pos:
            clock(back)
    counter(left)
    counter(right)
    clock(bottom)
    clock(left)
    clock(bottom)
def solved():
    #this will check if the cube is solved. If it is it returns True
    correct_cubes_at_once = 0
    for k in facelets:
        for l in imaginary_list:
            if k.pos==l.pos:
                correct_cubes_at_once += 1
                if correct_cubes_at_once == 2:
                    print "i got two at once"
            else:
                return False
                break
    return True
#this next silly function is so the computer can do random moves and try to solve a mixed cube.  If it solves it it says something.  It would take a long time for it to solve it this way
def solve():
    solved_now=solved()
    million_moves = 0
    moves = 0
    n=0
    while solved_now!=True:
        if solved()==False:
            mix(1)
            n+=1
            if moves == 1000000:
                million_moves+=1
                moves = 0
                print "still going after", million_moves, "million moves"
            else:
                moves = moves+1
                if moves == 1000:
                    print million_moves, "million","1000", "moves done with no avail"
        else:
            print "I did it! in", million_moves, "million moves!"
            solved_now = True
##while 1:
##    c.interact() # Check for mouse events and drive specified actions
#this last line is so the user can countinously input functions
while True:
    input()
