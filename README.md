WINNIE
------

Winnie is a re-write of an ancient and wonderfully functional idea I had as a child in which an IRC
bot would sit in a channel recording everything you say and ultimately spit it back out later whenever
relevent. The original version used a DIY irc lib and MySQL FULLTEXT search to find useful sayings.

This version uses the twisted protocol framework and SQLAlchemy for the orm.

FEATURES (TODO)
---------------

 * Web interface, to monitor / interfere with her decision making process.
 * Karma system (++ // --) for when you want to give a user meaningless Internet points.
 * Console log output hilighting, to differentiate between what's being learned and what is being spoken off of.
 * Use websockets for monitoring, :: http://autobahn.ws/python/tutorials/echo/
 * http://yz.mit.edu/wp/web-sockets-tutorial-with-simple-python-server/
