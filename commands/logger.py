from winnie import hook
from winnie.model import User

@hook.cmd
def logger( (src,targ,msg), **kw ):
    User.learned(src, msg)
    print ' -- [learned] %s' % msg

@hook.alias( 'testadd' )
def addition( arg, **kw ):
    print 'testadd fired with %s' % (arg,)
    return
