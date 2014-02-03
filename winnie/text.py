import re
import config

def is_hilight(message):
    if message.startswith(config.NICK+':'):
        return True

    return False

def is_cmd( prefix, message ):
    if is_hilight(message):
        return message.lstrip( '%s: %s '%(config.NICK, prefix) )
    return False
