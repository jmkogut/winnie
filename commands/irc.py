from winnie import hook
from winnie import text

@hook.cmd
def join( (src,targ,msg), client=None, **kw ):
    act = text.is_cmd( 'join', msg )
    if act:
        print 'Received a join command.'
        client.join( act )
    return False
