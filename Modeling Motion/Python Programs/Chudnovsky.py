from math import *

sum = 0.
a = 13591409.
b = 545140134.
c = 640320.
n = 0.
upperbound = 8.
count=0

def factorial(x):
    factorial1 = 1
    n=1
    while n <= x:
        factorial1 = factorial1*n
        n=n+1
    return long(factorial1)


while n <= upperbound:
    z= factorial(6*n)
    y=long(factorial(3*n))
    sum = sum + ((-1**n)*(z/((factorial(n))**3)*(y))*((a+(b*n))/(c**(3*n+(3./2.)))))
    n=n+1 

    print "sum = ", long(sum),
    print "1/pi = ", 12*sum,
    print "pi = ",(1/(12*-sum))

