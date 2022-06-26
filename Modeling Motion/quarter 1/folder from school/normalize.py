from math import sqrt

# Define a function to return a normalized vector. A normalized vector
# points in the same direction but has a magnitude of one.

def normalize(vec):
    x=vec[0] # extract the first  element
    y=vec[1] # extract the second element
    mag = sqrt(x*x+y*y) # compute magnitude
    return [x/mag, y/mag]

#try it out
norm = normalize( [2,4] )
print "[2,4] normalized is",norm
print "CHECK. length of normal should be 1:",sqrt(norm[0]*norm[0]+norm[1]*norm[1])
