import time
from winnie import settings
from winnie.util.logger import Logger
logger = Logger()

import threading
from functools import wraps

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

def simple_thread(method):
    """
    Executes a method in another thread for to not block
    """
    @wraps(method)
    def wrapper(*args):
        # Wrap the original func
        method_hl = threading.Thread(target=method, args=args)
        method_hl.start()
        return method_hl

    return wrapper

