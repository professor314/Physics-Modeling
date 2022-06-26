#---------------------------------------------------
# tvtest.py - a program to test the Television class
#---------------------------------------------------
from timewasters import Television
from tester import Tester
import sys, string

#create a new Television object
tv = Television()

#create a Tester object to test the TV
tester = Tester(tv)

try:  #catch exceptions caused when a method or attribute has not been implemented
    
    ###Check all of the attributes and methods to see if they exist

    tester.checkForAttribute("power")
    tester.checkForAttribute("channel")
    tester.checkForMethod("turnOn")
    tester.checkForMethod("turnOff")
    tester.checkForMethod("whatsOn")
    tester.checkForMethod("surfUp")
    tester.checkForMethod("surfDown")
    tester.checkForMethod("surfTo")


    tester.check('power and channel have correct default values', \
                 tv.power is "off" and tv.channel is 2)

    tv.turnOn()
    tester.check("turnOn()", tv.power is "on" )

    tv.turnOff()
    tester.check("turnOff()", tv.power is "off" )


    tv.turnOn()
    tv.surfTo(45)
    tester.check("surfTo() within valid range", tv.channel is 45)
    tv.surfTo(71)
    tester.check("surfTo() above valid range", tv.channel is 45)
    tv.surfTo(0)
    tester.check("surfTo() below valid range", tv.channel is 45)

    tv.channel=2
    tv.surfUp()
    tester.check("surfUp()", tv.channel is 3)
    tv.surfDown()
    tester.check("surfDown()",tv.channel is 2)
    tv.channel=70
    tv.surfUp()
    tester.check("surfUp() at 70 wraps around to 1", tv.channel is 1)
    tv.channel=1
    tv.surfDown()
    tester.check("surfDown() at 1 wraps around to 70", tv.channel is 70)



    # check to see if methods return True when TV is on and False when TV is off
    tester.check("surfUp() returns True while on",   tv.surfUp()   is True)
    tester.check("surfDown() returns  while on", tv.surfDown() is True)
    tester.check("surfTo() returns True while on",   tv.surfTo(45) is True)
    tester.check("whatsOn() returns True while on",  tv.whatsOn()  is True)
    tv.turnOff()
    tv.channel=10
    tester.check("surfUp() returns False while off",   tv.surfUp()   is False)
    tester.check("surfUp() doesn't change channel while off",  tv.channel is 10)
    tester.check("surfDown() returns False while off", tv.surfDown() is False)
    tester.check("surfDown() doesn't change channel while off", tv.channel is 10)
    tester.check("surfTo() returns False while off",   tv.surfTo(45) is False)
    tester.check("surfTo() doesn't change channel while off",  tv.channel is 10)
    tester.check("whatsOn() returns False while off",  tv.whatsOn()  is False)

    tv.turnOn()
    tester.check("surfTo() returns False when channel out of range",tv.surfTo(-1) is False)

except AttributeError, instance:
    print "\nTesting cannot continue because the", \
          string.split(instance.args[0],"'")[1]+"() method is missing."
    print "\n%d tests passed out of %d attempted.\n" % (tester.passed,tester.passed+tester.failed)

else:
    tester.printResults()

