"""
The underlying class for network communication in winnie.

A protocol can be IRC, jabber, or email for all I care
"""

import sys, string, os
import socket, asyncore, asynchat

class Protocol:
    
    
if __name__ == '__main__':
    # create our socket
    sock = socket.socket()

    bufsize = 64

    # connect to our server
    sock.connect( ( 'irc.freenode.net', 6667 ) )


    # our buffer destination
    readbuffer = ''

    # send our initial nick/user
w
    sock.send( 'NICK winniejr\r\n' )
    sock.send( 'USER pooh iw 0 :pooh\r\n' )


    # enter our data loop
    while True:
        try:
            bytes_received = readbuffer

            while bytes_received >= bufsize:
                packet = sock.recv( bufsize )
                bytes_received = len( packet )
                readbuffer += packet


        except Exception, e:
            print e
            print '<< DEBUG >> Fatal error.'
            sys.exit(1)


        while readbuffer.find('\r\n' ) >= 0:
            currentline = readbuffer[:readbuffer.find( '\r\n' )]
            readbuffer = readbuffer[len( currentline )+2:]
  
            print currentline
  
            #parser.irc_parse( currentline )
            print 'parsing'
