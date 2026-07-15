from visual import *
from math import *

scene.range = 6
scene.center = (0,0,0)
debug = true
#stereodepth = 2
#scene.lights = [vector(3,0,0)]
#scene.ambient = 0
#c = controls()
#b=button(pos = (0,0),width = 60, length =60, text = "right down", action = lambda: rightdown())
#class cubelet:
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
facelets = (a1,a2,a3,a4,a5,a6,b1,b2,b3,b4,b5,b6,c1,c2,c3,c4,c5,c6,d1,d2,d3,d4,d5,d6,e1,e2,e3,e4,e5,e6,f1,f2,f3,f4,f5,f6,g1,g2,g3,g4,g5,g6,h1,h2,h3,h4,h5,h6,i1,i2,i3,i4,i5,i6)

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
for k in imaginary_list:
    k.visible =0
    
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
#sizes:
#side 1:
sa1= (1,1,.01) 
sb1= (1,1,.01)   
sc1= (1,1,.01)
sd1= (1,1,.01)
se1= (1,1,.01)
sf1= (1,1,.01)
sg1= (1,1,.01)
sh1= (1,1,.01)   
si1= (1,1,.01)
#side 2:
sa2= (0.01,1,1) 
sb2= (0.01,1,1)
sc2= (0.01,1,1)
sd2= (0.01,1,1)
se2= (0.01,1,1)
sf2= (0.01,1,1)
sg2= (0.01,1,1)
sh2= (0.01,1,1)
si2= (0.01,1,1)
#side 3:
sa3= [1, 1, 0.01]    
sb3= [1, 1, 0.01]         
sc3= [1, 1, 0.01]         
sd3= [1, 1, 0.01]      
se3= [1, 1, 0.01]      
sf3= [1, 1 ,0.01]
sg3= [1 ,1 ,0.01]      
sh3= [1, 1, 0.01]         
si3= [1, 1 ,0.01] 
#side 4:
sa4= [0.01, 1, 1]
sb4= [0.01, 1 ,1]
sc4= [0.01, 1 ,1]
sd4= [0.01, 1 ,1]
se4= [0.01, 1, 1]
sf4= [0.01 ,1, 1]
sg4= [0.01 ,1, 1]
sh4= [0.01, 1, 1] 
si4= [0.01, 1, 1]
#side 5:
sa5= [1, 0.01 ,1]
sb5= [1, 0.01 ,1]
sc5= [1 ,0.01 ,1]
sd5= [1, 0.01, 1]
se5= [1, 0.01 ,1]
sf5= [1, 0.01 ,1]
sg5= [1, 0.01 ,1] 
sh5= [1, 0.01 ,1]
si5= [1, 0.01, 1]
#side 6:
sa6= [1, 0.01, 1]
sb6= [1, 0.01, 1]
sc6= [1, 0.01, 1] 
sd6= [1, 0.01, 1]
se6= [1, 0.01 ,1]
sf6= [1, 0.01, 1] 
sg6= [1, 0.01, 1]
sh6= [1, 0.01, 1] 
si6= [1, 0.01, 1]
#These are all initial values, size and color will stay the same, position
#will change as the following are applied:
#these are the six "x's" to be input into turn
bottom =(pa6,pc6,pb6,pf6,pc6,pi6,pd6,pb6,pe6,pe6,pf6,ph6,pg6,pa6,ph6,pd6,pi6,pg6,pg1,pg2,ph1,ph2,pi1,pi2,pg2,pg3,ph2,ph3,pi2,pi3,pg3,pg4,ph3,ph4,pi3,pi4,pg4,pg1,ph4,ph1,pi4,pi1)
top =   (pa5,pc5,pb5,pf5,pc5,pi5,pd5,pb5,pe5,pe5,pf5,ph5,pg5,pa5,ph5,pd5,pi5,pg5,pc3,pc2,pb3,pb2,pa3,pa2,pc2,pc1,pb2,pb1,pa2,pa1,pc1,pc4,pb1,pb4,pa1,pa4,pc4,pc3,pb4,pb3,pa4,pa3)
front = (pa1,pc1,pb1,pf1,pc1,pi1,pd1,pb1,pe1,pe1,pf1,ph1,pg1,pa1,ph1,pd1,pi1,pg1,pg5,pa2,ph5,pd2,pi5,pg2,pa2,pc6,pd2,pb6,pg2,pa6,pc6,pi4,pb6,pf4,pa6,pc4,pi4,pg5,pf4,ph5,pc4,pi5)
back =  (pa3,pc3,pb3,pf3,pc3,pi3,pd3,pb3,pe3,pe3,pf3,ph3,pg3,pa3,ph3,pd3,pi3,pg3,pi2,pc5,pf2,pb5,pc2,pa5,pc5,pa4,pb5,pd4,pa5,pg4,pa4,pg6,pd4,ph6,pg4,pi6,pg6,pi2,ph6,pf2,pi6,pc2)
left =  (pa1,pa6,pd1,pd6,pg1,pg6,pa5,pa1,pd5,pd1,pg5,pg1,pi3,pa5,pf3,pd5,pc3,pg5,pa4,pc4,pb4,pf4,pc4,pi4,pd4,pb4,pe4,pe4,pf4,ph4,pg4,pa4,ph4,pd4,pi4,pg4,pg6,pc3,pd6,pf3,pa6,pi3)
right = (pc1,pc5,pf1,pf5,pi1,pi5,pc5,pg3,pf5,pd3,pi5,pa3,pa2,pc2,pb2,pf2,pc2,pi2,pd2,pb2,pe2,pe2,pf2,ph2,pg2,pa2,ph2,pd2,pi2,pg2,pa3,pi6,pd3,pf6,pg3,pc6,pc6,pc1,pf6,pf1,pi6,pi1)
#each of these functions will find the boxes with the given positions and
#then change their positions accordingly following the trace of a circle in a
#particular direction    
def turn(x): #turn face 'x'
    if x ==top: face = top
    if x == bottom: face = bottom
    if x == left: face = left
    if x == right: face = right
    if x == back: face = back
    if x == front: face = front
    m=0
    n=0
    positions2 = x
    faceletslistx = []
    faceletslisty = []
    faceletslistz = []
    sizes = []
    faceletsmove = [] #list of the facelets that this function will actually move 
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
    while n<21:
        faceletsmove[n].pos.x = faceletslistx[n]
        faceletsmove[n].pos.y = faceletslisty[n]
        faceletsmove[n].pos.z = faceletslistz[n]
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

##        if faceletsmove[n].size == a1.size:
##            print faceletsmove[n].size, "same as", a1.size
##        if faceletsmove[n].size == a2.size:
##            print faceletsmove[n].size, "same as", a2.size
##        if faceletsmove[n].size == a3.size:
##            print faceletsmove[n].size, "same as", a3.size
##        if faceletsmove[n].size == a4.size:
##            print faceletsmove[n].size, "same as", a4.size
##        if faceletsmove[n].size == a5.size:
##            print faceletsmove[n].size, "same as", a5.size
##        if faceletsmove[n].size == a6.size:
##            print faceletsmove[n].size, "same as", a6.size
        n=n+1
while True:
    input()


