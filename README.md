WINNIE
------

Winnie is a re-write of an ancient and wonderfully functional idea I had as a child in which an IRC
bot would sit in a channel recording everything you say and ultimately spit it back out later whenever
relevent. The original version used a DIY irc lib and MySQL FULLTEXT search to find useful sayings.

This version uses the twisted protocol framework and SQLAlchemy for the orm.

![winnie, she so kawai](https://raw.github.com/jmkogut/winnie/master/doc/mascotu.jpg?raw=true)

FEATURES (TODO)
---------------

 * Web interface, to monitor / interfere with her decision making process.
 * Karma system (++ // --) for when you want to give a user meaningless Internet points.
 * Console log output hilighting, to differentiate between what's being learned and what is being spoken off of.
 * Use websockets for monitoring, :: http://autobahn.ws/python/tutorials/echo/
 * http://yz.mit.edu/wp/web-sockets-tutorial-with-simple-python-server/
 * Xapian guide - http://invisibleroads.com/tutorials/xapian-search-pylons.html

BOT IDEAS
---------

 * Logging - File, sqlite, http post mayhaps, whoknows
 * Live code reloading (done - 01/26/2014)
 * web irc client (secondary project there really.)
 * karma - allows you to upvote or downvote a user :: abzde++ or abzde-- and have the recorded votes saved.
 * greeter - acknowleges known users with positive karma score. May disparagingly greet users who have been downvoted, 
 * github features, i.e. self-reporting bugs from the users, notifying channels of commits to the repo
 * lastseen & notify - allows you to track when a member was lastseen. Optionally, you can leave a message to be delivered to that user as
   SOON as he says something. Winnie will continue reporting until PM'd with a confirmation that the msg was received
 * google / github search
 * github activity - notify when somebody subscribes/watches the winnie repo
 * Q&A support - learn common questions and try to answer them in the future.
 * Link archive - As links are posted, they become viewable in a stream-of-consciousness via the web interface
 * league of legends integration - http://developer.riotgames.com/docs/getting-started
 * feature suggestions by users
 * breaking news. I'm a bit wary on this though.
 * Markov response generation
 * Parroting via fulltext search and a dice-roll.
 * reports where I am at any given time.
 * pastebin - initiates a PM and after EOF will upload text to a pastebin and put the uri in the chawnnel
 * fortune - wrapper for linux fortune
 * Quote movies like The Big Lebowski and/or Pulp Fiction when appropriate.
 * Report users for reposting links. <- Hahahaha
 * Conduct polls, create them in IRC or the webiu.
 * Save specific intel as quotes and give users the choice to vote on em.
 * Search channel history for [topic], giving a weblink to more detailed results.
 * Activity stats / graphs / live tag cloud
 * Bitcoin stats / market rates # fucking why though?
