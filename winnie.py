import sys

from twisted.internet import protocol, reactor
from twisted.web import server

from winnie import irc
from winnie import websocket as ws
from winnie.web import Site

import config as cfg

# ////////////////////////////

if __name__ == "__main__":
    # IRC client connection
    factory = irc.IRCClientFactory( cfg.CMD_CHAN )
    reactor.connectTCP( cfg.IRC_HOST, cfg.IRC_PORT, factory)

    # HTTP interface
    site = server.Site(Site)
    reactor.listenTCP( cfg.HTTP_PORT, site)
    print ' -- HTTP int listening on port %s'%(cfg.HTTP_PORT,)

    # WebSocket interface
    wsf = ws.WSFactory( 'ws://%s:%s'%(cfg.HOST, cfg.WS_PORT) )
    wsf.irc = factory
    factory.wsf = wsf
    reactor.listenTCP(cfg.WS_PORT, wsf) 
    print ' -- WebSocket int listening on port %s'%(cfg.WS_PORT,)

    reactor.run()
