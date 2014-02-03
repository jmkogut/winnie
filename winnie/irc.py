from twisted.python.rebuild import rebuild
from twisted.words.protocols import irc
from twisted.internet import protocol
from winnie import process
import os

class Handler(object):
    filename = os.getcwd() + "/winnie/process.py"
    lastmodified = None
    instance = None

    def getModified(self):
        return os.stat(self.filename).st_mtime

    def loader(self):
        print " -- Rebuilding handler process."
        rebuild(process)
        self.lastmodified = self.getModified()
        self.instance = process.Process()

    def __init__(self):
        self.loader()

    def get(self):
        if self.getModified() != self.lastmodified:
            self.loader()
        return self.instance

class IRCClient(irc.IRCClient):
    handler = Handler()

    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)
 
    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        self.factory.clients.append(self)
 
    def signedOn(self):
        for chan in self.factory.channels:
            self.join( chan )

        print " -- Signed on as [%s]" % (self.nickname,)
 
    def joined(self, channel):
        print ' -- Joined %s' % (channel)
 
    def privmsg(self, user, channel, msg):
        # Send this privmsg off to the Handler
        self.handler.get().irc(
                source=user,
                target=channel,
                text=msg,
                client=self,
                factory=self.factory
        )
        
class IRCClientFactory(protocol.ClientFactory):
    protocol = IRCClient
    def __init__(self, channels, config=None, nickname='winnie'):
        self.channels = channels
        self.nickname = nickname
        self.clients  = []
        self.cfg      = config
 
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
 
    def send_msg(self, channel, msg):
        for client in self.clients:
            client.say(channel, msg)
            
    def send_ctrl_msg(self, msg):
        self.send_msg(self.cfg.CMD_CHAN, msg)
