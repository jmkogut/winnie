import asynchat
import logging
import socket


class IRCProtocol(asynchat.async_chat):
    '''
    Asynchronous protocol handler for IRC.
    '''
    
    def __init__(self, host=None, port=6667):
        print 'hit init'
        self.received_data = []
        self.logger = logging.getLogger('winnie.protocols.irc')
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('connecting to %s', (host, port))
        self.set_terminator("\r\n")
        self.connect((host, port))
        return
        
    def handle_connect(self):
        self.logger.debug('handle_connect()')
        # Send the command
        self.push( 'NICK winniejr\r\n' )
        self.push( 'USER pooh iw 0 :pooh\r\n' )
        # Send the data
        self.push_with_producer(EchoProduducer(self.message))
        # We expect the data to come back as-is, 
        # so set a length-based terminator

    
    def collect_incoming_data(self, data):
        """Read an incoming message from the client and put it into our outgoing queue."""
        self.logger.debug('collect_incoming_data() -> (%d)\n"""%s"""', len(data), data)
        self.received_data.append(data)

    def found_terminator(self):
        self.logger.debug('found_terminator()')
        self.logger.debug('Received:'+self.received_data[len(self.received_data)-1])

if __name__ == '__main__':
    irc = IRCProtocol(host='irc.freenode.org') 
