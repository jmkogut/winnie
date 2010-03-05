name_maps = [
    ('reset', ('\033[0m'))
]

names = ['black','red','green','yellow','blue','magenta','cyan','white']
for name in names:
    name_maps.append(
        (name, '\033[9%sm'%names.index(name))
    )

class Color:
    def __init__(self):
        self.maps = {}
        for name,value in name_maps:
            self.maps[name] = value

    def code(self, name, string):
        return self.maps[name] + string + self.maps['reset']

    def list(self):
        for name in [m for m in self.maps if m!='reset']:
            print "%s looks like %s" % (name, self.code(name, "this"))
