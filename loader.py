import collections
import glob
import os
import re
import sys
import traceback

class DotDict(dict):
    def __init__(self, *a, **kw):
        dict.__init__(self, *a, **kw)
        self.__dict__ == {}

    def __getattr__(self, k):
        if self.has_key(k):
            return self[k]

    def __setattr__(self, k, v):
        if isinstance(v, dict):
            self[k] = DotDict(v)
        else:
            self[k] = v

def Load(init = False):
    mtimes    = DotDict()
    lastfiles = DotDict()
    plugs     = DotDict()

    changed = False

    ns = DotDict()

    if init:
        plugs.cmds    = {}
        plugs.threads = {}
        plugs.plugs   = {}
        plugs.events  = {}

    plug_fileset = set(glob.glob(os.path.join('commands','*.py')))
    for fn in plug_fileset:
        mtime = os.stat(fn).st_mtime
        if mtime != mtimes.get(fn) or fn not in mtimes:
            mtimes[fn] = mtime
            changed    = True

            try:
                code = compile(open(fn,'U').read(), fn, 'exec')
                ns = DotDict()
                eval(code, ns)
            except Exception:
                print ' -- ERROOOOOOORRRRRR -------------------'
                traceback.print_exc()
                if init:
                    sys.exit()
                continue

        for obj in ns.itervalues():
            if hasattr(obj, '_handler'):
                print 'Found handler %s' % (obj._handler['name'])
                plugs.cmds[ obj._handler['name'] ] = obj

    return plugs.cmds

if __name__ == '__main__':
    cmds = Load(init=True)

    print
    print 'loaded %s cmds' % len(cmds)
    print ' -- %s -- ' % ([k for k in cmds.keys()])
    print cmds
