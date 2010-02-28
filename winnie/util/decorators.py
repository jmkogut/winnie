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

