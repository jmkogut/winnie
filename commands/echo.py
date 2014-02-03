import hook

@hook.alias( 'websock_echo', priority=0)
def WSEcho( (src,trg,msg), factory=None, **kw):
    factory.wsf.send_msg( "{'irc_event': '<%s> %s: %s'}" % (trg,src,msg) )
    return
