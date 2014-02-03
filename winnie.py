import sys

import logging
from twisted.python import log
from twisted.python import logfile

from twisted.internet import protocol, reactor
from twisted.web import server

from winnie import irc
from winnie import websocket as ws
from winnie.web import Site
from winnie import log as Log

import config as cfg

# ////////////////////////////

if __name__ == "__main__":
    # Logfile
    f = logfile.LogFile("winnie.log", cfg.APP_DIR+'/', rotateLength=9999999999,
            maxRotatedFiles=999 )
    logger = Log.LevelFileLogObserver(f, logging.DEBUG)
    log.addObserver(logger.emit)

    # IRC client connection
    factory = irc.IRCClientFactory( cfg.IRC_CHANNELS, config=cfg )
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
