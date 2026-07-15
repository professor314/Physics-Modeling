---
title: "Test/Exam Code Listings"
author: Sean Connolly
date: 2004
course: Modeling Motion
original_file: "test-1d.rtf, test-2c.rtf, test-2d.rtf, test-aviary.rtf, test-logistic.rtf"
notes: "Code written for tests/exams, preserved in RTF format. These are the original Python 2 versions as submitted."
---

# Test/Exam Code Listings

These programs were written as part of tests and exams for the Modeling Motion course. They demonstrate numerical methods, graphing, and object-oriented programming concepts.

---

## 1d — Arc Length by Numerical Integration

Computes the arc length of the curve y = x²/2 from 0 to a, using the formula S = ∫√(1 + (dy/dx)²) dx with Riemann sums.

```python
from math import *
for a in (1,2,3,4):
    upper_bound = a
    lower_bound = 0
    steps = 1000
    accumulation = 0
    numsteps = 100000
    deltax = float((upper_bound - lower_bound))/numsteps
    x = lower_bound
    while x <= a-.0000001:
        deltaS = sqrt(1+x**2)*deltax
        accumulation = accumulation+deltaS
        x += deltax
    print "length=",accumulation,"numsteps=",numsteps,"a=",a,x
```

---

## 2c — Logistic Function (Exact Solution)

Plots the exact solution of the logistic equation P(t) = 100A·eᵗ / (1 + A·eᵗ) with A = 0.25.

```python
from visual.graph import *
from math import *

graph1 = gdisplay(x=0, y=0, width=600, height=800, 
          title='2c', xtitle='time', ytitle='P(t)', 
          xmax=11., xmin=0, ymax=120, ymin=-2)
A = .25
t=0
deltat = .125
line = gcurve(color=color.cyan)
while t<=10:
    function = (100.*A*e**t)/(1.+A*e**t)
    line.plot(pos=(t,function))
    t+=deltat
```

---

## 2d — Euler's Method for Differential Equation

Solves y' = 100eᵗ/(1+eᵗ) numerically using Euler's method and plots the result.

```python
from math import *
from visual.graph import *

graph1 = gdisplay(x=0, y=0, width=600, height=600, 
          title='2d', xtitle='t', ytitle='y', 
          xmax=10., xmin=-1., ymax=1000, ymin=-1)
yplot = gcurve(color=color.red)
tinitial = 0
tfinal =10
t=tinitial
y=20    #initial value of y
deltat=.005
while t<=tfinal:
    yprime = (100*e**t)/(1+e**t)
    deltay = deltat*yprime
    yplot.plot(pos=(t,y))
    t=t+deltat
    y=y+deltay
```

---

## Aviary — Bird Class

An object-oriented programming exercise defining a Bird class with fly and land behaviors.

```python
from string import *
class Bird:
    def __init__(self,name,fly='no',land='yes'):
        self.name = name
        self.land=land
        self.fly=fly
        print "Hi, I'm", self.name
    def fly(self):
        if self.fly == 'yes':
            print self.name, "is already flying"
        if self.fly != 'yes':
            self.fly = 'yes'
            print self.name, "is now flying"
    def land(self):
        if self.land =='yes':
            print self.name, "already perched"
        if self.land !='yes':
            self.land = 'yes'
            print self.name, "landed"
```

---

## Logistic Equation — Class-Based Approach (Incomplete)

An attempt at a class-based logistic equation solver. This appears to be an incomplete work-in-progress with some syntax issues.

```python
from math import *
from visual.graph import *
a=1
class LogisticEquation:
    def _init__(self,k,C,initialvalue):
        self.initialvalue = initial
        self.k = k
        self.C = C
    def evaluate(self,t=0):
        
    def drawgraph(self,tfinal,dt=.1):
    
        self.dt = dt
        self.tfinal = tfinal
        t=0
        'graph'+str(a) = gdisplay(x=0, y=0, width=600, height=600, 
          title='Logistic Equation', xtitle='t', ytitle='y',
          xmax=tfinal, xmin=0., ymax=300, ymin=0)
        line = gcurve(color=color.red)
        while t<=tfinal:
            P = x
            DP = 
            t = t+dt
        a = a+1  #this is so when the next graph is made it will create a new window with a new name
```

> *Note: This code has intentional gaps (empty method bodies, incomplete expressions) — it appears to be a work-in-progress captured during the test.*

---

> *The Python source files corresponding to these listings are in [original/extras/](../../original/extras/) (1d.py, final test 2c.py, etc.)*
