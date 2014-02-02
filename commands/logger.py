import hook
from model import User

@hook.cmd
def logger( (src,targ,msg), s=None ):
    User.learned(src, msg)
    print ' -- [learned] %s' % msg

@hook.alias( 'testadd' )
def addition( (src,targ,msg), s=None ):
    return 'lolhax'
