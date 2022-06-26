from visual import *

#This class puts VPython objects added to it with its add() method into a VPython
#   frame object which when positioned or oriented will treat all the objects it
#   contains as a group
class CompositeObject:
    frame=frame(axis=(0,-1,0))

    def add(self,thing):
        'add a new object'
        thing.frame = self.frame


    def setAngle(self,theta):
        'set the angle of the frame with respect to vertical'
        self.frame.axis = (sin(theta), -cos(theta), 0)

    #This special function is called automatically whenever an attribute is referenced
    def __setattr__(self,name,value):
        if name=='axis':
            self.frame.axis=value

        if name=='angle':
            self.setAngle(value)
        else:
            self.__dict__[name]=value # this actually assigns the attribute the new value


            
class Spring:
    curve = curve(radius=0.01) # the visual representation of the spring

    def __init__(self,length=1, rest_length=1, k=10, damping=.8, turns=10):
        self.length      = length
        self.rest_length = rest_length
        self.k           = k       # spring constant (stiffness)
        self.damping     = damping # damping factor (damping due to friction)
        self._helix(length,turns)  # draw the spring

    def _helix(self,length=1, turns=10):
        '''This method draws the visual representation of the spring
           which is a helix from x=0 to x=length centered around x axis'''

        radius=.1 #how big around the turns of the helix are
        x=0
        dx = float(length)/turns/12 # how far forward each point is in X direction
        dtheta=pi/6 # angle between successive points
        points=[]
        for theta in arange(0,2*pi*turns,dtheta):
            z=radius*cos(theta)
            y=radius*sin(theta)
            points.append((x,y,z))
            x += dx
        self.curve.pos = points

    def __setattr__(self,name,value):
        if name=='frame':
            self.curve.frame=value
        elif name=='length':
            self._helix(value)
        self.__dict__[name]=value




class SpringPendulum(CompositeObject):
    'A class of objects representing a spring fixed at one end with a mass attached to the other'
    steps = 1         #number of Euler steps to simulate for each requested time interval
    v = vector(0,0,0) #velocity vector
    p = vector(0,0,0) #position vector

    def __init__(self):
        self.spring=Spring()
        self.add( self.spring )
        self.bob = sphere(radius=.2,color=color.red, pos=(self.spring.length,0,0))
        self.mass = 1.0
        self.pos = vector(0,-self.spring.length,0)
        self.add(self.bob)

   
    def simulate(self,time_interval):
        '''simulate forward in time using "steps" subintervals using Euler's method'''
        dt = float(time_interval)/self.steps
        g=vector(0,-9.8,0) # acceleration due to gravity
        p=self.pos
        v=self.velocity
        t=0
        while t<time_interval:
            S=mag(p)-self.spring.rest_length  # compute extension of the spring
            phat = norm(p) # the direction of force from spring and spring damping

            # force from spring extension
            Fspring = -self.spring.k*S*phat    
            
            # force from spring damping (friction in the spring)
            Fdamp = dot(-self.spring.damping*v,phat)*phat # friction in spring

            # force from air resistance proportional to velocity 
            Fair  = -.01*v  

            # sum the forces acting on the pendulum bob
            Fnet = g + Fspring + Fdamp + Fair 
            a  = Fnet/self.mass   # compute acceleration
            v += a*dt  # update velocity
            p += v*dt  # update position
            t += dt    # update time

        #copy final values back into this object's attributes
        self.pos = p
        self.velocity = v
                                         
    def _setPosition(self,position):
        self.frame.axis=norm(position)
        self._setLength(mag(position))

    def _setLength(self,l):
        '''change the pendulum's length'''
        self.spring.length=l  # set springs length
        self.bob.pos=(l,0,0)  # update the bob's position
        self.__dict__['pos']=l*norm(self.pos)

    def __setattr__(self,name,value):
        self.__dict__[name]=value
        if name=='pos':
            self._setPosition(value)
        elif name=='length':
            self._setLength(value)
        elif name=='theta':
            CompositeObject.setAngle(self,value)
            self.pos = vector(self.spring.length*sin(value),-self.spring.length*cos(value),0)
