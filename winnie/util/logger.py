from datetime import datetime

from winnie.util.singletons import Singleton

def action(sign=''):
    '''
    Decorator to allow for
        
        @action('%%')
        def crazytown(item): return "THIS IS CRAZY[%s]" % item.__repr__()
    '''
    def wrap(f):
        def wrapped_f(instance, item):
            instance.log( sign, f(item) )
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


    @action('++')
    def learned(intel): return 'Learned: %s' % item.__repr__()

    @action('++')
    def add(item): return 'Adding %s' % item

    @action('--')
    def rem(item): return 'Removing %s' % item

    @action('<-')
    def incoming(item): return item

    @action('->')
    def outgoing(item): return item
    
    @action('!!')
    def notice(item): return item

    @action('**')
    def info(item): return item

    def log(self, sign, message, time=datetime.now()):
        """
        logger.log('++', 'Added an awesome statement') # results in 
        print " ++ [15:21 33] Added an awesome statement"
        """
        timeformat = "%H:%M %S"   

        if 'strftime' in dir(time):
            out = " %s [%s] %s" % (sign, time.strftime(timeformat), message)
        else:
            out = " %s [%s] %s" % (sign, time, message)

        print out
