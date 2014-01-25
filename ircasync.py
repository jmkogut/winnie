# asyncore -- Asynchronous socket handler 
# http://www.python.org/doc/current/lib/module-asyncore.html

import string, re
import socket
import asyncore, asynchat

#RFC 2811: Internet Relay Chat: Client Protocol
#2.3 Messages
# http://www.valinor.sorcery.net/docs/rfc2812/2.3-messages.html
SPC="\x20"
CR="\x0d"
LF="\x0a"
CRLF=CR+LF

class SingleServerConnection(asynchat.async_chat):
    _commands = (
        'PRIVMSG',
        'NOTICE',
        'PING',
        'PONG',
        'USER',
        'NICK',
        'JOIN',
        'PART',
        'INVITE',
        'QUIT',
        ('RPL_WELCOME','001')
    )

    def __init__(self):
        asynchat.async_chat.__init__(self)
        self.buffer_in = ''
        self.set_terminator(CRLF)

        self.nick = 'winnie' 
        self.userid = self.nick
        self.fullName = self.nick + ' ' + self.nick

        self._startChannels = ['#'+self.nick]
        self._dispatch = []
        self._doc = []

        # Defaults value to the command
        for command in self._commands:
            if len(command) == 2:
                command,value = command
            else:
                value = command
            globals()[command] = value
        
    def makeConn(self, host, port):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        debug("connecting to...", host, port)
        self.connect((host, port))

        self.buffer_in = ''

    def todo(self, args, *text):
        command = string.join(args)
        if text: command = command + ' :' + string.join(text)

        self.push(command + CRLF)
        debug("sent/pushed command:", command)

    # asyncore methods
    def handle_connect(self):
        debug("connected")

        #@@ hmm... RFC says mode is a bitfield, but
        # irc.py by @@whathisname says +iw string.
        self.todo([NICK, self.nick])
        self.todo([USER, self.userid, "+iw", self.nick], self.fullName)


    # asynchat methods
    def collect_incoming_data(self, bytes):
        self.buffer_in = self.buffer_in + bytes

    def found_terminator(self):
        #debug("found terminator", self.buffer_in)
        line = self.buffer_in
        self.buffer_in = ''

        if line[0] == ':':
            origin, line = string.split(line[1:], ' ', 1)
        else:
            origin = None

        try:
            args, text = string.split(line, ' :', 1)
        except ValueError:
            args = line
            text = ''
        args = string.split(args)
        
        event = {
            'source': origin,
            'arguments': args,
            'message': text }

        debug("from::", origin)

        self.rxdMsg(args, text, origin)

    def bind(self, thunk, command, textPat=None, doc=None):
        """
        thunk is the routine to bind; it's called ala
          thunk(matchObj or None, origin, args, text)
        
        command is one of the commands above, e.g. PRIVMSG
        textpat is None or a regex object or string to compile to one
        
        doc should be a list of strings; each will go on its own line"""

        if type(textPat) is type(""): textPat = re.compile(textPat)

        self._dispatch.append((command, textPat, thunk))

        if doc: self._doc = self._doc + doc

    def rxdMsg(self, args, text, origin):
        if args[0] == PING:
            self.todo([PONG, text])

        for cmd, pat, thunk in self._dispatch:
            if args[0] == cmd:
                if pat:
                    #debug('dispatching on...', pat)
                    m = pat.search(text)
                    if m:
                        thunk(m, origin, args, text)
                else:
                    thunk(None, origin, args, text)

    def startChannels(self, chans):
        self._startChannels = chans
        self.bind(self._welcomeJoin, RPL_WELCOME)
                  
    def _welcomeJoin(self, m, origin, args, text):
        for chan in self._startChannels:
            self.todo(['JOIN', chan])

    def tell(self, dest, text):
        """todo a PRIVMSG to dest, a channel or user"""
        self.todo([PRIVMSG, dest], text)

    def notice(self, dest, text):
        """todo a NOTICE to dest, a channel or user"""
        self.todo([NOTICE, dest], text)

def actionFmt(str):
    return "\001ACTION" + str + "\001"

def replyTo(myNick, origin, args):
    target = args[1]
    if target == myNick: # just to me
        nick, user, host = splitOrigin(origin)
        return nick
    else:
        return target

def splitOrigin(origin):
    if origin and '!' in origin:
        nick, userHost = string.split(origin, '!', 1)
        if '@' in userHost:
            user, host = string.split(userHost, '@', 1)
        else:
            user, host = userHost, None
    else:
        nick = origin
        user, host = None, None
    return nick, user, host

# cf irc:// urls in Mozilla
# http://www.mozilla.org/projects/rt-messaging/chatzilla/irc-urls.html
# Tue, 20 Mar 2001 21:28:14 GMT
#SHIT'S UNUSED
#def serverAddr(host, port=6667):
#    return "irc://%s:%s/" % (host, port)
        
#def chanAddr(host, port, chan):
#    if chan[0] == '&': chanPart = '%26' + chan[1:]
#    elif chan[0] == '#': chanPart = chan[1:]
#    else: raise ValueError # dunno what to do with this channel name
#    return "%s%s" % (self.serverAddr(host,port), chanPart)
        
def debug(*args):
    import sys
    sys.stderr.write("DEBUG: ")
    for a in args:
        sys.stderr.write(str(a))
    sys.stderr.write("\n")


def test(hostName, port, chan):
    c = SingleServerConnection()
    c.startChannels([chan])

    def spam(m, origin, args,  text, c=c):
        c.tell(args[1], "spam, spam, eggs, and spam!")
    c.bind(spam, PRIVMSG, r"spam\?")

    def bye(m, origin, args, text, c=c):
        c.todo([QUIT], "bye bye!")
    c.bind(bye, PRIVMSG, r"bye bye bot")

    c.makeConn(hostName, port)
    asyncore.loop()
    
    
if __name__=='__main__':
    test('irc.w3.org', 6665, '#rdfbot')
    #test('irc.openprojects.net', Port, '#rdfig')
