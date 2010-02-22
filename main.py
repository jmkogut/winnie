#!/usr/bin/env python2.5

"""
The primary startup script for winnie. Initializes
the IRC connection 
"""

if __name__ == '__main__':
    from winnie.protocols.irc import communicator

    try:
        win = communicator.Communicator()
        win.start()
        win.running = False
        win.die()

    except KeyboardInterrupt, e:
        win.running = False
        win.die()
    
else:
    print 'Usage: python ./main.py'
