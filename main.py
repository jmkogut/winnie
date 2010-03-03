#!/usr/bin/env python2.5

"""
The primary startup script for winnie. Initializes
the IRC connection 
"""

from winnie.protocols.irc import connection as IRC
from winnie.web import server as HTTP



def main():
    try:

        #from pympler.muppy import tracker
        #memory_tracker = tracker.SummaryTracker()

        # Start these processes
        irc = IRC.Connection()
                
        #irc.memory_tracker = memory_tracker

        #http = HTTP.Server()
        #http.communicator = irc
        #http.start()

        irc.start()

    except KeyboardInterrupt, e:
        irc.running = False
        irc.die()
    
if __name__ == '__main__':
    main()
else:
    print 'Usage: python ./main.py'
