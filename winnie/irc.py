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
    names = {}

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

    def who(self, channel):
        "List the users in 'channel', usage: client.who('#testroom')"
        self.sendLine('WHO %s' % channel)

    def irc_RPL_WHOREPLY(self, *nargs):
        "Receive WHO reply from server"
        print 'WHO:', nargs

    def irc_RPL_ENDOFWHO(self, *nargs):
        "Called when WHO output is complete"
        pass

    def irc_RPL_NAMREPLY(self, *nargs):
        'Reply for every time you join a chan.'
        chan = nargs[1][2]
        self.names[ chan ] = ([n for n in nargs[1][3].split(' ') if n.strip() != ''])
        print ' -- Users in %s: %s' % (chan, self.names[chan])
        self.factory.names = self.names
        self.channels = self.factory.channels

    def irc_unknown(self, prefix, command, params):
        "Print all unhandled replies, for debugging."
        return
        # print 'UNKNOWN:', prefix, command, params

    def userJoined(self, user, chan):
        if chan in self.names:
            self.names[ chan ].append( user )
        print ' -- %s has joined %s' % (user,chan)

    def userLeft(self, user, chan):
        if chan in self.names:
            self.names[ chan ].remove( user )
        print ' -- %s has left %s' % (user,chan)

    def userQuit(self, user, reason):
        for n in self.names:
            if user in self.names[n]:
                self.names[ n ].remove( user )
        print ' -- %s has quit (Client Exited.)' % user

    def userKicked(self, user, chan, kicker, reason):
        if chan in self.names:
            self.names[ chan ].remove( user )
        print ' -- %s kicked %s from %s [[ %s ]]' % (kicker,user,chan,reason)
        
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
