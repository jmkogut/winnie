from winnie import hook

@hook.alias(priority=0)
def tester( (src,trg,msg), **kw):
    return "I have nothing to say."

@hook.cmd
def karma( (sr,tg,msg), **kw):
    return 'i am one who knocks'
