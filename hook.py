import inspect
import functools

# class Singleton(object):
#     _inst = None
#     def __new__(c, *a, **kw):
#         if not c._inst:
#             c._inst = super(Singleton, c).__new__(c, *a, **kw)
#         return c._inst
# 
# class Responders(Singleton):
#     funcs = []
# 
#     def add(s, func):
#         if func not in s.funcs:
#             s.funcs.append(func)
#         return func
# 
#     def rem(s, func):
#         if func in s.funcs:
#             s.funcs.remove(func)
# 
#     def dispatch(self, *args, **kwargs):
#         ret = []
#         for f in self.funcs:
#             ret.append( f( *args, **kwargs ) )
#         return ret

def _set_options( func, add, name='' ):
    if not hasattr(func, '_hook'):
        func._hook = []
    func._hook.append( add )

    if not hasattr(func, '_filename'):
        func._filename = func.func_code.co_filename

    if not hasattr(func, '_args'):
        argspec = inspect.getargspec( func )
        if name:
            n_args = len(argspec.args)
            if argspec.defaults:
                n_args -= len(argspec.defaults)
            if argspec.keywords:
                n_args -= 1
            if argspec.varargs:
                n_args -= 1
            
        args = []
        if argspec.defaults:
            end = bool(argspec.keywords) + bool(argspec.varargs)
            args.extend( argspec.args[-len(argspec.defaults):
                end if end else None])

        if argspec.keywords:
            args.append(0)

        func._args = args

    if not hasattr(func, '_thread'):
        func._thread = False

def _cmd(arg=None, **kwargs):
    args = {}

    def _wrapper( func ):
        func.func_defaults = func.func_defaults[:-1] + (func,)
        _set_options( func, ['command', (func, args)], 'command' )
        return func

    if kwargs or not inspect.isfunction(arg):
        args['name'] = arg if arg is not None else 'foo'
        args.update( kwargs )
        return _wrapper
    else:
        args['name'] = arg.__name__
        return _wrapper(arg)

def cmd( fn=None, **kwargs ):
    OPTS = kwargs

    def _wrap( fn ):
        fn.func_defaults = fn.func_defaults[:-1] + (fn,)
        OPTS["name"] = getattr(fn, '__prefix') if hasattr(fn, '__prefix') else fn.__name__
        _set_options( fn, ['command', (fn, OPTS)], 'command' )
        return fn

    if not inspect.isfunction(fn):
        return _wrap
    else:
        return _wrap(fn)
command = cmd

# def limit( prefix='' ):
#     OPTS = { 'name': prefix }
#     print 'entered hook'
# 
#     def _wrapp( fn ):
# 
#         print 'entered _wrapp'
#         fn.func_defaults = fn.func_defaults[:-1] + (fn,)
#         _set_options( fn, ['command', (fn, OPTS)], 'command' )
#         def _run( *a, **kw):
#             print 'inside _ran'
#             return fn(*a,**kw)
#         return _run
#     return _wrapp
def limit( prefix ):
    def deco( fn ):
        @functools.wraps( fn )
        def __mydecorator(*args, **kwargs):
            print 'limiting func to pfx %s'%prefix
            return func(*args, **kwargs)
        return __mydecorator
    return deco
