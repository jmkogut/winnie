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
