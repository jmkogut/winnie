import re
import config

def is_hilight( (sr, targ, message) ):
    if message.startswith(config.NICK+':'):
        return True
    if targ.startswith(config.NICK):
        return True
    return False

def is_cmd( prefix, (src, target, message), default=None):
    # TODO: token assumes you will always say winnie: getfucked #overhere
    # Obviously this wouldn't happen in a privmsg. fix it
     
    token = '%s: %s' % (config.NICK, prefix)
    if is_hilight((src,target,message)):
        if message.startswith(token):
            remainder = message.lstrip( token ).strip()
            return remainder if remainder else default
    return False

def mask_to_nick( mask ):
    if not '!' in mask: return mask.lower()
    else: return mask.split('!')[0].lower()
