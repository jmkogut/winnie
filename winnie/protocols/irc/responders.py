from winnie import settings
from winnie.data.model import *
from winnie.util import log, debug

import time
import random
import threading
import traceback
from types import *

class Processor(threading.Thread):
    """
    This thread sits alongside the IRC client and polls the output
    buffer for messages to send. When it's occupied it cycles through
    and sends them as fast as it can type.

    After polling, it'll try to do any other jobs it can (currently
    just statistics collecting)
    """

    def __init__(self, communicator):
        self.com = communicator
        self.c = self.com.c

        threading.Thread.__init__(self)

    def run(self):
        """
         The main app thread sets this to False when a keyboard interrupt is received
         """
        self.running = True
        
        # Continually run, checking for listeners and filling stats then sending output
        while self.running:
            self.fill_stats()
            self.check_output()

            # Pause for half second
            time.sleep(0.5)

    def check_output(self):
        """
        Polls the bot's content buffer and sends out anything in the queue
        """
        # If the buffer has content
        output = self.c.output

        if len(output) > 0:
            # Do this as long as it has content
            while len(output) > 0:
                # Unpack this message, calculate delay, pause for appropriate time
                (target, phrase) = output.pop()                
                delay = (len(tuple(phrase))*1.0 / settings.TYPING_SPEED*1.0) * 60
                time.sleep( delay )
                
                # Send off the message
                self.com.privmsg(target, phrase)

            self.c.output = output
    
    def fill_stats(self):
        """
        If there are any listeners, it fills the statistics cache
        """
        listeners = self.c.listeners or 0
        if listeners:
            # TODO: rework how stats are cached
            self.com.c.stats = {
                'factoids': intelligence.select().count(),
                'channels': [channel for channel in self.com.channels]
            }
            
            # Every active listener increments this, decrement it for justice!
            self.com.c.listeners -= 1

def CommandHandler(to_wrap, **kwargs):
    """
    First up, I apologize to anyone that has to read this.

    Second, this is a Python decorator that can support an optional
    keyword argument or any amount of them, really.

    The standard method for argument decorators doesn't allow
    for the decorator to be called /without any arguments/

    This does.
    """

    if 'require' in kwargs:
        require_trust = (kwargs['require'] == 'trust')
    else:
        require_trust = False
        
    def wrapper(*args, **kwargs):
        method = to_wrap or kwargs['method']
        self, connection, event = args
        
        allowed = not require_trust or event.source() in settings.TRUSTED_USERS
        
        # These next two blocks are hideous, refactor
        params = (
            event.source().split('!')[0],   # User nick
            method.__name__,                # method name
            event.arguments()[0]            # user message
        )

        if allowed:
            self.com.log("%s called %s with %s"%(params))
            try:
                resp = method(*args)
            except Exception, e:
                self.com.log('----------------')
                print dir(e)
                traceback.print_exc(e)
                self.com.log('----------------')
                resp = "Error: %s" % (e.message or e.__repr__())
        else:
            self.com.log("%s was denied access to %s"%(params[:2]))
            resp = "You are not allowed access"

        if resp and len(resp) > 0:
            self.com.queuemsg(event, event.target(), self.com.response('to_someone', resp))
    wrapper.__setattr__('is_handler', True)

    def wrapper_args(method):
        def wrapped_f(*pargs):
            return wrapper(pargs[0], pargs[1], pargs[2], method=method)
        wrapped_f.__setattr__('is_handler', True)
        return wrapped_f

    if to_wrap:
        return wrapper
    else:
        return wrapper_args

"""
To allow usages like

    @handler(require_trust=True)
    def help_handler(self):
        pass
"""
handler = CommandHandler


class Handler(object):
    """
    winnie takes every message and sends it to an instance of this class

    The handler class encapsulates all of the response methods, in order
    to make them easier to dynamically update. It's as simple as
    
        reload(responders)

    """

    def __init__(self, com):
        self.com = com
        self.com.log("Starting Responder.")
        self.c = self.com.c

        self.handler_prefix = settings.HANDLER_PREFIX
        self.handlers = {}
        self.find_handlers()
    
    def find_handlers(self):
        """
        Looks through all the attributes of this class and
        saves the event handlers to a dictionary
        """
        for i in dir(self):
            if 'is_handler' in dir(self.__getattribute__(i)) and self.__getattribute__(i).is_handler:
                self.handlers[i.split('_')[0]] = self.__getattribute__(i)


    
    @handler(None, require='trust')
    def die_handler(self, connection, event):
        self.com.die()

    @handler
    def channels_handler(self, connection, event):
        message = event.arguments()[0].split(' ')

        if len(message) > 1:
            command = message[1]
        else:
            command = 'list'

        self.com.update_channels()

        if command == 'list':
            return "%s" % [channel for channel in self.com.channels]

        elif command in ('join', 'enter'):
            if len(message) > 2:
                self.com.join(message[2])
            else:
                return "I need a channel name."
        elif command in ('part','leave'):
            if len(message) > 2:
                self.com.part(message[2])
            else:
                return "I need a channel name."

        self.com.update_channels()

    @handler
    def help_handler(self, connection, event):
        message = event.arguments()[0].split(' ')

        if len(message) > 1:
            command = message[1]
        else:
            command = 'list'

        if command == 'list':
            return "Command list is %s" % (", ".join(
                ["%s%s" % (self.handler_prefix, c) for c in self.handlers]
            ))
    
    @handler
    def mode_handler(self, connection, event):
        message = event.arguments()[0].split(' ')

        if len(message) > 1:
            command = message[1]
        else:
            command = 'show'

        if command == 'show':
            mode = self.get_mode(event.target())
            debug(mode)
            statement = "I am in %s mode" % mode
            debug(statement)
            return statement
        elif command in ('shush', 'speak'):
            self.set_mode(event.target(), command)
            return "Set mode to %s" % command

    @log
    def get_mode(self, channel):
        modes = self.c.modes
        if type(modes) != DictType or channel not in modes:
            self.set_mode(channel, 'shush')
            modes = self.c.modes
        
        return modes[channel]
    @log
    def set_mode(self, channel, mode):
        if mode in ('shush', 'speak'):
            modes = self.c.modes
            if type(modes) is not DictType: modes = {}
            modes[channel] = mode
            self.c.modes = modes
            print self.c.modes

        return "Going into %s mode" % mode

    @handler(None, require='trust')
    def reload_handler(self, connection, event):
        self.com.reload()
        
        # TODO: reload model
        #reload(model)
        return "Reloaded responder engine."


    @handler(None, require='trust')
    def update_handler(self, connection, event):
        self.com.update_phrases()
        return "Updated responses."
            
    @handler
    def verbosity_handler(self, connection, event):
        message = event.arguments()[0].split(' ')

        if len(message) is 1:
            return "Verbosity is %s." % self.c.verbosity
        else:
            i = int(message[1])
            if i in range(0,100):
                self.c.verbosity = i
                return "Set verbosity to %s." % self.c.verbosity
            else:
                return "Verbosity must be between 0 and 100."

    @handler(None, require='trust')
    def set_handler(self, connection, event):
        message = event.arguments()[0].split(' ', 2)

        if len(message) is not 3:
            return "Usage is %sset [key] [value]." % self.handler_prefix
        else:
            if (self.c.__setattr__(message[1], message[2])):
                return "Noted."

    @handler
    def get_handler(self, connection, event):
        message = event.arguments()[0].split(' ')

        if len(message) is not 2:
            return "Usage is %sget [key]." % self.handler_prefix
        else:
            value = self.c.__getattr__(message[1])
            if value:
                return "%s is %s." % (message[1], value)
            else:
                return "I dunno."

    @handler
    def whoami_handler(self, connection, event):
        message = event.arguments()[0].split(' ')

        if len(message) is not 1:
            return "Usage is %swhoami" % self.handler_prefix
        else:
            return "You are %s"%event.source()


    @handler(None, require='trust')
    def run_handler(self, connection, event):
        message = event.arguments()[0].split(' ', 1)

        if len(message) is not 2:
            return "Usage is %srun [code]." % self.handler_prefix
        else:
            self.com.log("EVALING CODE: %s"%message[1], 'notice')
            
            value = None
            if '=' in message[1]:
                exec message[1]
            else:
                value = eval(message[1], globals(), locals())

            if not value == None:
                return "Returned: %s" % value

    def roll_speak(self, channel):
        if channel in self.c.modes and self.c.modes[channel] == 'speak' and random.choice(range(0,100)) < self.c.verbosity:
            return True
        return False

    def handle(self, connection, event):
        try:
            for handler in self.handlers.keys():
                if event.arguments()[0].startswith("%s%s" % (self.handler_prefix,handler)):
                    self.handlers[handler](connection, event)
                    return
            
            self.map_reply(connection, event)

        except Exception, e:
            traceback.print_exc(e)
            self.com.init_responders()
        finally:
            pass


    def map_reply(self, connection, event):
        message = event.arguments()[0]
        
        # Basically returns if a statement like 'x is/are/was/has a cat'
        is_indicated = self.indicated(message)

        # Verify that someone made an indication, and that it doesn't end in the indicator
        if is_indicated and len(is_indicated[1]) > 1:
            query =  intelligence.select(intelligence.q.keyphrase==is_indicated[1][0])

            # If this intelligence doesn't exist already
            if query.count() == 0:
                # We just learned something
                self.new_intelligence(event, is_indicated)
            
            # If we've already heard this before
            else:
                # Has this exact statement been said before?
                if is_indicated[1][1] == query[0].value:
                    statement = self.com.response('rebuttal', event.source().split('!')[0])
                # If he's conflicting what we already know
                else:
                    # TELL HIM OFF & learn
                    statement= self.com.response('preconception',
                        query[0].keyphrase,
                        query[0].indicator,
                        query[0].value
                    )
                    f = self.new_intelligence(event, is_indicated)                       
                    
                    if self.roll_speak(event.target()):
                        self.com.queuemsg(event, event.target(), statement)

        # Nothing indicated, let's do a search mang
        elif self.roll_speak(event.target()):
            result = search_intelligence(message)
      
            if result:
                 # If something matches that phrase:
                self.com.queuemsg(
                    event,
                    event.target(),
                    self.com.response('statement',
                        result.keyphrase,
                        result.indicator,
                        result.value
                    )
                )
           
            
                result.lastused = datetime.now()

    """
    Looks through the phrase for the existance of any thing like
        'john is a fag'
    and will return ('is', ['john', 'a fag'])
    """
    def indicated(self, message):
        # Don't log questions now
        if message.endswith('?') and not message.endswith('\\?'):
            return None

        # If it starts with an interrogative, don't add it
        for v in self.com.interrogatives:
            if message.startswith(v):
                return None
        
        message = message.lstrip('\\')

        split = message.split(' ')
        for i in self.com.indicators:
            for s in split:
                if i == s:
                    return (i, [s.strip() for s in message.split(' %s '%i, 1)])

        return None

    """
    Creates a new intelligence
    """
    def new_intelligence(self, event, is_indicated, save=True):
        if save:
            i = intelligence(
                mask = event.source(),
                keyphrase = is_indicated[1][0],
                value = is_indicated[1][1],
                indicator = is_indicated[0],
                created=event.timestamp
            )

            self.com.log(i)
        else:
            self.com.log("Did not save intelligence.", urgency="notice")

        return i
