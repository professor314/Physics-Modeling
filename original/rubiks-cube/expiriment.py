from visual import *
scene.range = 7

homebox1 = (3,2,1)
box1 = box()
box1.pos.x=3
box1.pos.y=2
box1.pos.z=1
 #this works!

if box1.pos.x == homebox1[0]:  # Python 3 fix - was 'while a if' (invalid syntax, work in progress)
    print("yes")  # Python 3 fix
else: print("no")  # Python 3 fix
