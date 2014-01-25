import sys
from twisted.words.protocols import irc
from twisted.web import server, resource
from twisted.internet import protocol, reactor
    
class Home(resource.Resource):
    isLeaf = True
    def __init__(self, irc_factory):
        self.irc_factory = irc_factory
 
    def render_GET(self, request):
        self.factory.send_msg("HTTP Access!")
        return "<html>Welcome Home!</html>"

class TalkBot(irc.IRCClient):
    # The method below allows us to get the nickname from the factory
    def _get_nickname(self):
        return self.factory.nickname
    nickname = property(_get_nickname)
 
    def connectionMade(self):
        # Since we override this method, we need to call the IRCClient one as well
        irc.IRCClient.connectionMade(self)
 
        # Add this instance to the client list
        self.factory.clients.append(self)
 
    def signedOn(self):
        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)
 
    def joined(self, channel):
        print "Joined %s." % (channel,)
 
    def privmsg(self, user, channel, msg):
        print "#" + channel + " <" + user + "> " + msg


class TalkBotFactory(protocol.ClientFactory):
    protocol = TalkBot
    def __init__(self, channel, nickname='talkbot'):
        self.channel = channel
        self.nickname = nickname
        self.clients = []
 
    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()
 
    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)
 
    def send_msg(self, msg):
        for client in self.clients:
            client.say(self.channel, msg)


if __name__ == "__main__":
    factory = TalkBotFactory('#bots')
    site = server.Site(Home(factory))
    reactor.listenTCP(8080, site)
    reactor.connectTCP('irc.subluminal.net', 6667, factory)
    reactor.run()
