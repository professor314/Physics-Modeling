class Human:
    def __init__(self,first,last):
        self.firstname = first
        self.lastname = last

    def say(self,sentence):
        print self.firstname,"says", sentence

dude = Human("John","Dough")
dudette = Human("Jane","Dough")

dude.say("Hello")
dudette.say("Hi")
