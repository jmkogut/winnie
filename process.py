from model import User

class Process(object):

    def __init__(self):
        pass

    def irc(self, source=None, target=None, text=None):
        User.learned(source, text)
        print "<%s> %s :: %s" % (target, source, text)
