class Tester:
    'A Basic Unit Testing Class'
    def __init__(self,object):
        self.passed=0
        self.failed=0
        self.object=object
        print "\nTester is testing an object of class "+str(object.__class__)
        print '-'*60,'\n'
    def check(self,testname,expression):
        if expression is True:
            self.passed += 1
            print "Passed....%s test." % testname
            return True
        else:
            self.failed += 1
            print "\n*********FAILED******** %s test.\n" % testname
            return False
        
    def checkForMethod(self,methodname):
        try:
            dir(self.object).index(methodname)
        except ValueError, inst:
            self.failed += 1
            print "\n*********FAILED******** check for method: %s()\n" % methodname
            return False
        else:
            self.passed += 1
            print "Passed....check for method: "+methodname+'()'
            return True

    def checkForAttribute(self,attribute):
        if self.object.__dict__.has_key(attribute):
            self.passed += 1
            print "Passed....check for attribute: "+attribute
            return True
        else:
            self.failed += 1
            print "\n*********FAILED******** check for attribute "+attribute+'\n'
            return False

    def printResults(self):
        print
        if self.failed is 0:
            print "!!!CONGRATULATIONS!!! - all %d tests passed!" % self.passed
        else:
            print "%d tests passed %d failed. You're %.1f percent there." % \
                  (self.passed,self.failed,100.0*self.passed/(self.passed+self.failed))
    

