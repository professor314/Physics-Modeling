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
hawk = Bird(name='sean')
hawk.fly()

