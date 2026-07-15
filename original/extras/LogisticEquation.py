from math import *
from visual.graph import *
a=1
class LogisticEquation:
    def _init__(self,k,C,initialvalue):
        self.initialvalue = initialvalue  # Python 3 fix
        self.k = k
        self.C = C
    def evaluate(self,t=0):
        pass  # Python 3 fix - incomplete function (work in progress)

    def drawgraph(self,tfinal,dt=.1):

        self.dt = dt
        self.tfinal = tfinal
        t=0
        # 'graph'+str(a) = gdisplay(...)  # Python 3 fix - invalid assignment target (work in progress)
        # line = gcurve(color=color.red)
        # while t<=tfinal:
        #     P = x
        #     DP =
        #     t = t+dt
        # a = a+1  #this is so when the next graph is made it will create a new window with a new name
        pass  # Python 3 fix - incomplete function (work in progress)
