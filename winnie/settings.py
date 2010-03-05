# Typing Speed (in characters per minute)
TYPING_SPEED = 750 # Mine is ~550, 750 is exceedingly high

# Verbosity, the percentage of the time that winnie will 
# look for something to say in response.
VERBOSITY = 15

# LOGSIZE
LOGSIZE = 50

# IRC settings
IRC = (
    # nick first, any alt names after that (also things that people can call her)
    ('winniepooh','winnie','winniep','thepooh','winnibear','pooh'),
    ('irc.freenode.net', 6667)    # server
)

IRC_CHANNELS = (
    '#'+IRC[0][0],                     # join the channel with our nickname
#    '#trees',
    '#trees', '#reddit',
)

# The db connection string
DATABASE = "mysql://doobie:doobienine@localhost/winnie"

# Handler Prefix (for commands %channels, %help, etc)
HANDLER_PREFIX = '%'

# HTTP Address
HTTP_ADDRESS = {
    'host': '0.0.0.0',
    'port': '8090'
}

# Directory paths
PATH = '/home/winnie/projects/winnie'
TEMPLATES_PATH = PATH + '/web/static/'
STATIC_PATH = TEMPLATES_PATH
