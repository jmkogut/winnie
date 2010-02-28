from winnie.util.logger import *
from winnie.data import model
from winnie.lexer import Lexer

from irclib import Event
import datetime
import re
import os


def create_keywords(max=50):
    to_index = model.intelligence.selectBy(keywords='')

    debug("Found %s records to index. (Max: %s)"%(to_index.count(),max))
    debug("Indexing...")

    i = 0
    while i is not False:
        intel = to_index[i]
        debug("Indexing %s"%intel.id)
        #intel.keywords = lexer(intel.original).keywords
        i = i + 1 if i is not max else False

def import_irc_log(filename=None, target=None, max=-1, threshold=4):
    """
    Reads the irc log and imports data to your target
    """
    file = open(filename, 'r')
    stats = {
        'days': 0,
        'lines': 0,
        'events': 0,
        'saved': 0,
        'date': None
    }
    
    months = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    time = '(?P<H>[\d]{2}):(?P<M>[\d]{2}):(?P<S>[\d]{2})'
    nick = '<\s+(?P<nick>.+)>'

    ignored_targets = (
        "#mp3passion"
    )

    if target in ignored_targets: return

    linehandlers = {}
    def group_to_event(group):
        e = Event('pubmsg', group['nick'], target, (group['message'],))
        e.timestamp = datetime.datetime(int(stats['year']), months.index(stats['month']), int(stats['date']), \
                                        int(group['H']), int(group['M']), int(group['S']))
        e.keywords = Lexer(group['message']).keywords
        return e

    linehandlers['^'+time+nick+'\s(?P<message>.+)$'] = group_to_event
    linehandlers['.+Log opened\s(?P<Day>.+)\s(?P<month>.+)\s(?P<date>.+)\s'+time+'\s(?P<year>.+)'] = lambda g: stats.update(g)

    for line in file.xreadlines():
        #print line

        stats['lines'] += 1
        if stats['lines'] == max: break
        
        # TODO print dict keys not tuple indexes
        if stats['lines'] % 20 == 0: print " %s lines read, %s/%s events saved to %s" % (stats['lines'],stats['saved'],stats['events'], target)
        for pattern in linehandlers:
            match = re.match(pattern, line)
            if match:
                result = linehandlers[pattern](match.groupdict())
                if result:
                    stats['events'] += 1
                    if len(result.keywords) > threshold:
                        save_event(result)
                        stats['saved'] += 1


def recursive_import_log(basedir=None, threshold=4):
    def visit(to_index, dirname, names):
        logfiles.extend([(dirname +'/'+ name,name.replace('.log','')) for name in names if (name.endswith(".log") and name.startswith("#"))])
    
    logfiles = []
    os.path.walk(basedir, visit, logfiles)
    [import_irc_log(filename, target, max=-1, threshold=4) for (filename,target) in logfiles]

def save_event(event):
    i = model.intelligence(
        source=event.source(),
        target=event.target(),
        keywords=' '.join(event.keywords),
        message=event.arguments()[0],
        created=event.timestamp
    )

