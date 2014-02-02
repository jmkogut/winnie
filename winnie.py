import sys
from twisted.words.protocols import irc

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

from twisted.web.template import Element, renderer, XMLFile
from twisted.web import server, resource
from twisted.web.static import File

from mako.template import Template
from mako.lookup import TemplateLookup

from twisted.internet import protocol, reactor

import os
from twisted.python.rebuild import rebuild
import process

class Handler(object):
    filename = os.getcwd() + "/process.py"
    lastmodified = None
    instance = None

    def getModified(self):
        return os.stat(self.filename).st_mtime

    def loader(self):
        print "Rebuilding process."
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
        self.join(self.factory.channel)
        print " -- Signed on as [%s]" % (self.nickname,)
 
    def joined(self, channel):
        print ' -- Joined %s' % (channel)
 
    def privmsg(self, user, channel, msg):
        # Send this privmsg off to the Handler
        self.handler.get().irc( source=user, target=channel, text=msg )
        

class IRCClientFactory(protocol.ClientFactory):
    protocol = IRCClient
    def __init__(self, channel, nickname='winnie'):
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


# ////////////////////////////

app_dir      = os.path.dirname(__file__)
static_dir   = os.path.join(app_dir, 'web.static')
template_dir = os.path.join(app_dir, 'web.tpl')

lookup = TemplateLookup(directories=[template_dir],
                                        input_encoding='utf-8',
                                        output_encoding='utf-8')

class WebUI(resource.Resource):
    isLeaf = True
    def __init__(self):
        resource.Resource.__init__(self)
        self.putChild('static', File('web.static'))

    def getChild(self, name, req):
        print 'getChild'
        if name == '': return self
        return resource.Resource.getChild(self, name, req)

    def render_GET(self, req):
        print 'render'
        tpl = lookup.get_template('demo.mako')
        return tpl.render(page={
            'app_title': "lolhaxs",
            'page_title': "fooo"
        })

# ////////////////////////////

class EchoWS(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.factory.irc.send_msg("WebSocket opened at %s"%(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage("welcome", False)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.irc.send_msg("WebSocket closed at %s"%(request.peer))

    def onMessage(self, m, b):
        print("Text message received: {0}".format(m.decode('utf8')))
        self.factory.irc.send_msg("<- ws msg :: %s"%(m))
        self.sendMessage(m, b)

class WSFactory(WebSocketServerFactory):
    protocol = EchoWS

    def __init__(self, uri='ws://localhost'):
        WebSocketServerFactory.__init__(self, uri)
        self.clients = []

    def register(self, client):
        if not client in self.clients:
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            self.clients.remove(client)

    def send_all(self, msg):
        for c in self.clients:
            c.sendMessage(msg, False)


# ////////////////////////////

if __name__ == "__main__":

    # IRC client connection
    factory = IRCClientFactory('#bots')
    reactor.connectTCP('irc.subluminal.net', 6667, factory)

    # HTTP interface
    root = resource.Resource()
    root.putChild("",       WebUI())
    root.putChild("static", File(static_dir))
    site = server.Site(root)
    reactor.listenTCP(8080, site)
    print ' -- HTTP int listening on port 8080'

    # WebSocket interface
    wsf = WSFactory("ws://abzde.com:8888", debug=False)
    wsf.protocol = EchoWS
    wsf.irc = factory
    factory.wsf = wsf
    reactor.listenTCP(8888, wsf) 
    print ' -- WebSocket int listening on port 8888'

    reactor.run()
