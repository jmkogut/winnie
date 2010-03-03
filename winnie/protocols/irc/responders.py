"""
Contains the processes in charge of responding to input
"""

from winnie import settings
from winnie.data import model

from winnie.util.logger import Logger
logger = Logger()

from winnie.lexer import Lexer

import md5
import time
import random
import threading
import traceback

from types import DictType
from irclib import nm_to_n
from datetime import datetime

class Processor(threading.Thread):
    """
    This thread sits alongside the IRC client and polls the output
    buffer for messages to send. When it's occupied it cycles through
    and sends them as fast as it can type.
    """

    def __init__(self, communicator):
        self.com = communicator
        self.running = True

        threading.Thread.__init__(self)

    def run(self):
        """
         The main app thread sets this to False when a keyboard interrupt is received
         """
       
        # Continually run, checking for listeners and filling stats then
        #sending output
        while self.running:
            self.send_queue()

            # Pause for half second
            time.sleep(0.25)

    def send_queue(self):
        """
        Polls the bot's content buffer and sends out anything in the queue
        """
        while not self.com.output.empty():
            # Unpack this message, calculate delay, pause for appropriate
            # time
            (target, phrase) = self.com.output.get()
            
            # TODO: enable delay for certain things
            
            # Send off the message
            self.com.privmsg(target, phrase)

def handler(*args, **kwargs):
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
    
    to_wrap = args[0] if len(args) > 0 else None
    default_docstring = "No documentation provided."

    def wrapper(*args, **kwargs):
        """wrapper"""
        method = to_wrap or kwargs['method']

        self, _connection, event = args

        allowed = not require_trust or event.user.trusted
        
        # These next two blocks are hideous, refactor
        params = (
            nm_to_n(event.source()),        # User nick
            method.__name__,                # method name
            event.arguments()[0]            # user message
        )

        if allowed:
            try:
                resp = method(*args)
            except Exception, e:
                print '== Exception------'
                traceback.print_exc(e)
                print '== ---------------'

                resp = "Error: %s" % e
            finally:
                pass
        else:
            logger.info("%s was denied access to %s"%(params[:2]))
            resp = "You are not allowed access"

        if resp is not None:
            self.com.queuemsg(
                event,
                event.target(),
                "$who: "+resp.strip()
            )

    wrapper.__setattr__('is_handler', True)

    def wrapper_args(method):
        """wrapper"""
        def wrapped_f(*pargs):
            """wrapper"""
            return wrapper(pargs[0], pargs[1], pargs[2], method=method)
        wrapped_f.__setattr__('is_handler', True)
        wrapped_f.__setattr__('__doc__', "wrapped_f: "+method.__doc__.strip() if method.__doc__ else default_docstring)
        return wrapped_f

    if to_wrap:
        wrapper.__setattr__('__doc__', "wrapper: "+to_wrap.__doc__.strip() if to_wrap.__doc__ else default_docstring)
        return wrapper
    else:
        wrapper_args.__doc__ = "wrapper_args docs!"
        return wrapper_args

class Handler(object):
    """
    winnie takes every message and sends it to an instance of this class

    The handler class encapsulates all of the response methods, in order
    to make them easier to dynamically update. It's as simple as
    
        reload(responders)

    """

    def __init__(self, com):
        self.com = com
        logger.info("Starting Responder.")
        self.c = self.com.c

        self.handler_prefix = settings.HANDLER_PREFIX
        self.handlers = {}
        self.find_handlers()
        
        # TODO: fix what these call to return None if nothing {
        self.modes = {}
        self.default_mode = 'mimic'

        self.modes['shush'] = lambda _: None
        self.modes['mimic'] = lambda event: self.search(event.keywords, limit=1).use()

        self.markov_table = {}
        self.modes['markov-fresh'] = lambda event: self.markov_from(event.arguments()[0], None)
        self.modes['markov-cumulative'] = lambda event: self.markov_from(event.arguments()[0], self.markov_table)
        # }

    
    def find_handlers(self):
        """
        Looks through all the attributes of this class and
        saves the event handlers to a dictionary
        """
        for i in dir(self):
            if 'is_handler' in dir(self.__getattribute__(i)) \
                and self.__getattribute__(i).is_handler:

                self.handlers[i.split('_')[0]] = self.__getattribute__(i)


    
    @handler(require='trust')
    def die_handler(self, _connection, _event):
        """
        Turns winnie off.
        """
        self.com.die()

    @handler
    def channels_handler(self, _connection, event):
        """
        Interact with the channel list, options are ['list', 'join', 'part']
        """
        message = event.arguments()[0].split(' ')

        if len(message) > 1:
            command = message[1]
        else:
            command = 'list'


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

    @handler
    def last_handler(self, _connection, event):
        """
        Prints the key of the last used intel
        """
        intel = model.intelligence.select().orderBy('lastused').reversed()[0]

        return "Last used intel was %s" % intel.id

    @handler
    def show_handler(self, _connection, event):
        """
        Prints the key of the last used intel
        """
        intel = model.intelligence.select().orderBy('lastused').reversed()[0]

        return "In %s, using %s mode, and verbosity is %s." % (event.target(), self.get_mode(event.target()), self.c.verbosity)

    @handler
    def mode_handler(self, _connection, event):
        """
        Allows you to view or set the mode for this channel. Options are in self.modes determined at runtime
        """
        message = event.message.split(' ')

        
        # sets the mode, otherwise shows the mode
        if len(message) > 1:
            return self.set_mode(event.target(), message[1])
        else:
            return "I am in %s mode" % self.get_mode(event.target())

    def get_mode(self, channel):
        """
        Retrieves the mode for this channel.
        """
        modes = self.c.modes
        if type(modes) != DictType or channel not in modes:
            self.set_mode(channel, self.default_mode)
            modes = self.c.modes
        
        return modes[channel]
   
    def set_mode(self, channel, mode):
        """
        Sets the mode for this channel.
        """
        modes = self.c.modes
        if type(modes) is not DictType:
            modes = {}
        
        if mode in self.modes:
            modes[channel] = mode
            self.c.modes = modes
            # TODO: don't say this here
            return "Going into %s mode" % mode
        else:
            return "%s is not a valid mode" % mode

    @handler(require='trust')
    def reload_handler(self, _connection, _event):
        """
        Reloads responder engine.
        """
        self.com.reload()
        
        # TODO: reload model
        #reload(model)
        return "Reloaded responder engine."
            
    @handler
    def verbosity_handler(self, _connection, event):
        """
        Allows user to interact with the verbosity setting
        """
        message = event.arguments()[0].split(' ')

        if len(message) is 1:
            return "Verbosity is %s." % self.c.verbosity
        else:
            i = int(message[1])
            if i in range(0, 101):
                self.c.verbosity = i
                return "Set verbosity to %s." % self.c.verbosity
            else:
                return "Verbosity must be between 0 and 100."

    @handler(require='trust')
    def set_handler(self, _connection, event):
        """
        Sets a memcached key/value
        """
        message = event.arguments()[0].split(' ', 2)

        if len(message) is not 3:
            return "Usage is %sset [key] [value]." % self.handler_prefix
        else:
            if (self.c.__setattr__(message[1], message[2])):
                return "Noted."

    @handler
    def get_handler(self, _connection, event):
        """
        Retrieves a memcached value
        """
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
    def whoami_handler(self, _connection, event):
        """
        Returns the full mask
        """
        message = event.arguments()[0].split(' ')

        if len(message) is not 1:
            return "Usage is %swhoami" % self.handler_prefix
        else:
            resp = "You are %s (trusted: %s)" % (event.user.mask,
                ('yes' if event.user.trusted else 'no')
            )

            if event.user.account:
                resp = resp + " Registered as %s" % (event.user.account.email)
            return resp

    @handler(require='trust')
    def python_handler(self, connection, event):
        """
        Executes Python code
        """
        message = event.arguments()[0].split(' ', 1)

        if len(message) <= 1:
            return "Usage is %srun [code]." % self.handler_prefix
        else:
            logger.notice("EVALING CODE: %s"%message[1])
            
            value = None
            if '=' in message[1]:
                exec message[1]
            else:
                value = eval(message[1], globals(), locals())

            if not value == None:
                return "Returned: %s" % value

    @handler(require='trust')
    def trust_handler(self, connection, event):
        message = event.arguments()[0].split(' ')

        if len(message) is not 2:
            return "Usage is %strust [mask]." % self.handler_prefix
        else:
            nick = message[1]
            
            if nick in [u for u in self.com.channels[event.target()].userdict]:
                return "You must specify %s's full nick mask." % nick

            user = self.get_usermask(nick)
            
            if not user.account:
                return "%s doesn't have an account registered" % nm_to_n(nick)

            user.account.trusted = 1

            return "%s is now trusted" % nm_to_n(nick)
    
    @handler
    def register_handler(self, connection, event):
        message = event.arguments()[0].split(' ') # register [email] [password]

        if len(message) is not 3:
            return "Usage is %sregister email password" % self.handler_prefix
        else:
            email, password = message[1:]
            
            query = model.account.selectBy(email=email)
            if query.count() == 0:
                a = model.account(email=email, password=md5.md5(password).hexdigest())
                event.user.account = a
                return "account created, identified as %s" % email
            else:
                return "an account already exists for that email"

            user.trusted = 1

            return "%s is now trusted" % nm_to_n(to_trust)

    @handler
    def identify_handler(self, connection, event):
        message = event.arguments()[0].split(' ') # register [email] [password]

        if len(message) is not 3:
            return "Usage is %sidentify email password" % self.handler_prefix
        else:
            email, password = message[1:]

            query = account.selectBy(email=email)
            if query.count() == 0:
                return "No user registered as %s" % email
            else:
                a = query.getOne()

                if md5.md5(password).hexdigest() == a.password:
                    event.user.account = a
                    
                    return "identified as %s" % event.user.account.email
                else:
                    return "wrong password"
    
    @handler(require='trust')
    def trace_handler(self, connection, event):
        """
        Opens a trace in the console. Do not use unless you have access to winnie's terminal.
        """
        message = event.arguments()[0].split(' ')

        if len(message) is not 1:
            return "Usage is %strace" % self.handler_prefix
        else:
            from ipdb import set_trace; set_trace()

            return "done with trace"

    def gets_to_speak(self, channel):
        """
        For any event in which winnie /might/ speak, she
        calls this method.

        It rolls the dice and determines whether or not she
        should based on channel mode + randomness + verbosity.
        """
        return True if random.choice(range(0,100)) < self.c.verbosity else False

    def get_usermask(self, mask):
        """
        returns the account_mask db record for the user
        """
        query = model.account_mask.selectBy(mask=mask)

        if query.count() > 0:
            return query.getOne()
        else:
            return model.account_mask(mask=mask, accountID=None)

    def handle(self, connection, event):
        """
        The first level of handling. This checks to see if
        a command was called.

        Otherwise the event gets sent off to the mapper, which
        scans text for things to learn or replies to formulate
        based on channel mode.
        """
        print "Handling event :%s"%event.arguments()[0]

        event.user = self.get_usermask(event.source())

        try:
            if event.message.startswith(self.handler_prefix):
                for handler in self.handlers.keys():
                    if event.arguments()[0].startswith(
                            "%s%s" % (self.handler_prefix,handler)):
                        self.handlers[handler](connection, event)
                        return None
            else:
                self.analyze(connection, event)

        # In the event of an unhandled exception, we print the traceback
        # and restart our responders.
        except Exception, e:
            traceback.print_exc(e)
            self.com.init_responders()
        finally:
            pass

    def analyze(self, connection, event):
        """
        Searches text for learnable content, also formulates replies to content
        either mimicing former statements or generating entirely new ones
        using markov chains.
        """
        logger.info("Analyzing %s" % event.message)

        # Keyword generation
        l = Lexer(event.message)
        event.keywords = l.keywords

        # If this intelligence doesn't exist already
        # We just learned something
        # SAVE IT!
        if self.should_save(event):
            print "Saving that"
            self.save_intel(event)

        # Hold your tounge winnie
        if self.gets_to_speak(event):
            print "Speaking that"
            self.speak_for(event)
        else:
            print "Didn't get to speak T_T"
    
    def should_save(self, event):
        return (len(event.keywords) > 3)

    def search(self, query, limit=1, not_within=60):
        """
        Does a natural language search on the database for [query], 
        results limited to [limit], and always older than the last
        argument (in minutes).
        """
        return model.search_intelligence(query, limit, not_within)

    def speak_for(self, event):
        """
        Sends a response for a given event
        """

        # TODO: some badass shit for return self.modes[self.mode](event) if len(self.modes) > 0 else None
        if len(self.modes) == 0:
            return # No  modes!

        response = None if len(self.modes) == 0 else self.modes[self.get_mode(event.target())](event)
        
        self.com.queuemsg(event, event.target(), response)

    def markov_from(self, query, table=None):
        """
        Builds a markov chain from the search query

        TODO: build out a Markov class, it'll use winnie.data.Client
        """
        if False: #len(query.split()) > 2: # TODO: factor out
            return "Limited to two query words"
        else:
            #print "[%s]"%query
            intel = self.search(query.split(" "), limit=0, not_within=0)
            if not intel or 'msg' in intel[0].__dict__:
                print "NOT GUNNA PRINT FAKE INTEL! %s"%intel[0].msg
                return

            results = [i.message for i in intel]

            lw = "\n"
            w1, w2 = lw, lw
            
            if type(table) != DictType: table = {}

            # TODO: refactor out
            newtable = self.generate_table(results)
            for key in newtable:
                if key in table:
                    table[key].extend(newtable[key])
                else:
                    table[key] = newtable[key]

            # Chain generation
            w1, w2 = lw, lw
            chain = ""
            for i in xrange(100): # TODO: make this configurable, do something
                try:
                    newword = random.choice(table[(w1,w2)])
                except KeyError, e:
                    newword = lw

                chain += " " + newword
                w1, w2 = w2, newword

            # TODO: regulate returns, allow option to return more than first
            # sentence
            return chain.split('. ')[0]+'.'

    def generate_table(self, strings=None):
        table = {}
        if not strings: return table

        # For each statement, we're going to build up a table of word
        # sequences and the words that follow.
        lw = "\n"
        w1, w2 = lw, lw
        for word in " ".join(strings).split(" "):
            table.setdefault( (w1, w2), [] ).append(word)
            w1, w2 = w2, word
       
        table.setdefault( (w1, w2), [] ).append(lw)
        return table


    def indicated(self, message):
        """
        Looks through the phrase for the existance of any thing like
            'john is a fag'
        and will return ('is', ['john', 'a fag'])
        """
        # Don't log questions now
        if message.endswith('?') and not message.endswith('\\?'):
            return None

        # If it starts with an interrogative, don't add it
        for v in self.com.interrogatives:
            if message.startswith(v):
                return None
        
        message = message.lstrip('\\')
        message = message.lstrip('\\')

        split = message.split(' ')
        for i in self.com.indicators:
            for s in split:
                if i == s:
                    return (i, [s.strip() for s in message.split(' %s '%i, 1)])

        return None
 
    def save_intel(self, event):
        """
        Saves intel to the db from an event
        TODO: remove last two arguments
        """
        # TODO: remove
        #from ipdb import set_trace; set_trace()

        intel = model.intelligence(
            source = event.source(),
            target = event.target(),
            keywords = " ".join(event.keywords),
            message = event.arguments()[0],
            created=event.timestamp
        )

        self.com.log(intel)
        return intel
