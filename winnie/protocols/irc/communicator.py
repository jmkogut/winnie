from ircbot import SingleServerIRCBot

import responders

from winnie.util import debug
from winnie.data.cache import Client
from winnie.data.model import *
from winnie import settings

from irclib import nm_to_n

from types import TupleType

class Communicator(object, SingleServerIRCBot):
    """
    The IRC connection handler / intelligence gathering mechanism for winnie
    """

    def __init__(self):
        """
        Setup the robot, pulls a list of the latest phrases from the DB,
        sets channel list and modes.
        """

        self.nick, address = settings.IRC
        SingleServerIRCBot.__init__(self, [address], self.nick, self.nick)
    
        self.c = Client(self.nick)

        self.update_phrases()

        self.init_responders()

        # Channel related things
        self.c.log = []
        self.c.channels = []
        self.c.modes = {}

        self.c.output = []
        self.c.to_join = [c for c in settings.IRC_CHANNELS]

        self.c.verbosity = settings.VERBOSITY

    def update_phrases(self):
        """
        Caches phrases that we're going to need so no future
        DB lookups are needed for them
        """
        for category in [phrase.category for phrase in phrase_category.select()]:
            l = phrase_list(category)
            self.__dict__[category+'s'] = l
            self.log("%s: %s" % (category, l))

    def response(self, category, message):
        """
        Returns a preformatted response
        """
        if message is None or len(message) is 0:
            return None

        return random.choice(self.__dict__[category+'s']) % message

    def init_responders(self):
        self.processor = responders.Processor(self)    # Sends messages from the outgoing queue
        self.handler = responders.Handler(self)        # Response engine for phrases

    def reload(self):
        """
        Reloads responder module
        """
        reload(responders)
        self.init_responders()


    def on_welcome(self, connection, event):
        """
        Initial server welcome message, join all channels
        """
        to_join = self.c.to_join or []
        while len(to_join) > 0:
            chan = to_join.pop()
            if chan not in (None, '', self.nick):
                self.join(chan)

        self.processor.start()
    
    def queuemsg(self, event, target, phrase, pause=True):
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

        replyIndex = phrase.lower().find('<reply>')
        if replyIndex > -1:
            self.queuemsg(
                event,
                target,
                "%s" % (
                    phrase[replyIndex+7:].strip()
                )
            )

            return
        
        if (target == self.nick):
            target = nm_to_n(event.source())

        output = self.c.output
        output.insert(0, (target, phrase))
        self.c.output = output

        self.log("Added output")

    def privmsg(self, target, phrase):
        self.log((target, phrase))
        self.connection.privmsg(target, phrase)

    def on_pubmsg(self, connection, event):
        self.message_handler(connection, event)

    def on_privmsg(self, connection, event):
        self.message_handler(connection, event)

    def log(self, thing, urgency='sys'):
        t = type(thing)

        # An intelligence learned
        if '__dict__' in dir(t) and t.__name__ == 'intelligence':
            debug("Discovered: %s [%s] %s" % (
                thing.keyphrase,
                thing.indicator,
                thing.value
            ), thing.created, 'add')
        # An outgoing message
        elif t is TupleType and len(thing) is 2:
            target, phrase = thing
            debug("[%s] %s> %s" % (
                target,
                self.nick,
                phrase
            ), urgency='out')
        # If this is an IRC event
        elif 'timestamp' in dir(thing):
            debug("[%s] %s> %s" % (
                thing.target(),
               nm_to_n(thing.source()),
                thing.arguments()[0]
            ), thing.timestamp, 'in')
        else: #It's just a string
            debug(thing, urgency=urgency)

    def message_handler(self, connection, event):
        event.timestamp = datetime.now()
        self.log(event)
        self.handler.handle(connection, event)

    def update_channels(self):
        chans = [chan for chan in self.channels]
        print "Chanlist: %s"%chans
        self.c.channels = chans

    def join(self, channel):
        if channel not in [chan for chan in self.channels]:
            self.log("Joining %s" % channel)
            self.connection.join(channel)

    def part(self, channel):
        self.update_channels()
        if channel in [c for c in self.channels]:
            self.log("Parting %s" % channel)
            self.connection.part(channel)
