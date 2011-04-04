#!/usr/bin/env python2.5

"""
The primary startup script for winnie. Initializes
the IRC connection 
"""

from winnie.protocols.irc import connection as IRC
from winnie.web import server as HTTP



def main():
    try:
        irc = IRC.Connection()
        irc.start()

    except KeyboardInterrupt, e:
        irc.running = False
        irc.die()
    
if __name__ == '__main__':
    main()
else:
    print 'Usage: python ./main.py'
