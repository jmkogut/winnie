import hook

@hook.cmd
def tester( (src,trg,msg), self=None ):
    return "I have nothing to say."

@hook.cmd
def karma( (sr,tg,msg), s=None ):
    return 'i am one who knocks'
