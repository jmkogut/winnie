import time
from winnie import settings
from winnie.util.logger import Logger
logger = Logger()

def monkeypatch(cls):
    '''
    To use:

    from <somewhere> import <someclass>

    @monkeypatch(<someclass>)
    def <newmethod>(self, args):
        return <whatever>
    '''
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator

def singleton(cls):
    """
    To use:

    @singleton
    class <newclass>:
        ...
    """
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

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

def type_delay(method):
    """
    Decorator: Will sleep a bit before returning based on length and typing
    speed
    """
    def wrapper(*args):
        # Wrap the original func
        phrase = method(*args)
        
        if phrase:
            # Time delay
            delay = (len(tuple(phrase))*1.0 / settings.TYPING_SPEED*1.0) * 60
            logger.info("Delay of %s seconds"%delay)
            time.sleep( delay )

        return phrase

    return wrapper

