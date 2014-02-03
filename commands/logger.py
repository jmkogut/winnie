from winnie import hook
from winnie import text
from winnie.model import User

@hook.cmd
def logger( (src,targ,msg), **kw ):
    if not text.is_hilight((src,targ,msg)):
        User.learned(src, targ, msg)
        print ' -- [Logged] %s' % msg
