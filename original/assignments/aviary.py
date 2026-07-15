class Bird:
    def __init__(self,name,fly='no',land='yes'):
        self.name = name
        self.land=land
        self.fly=fly
        print("Hi, I'm", self.name)  # Python 3 fix
    def fly(self):
        if self.fly == 'yes':
            print(self.name, "is already flying")  # Python 3 fix
        if self.fly != 'yes':
            self.fly = 'yes'
            print(self.name, "is now flying")  # Python 3 fix
    def land(self):
        if self.land =='yes':
            print(self.name, "already perched")  # Python 3 fix
        if self.land !='yes':
            self.land = 'yes'
            print(self.name, "landed")  # Python 3 fix
hawk = Bird(name='sean')
hawk.fly()

