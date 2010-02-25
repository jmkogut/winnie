#!/usr/bin/env python2.5

"""
The primary startup script for winnie. Initializes
the IRC connection 
"""

if __name__ == '__main__':
    from winnie.protocols.irc import communicator
    from winnie.web import server

    try:
        # Start these processes
        win = communicator.Communicator()
        srv = server.Server()

        srv.communicator = win

        srv.start()
        win.start()

    except KeyboardInterrupt, e:
        win.running = False
        win.die()
    
else:
    print 'Usage: python ./main.py'
