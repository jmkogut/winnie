class Singleton(type):
    """
    Singleton metaclass

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

