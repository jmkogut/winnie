from winnie import hook
from winnie import text

@hook.cmd
def quit( (src,targ,msg), client=None, **kw ):
    act = text.is_cmd( 'quit', (src,targ,msg) )
    if act:
        print 'Received a quit command.'
        client.quit() # TODO: USE COLOURFUL PART MESSAGES
    return False

@hook.cmd
def join( (src,targ,msg), client=None, **kw ):
    act = text.is_cmd( 'join', (src,targ,msg) )
    if act:
        print 'Received a join command.'
        client.join( act )
    return False

@hook.cmd
def leave( (src,targ,msg), client=None, **kw ):
    act = text.is_cmd( 'leave', (src,targ,msg), default=targ )
    if act:
        print 'Received a leave command.'
        client.leave( act )
    return False

@hook.cmd
def who( (src,targ,msg), client=None, **kw ):
    act = text.is_cmd( 'who', (src,targ,msg), default=targ )
    if act:
        print 'Received a who command.'
        client.join( act )
    return False
