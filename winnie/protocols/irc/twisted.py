"""
Communication class
"""

import random


from winnie.protocols.irc import responders
from winnie.util.singletons import Singleton
from winnie.data.cache import Client
from winnie.data import model
from winnie import settings
from winnie.util.logger import Logger
logger = Logger()

from types import TupleType

from datetime import datetime
import hashlib
import Queue

from irclib import nm_to_n


# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor
from twisted.internet import protocol


class WinnieEvent(object):
    def __init__(self, source, target, message):
        self._source = self.user = source
        self._target = self.channel = target
        self.message = message

    def source(_): return _._source
    def target(_): return _._target

class WinnieEvents(irc.IRCClient):
  def init_handlers(self):
    self.handler = responders.Handler(self)
    self.processor = responders.Processor(self) 
    self.processor.start()
    
  def signedOn(s):
    s.init_handlers()

    [s.join(channel) for channel in s.factory.channels] 
    print "joined %s"%s.factory.channels

  def left(s,chan): 
      pass

  def joined(s,chan):
      print 'joined %s'%chan

  def privmsg(s,  usr, chan, msg):
    s.respond(usr, chan, msg)

  def respond(self, user, chan, msg):
    print '%s: %s | %s'%(user, chan, msg)

  def queuemsg(self, target, msg):
    self.msg(target, msg)

class WinnieFactory(protocol.ClientFactory):
  protocol = WinnieEvents
  def __init__(self):
    self.channels = self.factory.channels
    self.nickname = self.nick = self.factory.nicks[0]

  def clientConnectionLost(s,connector,reason):
    print 'lost con (%s), reconnecting' % (reason,)
    connector.connect()

  def clientConnectionFailed(s,connector,reason):
    print 'con failed: %s' % (reason,)


class Connection(object):
    """
    The IRC connection handler / intelligence gathering mechanism for winnie
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.nicks, self.address = settings.IRC
        self.channels = settings.IRC_CHANNELS
        self.mc = self.c = Client(self.nicks[0])

        # Channel related things
        self.c.modes = {}

        self.credentials = settings.IRC_CREDENTIALS
        
        self.output = Queue.Queue(20)

        self.c.verbosity = settings.VERBOSITY

        self.init_responders()

    def start(self):
        host, port = self.address
        reactor.connectTCP(host, port, WinnieFactory())
        reactor.run()


    def on_welcome(self, _connection, _event):
        """
        Initial server welcome message, join all channels
        """
        logger.info("Received welcome.")

        # try to authenticate
        self.auth()

        to_join = self.c.to_join or []
        logger.info("Joining %s channels"%len(to_join))

        while len(to_join) > 0:
            chan = to_join.pop()
            if chan not in (None, '', self.nick):
                self.join(chan)

        # Set mode +B to show that we are a bot
        self.connection.send_raw("MODE %s +B"%self.nick)

        self.processor.start()
    
    def queuemsg(self, event, target, phrase):
        """
        A local wrapper to connection.privmsg

        This wrapper adds a typing delay, improves grammar, performs replies,
        then sends the message out.
        """

        if phrase is None or len(phrase) is 0:
            return

        phrase = phrase.replace("$who", nm_to_n(event.source()))
        phrase = phrase.replace(self.nick+' ', 'I ').replace('I is', 'I am')
        phrase = phrase.lstrip('10')
        
        # If any statement contains <reply> we only say what comes
        # after it.
        index = phrase.lower().find('<reply>')
        if index > -1:
            self.queuemsg(
                event,
                target,
                "%s" % (
                    phrase[index+7:].strip()
                )
            )

            return
        
        if (target == self.nick):
            target = nm_to_n(event.source())

        self.output.put((target,phrase))

    def privmsg(self, target, phrase):
        """
        Sends a private message to the target
        """
        self.log((target, phrase))
        self.connection.privmsg(target, phrase)

    def on_invite(self, connection, event):
        print event.arguments
        self.message_handler(connection, event)



    def on_pubmsg(self, connection, event):
        """
        On every pubmsg received
        """
        self.message_handler(connection, event)
        print event

    def on_privmsg(self, connection, event):
        """
        On every private message received
        """
        self.message_handler(connection, event)
        print event

    def log(self, thing, urgency='sys'):
        """
        Pretty format log messages
        TODO: refactor it out that's what the fucking logger class is for
        TODO: make work
        """
        t = type(thing)

        # An intelligence learned
        if '__dict__' in dir(t) and t.__name__ == 'intelligence':
            logger.learned(thing.message)

        # An outgoing message
        elif t is TupleType and len(thing) is 2:
            target, phrase = thing
            logger.outgoing("%s/%s> %s" % (target, self.nick, phrase))

        # If this is an IRC event
        elif 'timestamp' in dir(thing):
            target, source, phrase = (thing.target(), nm_to_n(thing.source()), thing.message)
            logger.incoming("%s/%s> %s" % (target, source, phrase))

        else: #It's just a string
            logger.info(thing)

    def message_handler(self, connection, event):
        """
        Send events off to the responders
        """
        event.timestamp = datetime.now()
        event.ref = hashlib.md5(event.timestamp.isoformat()).hexdigest()[0:5]
        event.message = event.arguments()[0].strip()
        self.add_history(event)
        self.log(event)

        #print "EVENT REF %s \"%s\" " % (event.ref, event.message)
        logger.info(event.message)

        if event.eventtype() == 'invite':
            self.join(event.message)

#        print event.message

        self.handler.handle(connection, event)

    def start(self):
        host, port = self.address
        reactor.connectTCP(host, port, WinnieFactory())
        reactor.run()

    def add_history(self, event):
        # Max history hardcoded
        max = 40
        
        history = self.get_history(event.target())

        if len(history) is max: history.pop()
        history.insert(0, event_to_dict(event))

        self.set_history(event.target(), history)

    def auth(self):
        """
        Attempt server authentication
        """
        logger.info("Attempting to auth to %s"%self.credentials['authority'])
        
        if self.credentials is not None:
            self.privmsg (
                self.credentials['authority'],
                self.credentials['command'] % self.credentials['creds'] )


    def join(self, channel):
        """
        Join in on a channel
        """
        logger.info("Attempting to join %s"%channel)

        if channel not in [chan for chan in self.channels]:
            logger.add("channel %s" % channel)
            self.connection.join(channel)

    def part(self, channel):
        """
        Storm out of a channel
        """
        if channel in [c for c in self.channels]:
            self.log("Parting %s" % channel)
            self.connection.part(channel)

    def get_history(self, channel):
        try:
            return self._history[channel]
        except KeyError, e:
            return []

    def set_history(self, channel, history):
        self._history[channel] = history


def event_to_dict(event):
    return {
        'target': event.target(),
        'source': event.source(),
        'type': event.eventtype(),
        'timestamp': event.timestamp.isoformat(),
        'arguments': event.arguments(),
        'ref': event.ref
    }

# class ConnectionModel:
#     """
#     Holds a few data classes for the communicator
#     """
#     class channel(model.WinnieList):
#         class model(model.WinnieObject):
#             def __init__(self, name):
#                 self.name=name
#             def ref(self):
#                 return self.name
#     
#         select = classmethod(lambda cls: [cls.model(chan) for chan in Connection().channels])
#  
#     class log(model.WinnieList):
#         class model(model.WinnieObject):
#             def __init__(self,line):
#                 self.line = line
# 
#             def ref(self):
#                 return self.line
# 
#         @classmethod
#         def selectBy(cls, channel=None, since=None):
#             c = Connection() # Get the connection
#             history = c.get_history(channel)
#             
#             send = []
# 
#             for event in history:
#                 if event['ref'] == since: return send
#                 send.append(event)
# 
#             return send
# 
#     class server(model.WinnieList):
#         class model(model.WinnieObject):
#             def __init__(self,server,port):
#                 self.server = server
#                 self.port = port
#             def ref(self):
#                 return (self.server,self.port)
# 
#         select = classmethod(lambda cls: [cls.model(*server) for server in Connection().server_list])
# 
