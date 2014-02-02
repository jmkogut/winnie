from twisted.python import log
from model import User

class Process(object):
    def irc(self, source=None, target=None, text=None):
        User.learned(source, text)
        print "<%s> %s :: %s" % (target, source, text)
