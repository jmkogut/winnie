from datetime import datetime
from types import StringType, FunctionType

urgencies = {
    'add':'++',
    'sub':'--',
    'in':'<-',
    'out':'->',
    'notice':'!!',
    'sys':'**',
}

def debug(item=None, time=datetime.now(), urgency='sub'):
    if urgency not in urgencies:
        raise Exception('Not a valid logging urgency')

    if type(item) == FunctionType:
        def wrapper(*args):
            resp = item(*args)
            debug_print(resp, time, urgency)
            return resp
        return wrapper
    elif type(item) == StringType:
        debug_print(item, time, urgency)

def debug_print(message, time, urgency):
    """
    debug_print("My foo!", datetime.now(), 'out') # results in
    " -> [15:21.33] My foo!"
    """
    timeformat = "%H:%M %S"   

    if 'strftime' in dir(time):
        out = " %s [%s] %s" % (urgencies[urgency], time.strftime(timeformat), message)
    else:
        out = " %s [%s] %s" % (urgencies[urgency], time, message)

    print out
    # WTF, was I high?
    #log = cache.get_cache()
    #log.append((datetime.now(), out))

    ## Don't let log go past LOGSIZE
    #if (len(log) is settings.LOGSIZE):
    #    log.pop(0)
    #
    #self.c.log = log

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class Singleton(type):
    """
    To use:
    from winnie.util import Singleton
    class Foo:
        __metaclass__ = Singleton
    """
    def __init__(cls, name, bases, dic):
        super(Singleton, cls).__init__(name, bases, dic)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

def log(method):
    """
    Decorator: will log the method name and what it was called with
    """
    def wrapper(*args):
        debug("%s called with %s"%(method.__name__, args))
        resp = method(*args)
        debug("%s returned %s"%(method.__name__, resp))
        return resp

    return wrapper
