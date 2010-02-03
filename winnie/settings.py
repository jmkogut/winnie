# Typing Speed (in characters per minute)
TYPING_SPEED = 550

# Verbosity, the percentage of the time that winnie will 
# look for something to say in response.
VERBOSITY = 10

# LOGSIZE
LOGSIZE = 50

# IRC settings
IRC = (
    'winniepooh',                   # nick
    ('irc.freenode.net', 6667)    # server
)

IRC_CHANNELS = (
    '#'+IRC[0],                     # join the channel with our nickname
    '#trees'
)

# The db connection string
DATABASE = "mysql://db9:doobienine@localhost/factoids"

# Handler Prefix (for commands %channels, %help, etc)
HANDLER_PREFIX = '%'
