# Typing Speed (in characters per minute)
TYPING_SPEED = 750 # Mine is ~550, 750 is exceedingly high

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
    '#bupki',
#    '#trees'
)

TRUSTED_USERS = (
    "db9!db9@64.79.219.85",
)

# The db connection string
DATABASE = "mysql://db9:doobienine@localhost/factoids"

# Handler Prefix (for commands %channels, %help, etc)
HANDLER_PREFIX = '%'

# HTTP Address
HTTP_ADDRESS = {
    'host': '0.0.0.0',
    'port': '8090'
}
