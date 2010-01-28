from time import datetime
from types import StringType, FunctionType

urgencies = {
    'add':'++',
    'sub':'--',
    'in':'<-',
    'out':'->',
    'notice':'!!',
    'sys':'**'
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
    timeformat = "%H:%M.%S"   
    out = " %s [%s] %s" % (urgencies[urgency], time.strformat(timeformat), message)

    log = cache.get_cache()
    log.append((datetime.now(), out))

    # Don't let log go past LOGSIZE
    if (len(log) is settings.LOGSIZE):
        log.pop(0)

    self.c.log = log

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

