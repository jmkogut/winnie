"""
Communication class
"""

import random

from ircbot import SingleServerIRCBot

from winnie.protocols.irc import responders

from winnie.util.logger import Logger
logger = Logger()

from winnie.util.singletons import Singleton

from winnie.data.cache import Client
from winnie.data import model
from winnie import settings

from irclib import nm_to_n

from types import TupleType

from datetime import datetime
import hashlib
import Queue

def event_to_dict(event):
    return {
        'target': event.target(),
        'source': event.source(),
        'type': event.eventtype(),
        'timestamp': event.timestamp.isoformat(),
        'arguments': event.arguments(),
        'ref': event.ref
    }

class ConnectionModel:
    """
    Holds a few data classes for the communicator
    """
    class channel(model.WinnieList):
        class model(model.WinnieObject):
            def __init__(self, name):
                self.name=name
            def ref(self):
                return self.name
    
        select = classmethod(lambda cls: [cls.model(chan) for chan in Connection().channels])
 
    class log(model.WinnieList):
        class model(model.WinnieObject):
            def __init__(self,line):
                self.line = line

            def ref(self):
                return self.line

        @classmethod
        def selectBy(cls, channel=None, since=None):
            c = Connection() # Get the connection
            history = c.get_history(channel)
            
            send = []

            for event in history:
                if event['ref'] == since: return send
                send.append(event)

            return send


    class server(model.WinnieList):
        class model(model.WinnieObject):
            def __init__(self,server,port):
                self.server = server
                self.port = port
            def ref(self):
                return (self.server,self.port)

        select = classmethod(lambda cls: [cls.model(*server) for server in Connection().server_list])

class Connection(object, SingleServerIRCBot):
    """
    The IRC connection handler / intelligence gathering mechanism for winnie
    """

    __metaclass__ = Singleton

    def __init__(self):
        """
        Setup the robot, pulls a list of the latest phrases from the DB,
        sets channel list and modes.
        """

        self.nicks, address = settings.IRC
        self.nick = self.nicks[0]

        SingleServerIRCBot.__init__(self, [address], self.nick, self.nick)
    
        self.c = Client(self.nick)

        # Channel related things
        self.c.modes = {}

        # Channel history
        self._history = {}

        self.c.to_join = [c for c in settings.IRC_CHANNELS]
        
        self.output = Queue.Queue(20)

        self.c.verbosity = settings.VERBOSITY

        self.processor = None
        self.handler = None
        
        self.init_responders()

    def init_responders(self):
        """
        Spawns the responders
        """
        # Sends messages from the outgoing queue
        self.processor = responders.Processor(self)

        # Generates responses, learns intel
        self.handler = responders.Handler(self)

    def reload(self):
        """
        Reloads and restarts responders
        """
        reload(responders)
        self.init_responders()


    def on_welcome(self, _connection, _event):
        """
        Initial server welcome message, join all channels
        """
        logger.info("Received welcome.")

        to_join = self.c.to_join or []
        logger.info("Joining %s channels"%len(to_join))

        while len(to_join) > 0:
            chan = to_join.pop()
            if chan not in (None, '', self.nick):
                self.join(chan)
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

    def on_pubmsg(self, connection, event):
        """
        On every pubmsg received
        """
        self.message_handler(connection, event)

    def on_privmsg(self, connection, event):
        """
        On every private message received
        """
        self.message_handler(connection, event)

    def log(self, thing, urgency='sys'):
        """
        Pretty format log messages
        TODO: refactor it out that's what the fucking logger class is for
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

        self.handler.handle(connection, event)

    def add_history(self, event):
        # Max history hardcoded
        max = 40
        
        history = self.get_history(event.target())

        if len(history) is max: history.pop()
        history.insert(0, event_to_dict(event))

        self.set_history(event.target(), history)

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

