#compute the average of a list of numbers
total = 0
for number in [10,1,9,2,8,3,7,4,6,5]:
    total = total + number

average = total/10.0 # don't forget to do floating point divide
print average

#skip some space
print
print


#A uniform motion example
print 't | x'
print '-----'
for t in [0,1,2,3,4,5,6,7,8,9,10]:
    x = 2 + 3*t
    print t,'|',x

print
print

#The same thing using the range() function
print 't | x'
print '-----'
for t in range(11):
    x = 2 + 3*t
    print t,'|',x


    
