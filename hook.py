import inspect
import functools

def _mark_handler( fn, **kw ):
    if not hasattr(fn, '_handler'):
        fn._handler = { 'name':
            fn.__name__ if not 'name' in kw else kw['name']
        }

    if not hasattr(fn, '_filename'):
        fn._filename = fn.func_code.co_filename

# These decorators are fucking horrible. They don't work like normal.
def cmd( fn ):
    def _deco(fn):
        _mark_handler(fn)
        return fn
    return _deco(fn)

def alias( name ):
    def _wrap( fn ):
        def _deco(fn):
            _mark_handler(fn, name=name)
            return fn
        return _deco(fn)
    return _wrap
