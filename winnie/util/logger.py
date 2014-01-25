from datetime import datetime

from winnie.util.singletons import Singleton
from winnie.util.color import Color
color = Color()

def action(sign='', color_name=None):
    '''
    Decorator to allow for
        
        @action('%%')
        def crazytown(item): return "THIS IS CRAZY[%s]" % item.__repr__()
    '''
    def wrap(f):
        def wrapped_f(instance, item):
            prefix = color.code(color_name, sign) if color_name else sign
            instance.log( prefix, f(item) )
        return wrapped_f
    return wrap

class Logger:
    """
    logger = Logger()
    logger.learned(intelligence.message)

    # Results in
    # print '++', datetime.now(), "Learned: ", message
    # ++ [15:22.23] Learned: somehow I doubt that's believable
    """
    __metaclass__ = Singleton


    @action('++', 'green')
    def learned(intel): return 'Learned: %s' % intel.__repr__()

    @action('++', 'green')
    def add(item): return 'Adding %s' % item

    @action('--', 'red')
    def rem(item): return 'Removing %s' % item

    @action('<-', 'blue')
    def incoming(item): return item

    @action('->', 'blue')
    def outgoing(item): return item
    
    @action('!!', 'magenta')
    def notice(item): return item

    @action('**', 'yellow')
    def info(item): return item

    def log(self, sign, message, time=datetime.now()):
        """
        logger.log('++', 'Added an awesome statement') # results in 
        print " ++ [15:21 33] Added an awesome statement"
        """
        timeformat = "%H:%M %S"   

        if 'strftime' in dir(time):
            out = " %s [%s] %s" % (sign, color.code('blue', time.strftime(timeformat)), message)
        else:
            out = " %s [%s] %s" % (sign, color.code('blue', time), message)

        print out
