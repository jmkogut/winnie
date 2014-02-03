from winnie import model

from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

class EchoWS(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.factory.irc.send_ctrl_msg("WebSocket opened at %s"%(request.peer))
        self.factory.register( self )


    def onOpen(self):
        print("WebSocket connection open.")
        self.send_names()
        self.send_recent()

    def send_names(self):
        names_json = '{"irc_names": [ %s ]}' % ', '.join(['"%s"'%s for s in
            self.factory.irc.names[self.factory.irc.channels[-1]]])
        self.sendMessage( names_json, False )
        print 'names :: %s' % (names_json,)

    def send_recent(self, count=20):
        print ' -- sending %s latest messages'%(count,)
        q = model.session.query(model.Intel)
        for i in q[count:]:
            msg = '{"irc_event": "<%s> %s: %s" }' % (
                i.target, i.user.nick, i.text
            )
            # print ' event :: %s ' % (msg,)
            self.sendMessage( msg.encode('ascii'), False )

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.irc.send_ctrl_msg("WebSocket closed :: %s"%(reason))
        self.factory.unregister( self )

    def onMessage(self, m, b):
        print("Text message received: {0}".format(m.decode('utf8')))
        self.factory.irc.send_ctrl_msg("<- ws msg :: %s"%(m))
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

    def send_msg(self, msg):
        for c in self.clients:
            c.sendMessage(msg, False)
