from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                       WebSocketServerFactory

class EchoWS(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        self.factory.irc.send_ctrl_msg("WebSocket opened at %s"%(request.peer))
        self.factory.register( self )

    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage("welcome", False)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
        self.factory.irc.send_msg("WebSocket closed :: %s"%(reason))
        self.factory.unregister( self )

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

    def send_msg(self, msg):
        for c in self.clients:
            c.sendMessage(msg, False)
