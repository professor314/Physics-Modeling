class Television:
    def __init__(self, power="off", channel=2):
        self.power = power
        self.channel = channel
    def whatsOn(self):
        if self.power=="off":
            print "This TV isn't on."
            return False
        else:
            if self.channel == 1:
                print 'Homer just said "doh!"'
            if self.channel == 2:
                print 'That guy on king of the hill says something you do not understand'
            if self.channel == 3:
                print "I Hate Lucy is on."
            if self.channel == 4:
                print "Bob Barker just reminded you to have your pet spayed."
            if self.channel == 5:
                print "Alex Tribeck no longer has a mustache!"
            if self.channel == 6:
                print "Vana White is pregnant again"
            if self.channel == 7:
                print "Kathy Lee is rambling about Cody..."
            if self.channel == 8:
                print "Midgets are wrestling"
            if self.channel == 9:
                print "Who wants to beat a Millioniare!"
            if self.channel ==10:
                print "Man drops something expensive on antique road show and curses"
            if self.channel == 11:
                print "Elvis shoots his tv"
            if self.channel == 11:
                print "Lambchops is eaten by gypsies"
            if self.channel==12:
                print "Ugly kid is drinking juice on this advertisement"
            if self.channel==13:
                print "A naked man is making a meal"
            if self.channel==14:
                print ""
            #print "Nothing good is on channel", self.channel
            return "change channel"
    def turnOn(self):
        self.power = "on"
        print "Power on"
    def turnOff(self):
        self.power="off"
        print "Power off"
    def surfTo(self,channel):
        if self.power=="off":
            print "This TV isn't on."
            return False
        else:
            if channel <=0:
                print "Channel", channel, "is out of range."
                return False
            if channel >70:
                print "Channel", channel, "is out of range."
                return False
            if channel>=1 and channel<=70:
                self.channel = channel
                print "Now on channel", channel
                return True
    def surfUp(self):
        if self.power=="off":
            print "This TV isn't on."
            return False
        else:
            if self.channel == 70:
                self.channel = 1
                return True
            else:
                self.channel = self.channel+1
                return True
    def surfDown(self):
        if self.power=="off":
            print "This TV isn't on."
            return False
        else:
            if  self.channel == 1:
                self.channel = 70
                return True
            else:
                self.channel = self.channel-1
                return True
tv = Television()
tv.channel = 8
tv.power = "on"
for n in range(11):
    tv.channel = n
    print tv.whatsOn()
