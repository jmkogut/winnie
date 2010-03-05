maps = {
    'ascii': (['black','red','green','yellow','blue','magenta','cyan','white'], '\033[0m', '\033[9%sm'),
    'irc':   (['white','black','blue','green','red','brown','purple','orange','yellow', \
                                    'lime','teal','cyan','royal','pink','grey','silver'], '\x030', '\x03%s'),
}

def map_gen(names, reset, fgtemplate):
    maps = { 'reset': reset }
    for name in names:
        maps[name] = fgtemplate % names.index(name)
    return maps

class Color:
    def __init__(self, map='ascii'):
        self.maps = map_gen(*maps[map])

    def code(self, name, string):
        return self.maps[name] + string + self.maps['reset']

    def gen_list(self, sep):
        items = []
        for name in [m for m in self.maps if m!='reset']:
            items.append(self.code(name, "%s looks like %s" % (name, "this")))

        return sep.join(items)

    def list(self, sep="\n"):
        print self.gen_list(sep)
