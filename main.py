#!/usr/bin/env python2.5

"""
The primary startup script for winnie. Initializes
the IRC connection 
"""

if __name__ == '__main__':

    from winnie.protocols.irc import communicator
    
    try:
        
        w = communicator.Communicator()

        w.start()
        w.die()

    except KeyboardInterrupt, e:
        
        w.running = False
        w.die()
    
else:
    print 'Usage: python ./main.py'
