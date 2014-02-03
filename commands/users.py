from winnie import model
from winnie import hook
from winnie import text

import datetime

@hook.cmd
def lastseen( event, client=None, **kw ):
    '''Updates lastseen every time a user talks.'''
    s,t,m = event
    u = model.User.find_by(s)
    u.lastseen = datetime.datetime.utcnow()
    model.session.add(u)
    model.session.commit()

@hook.cmd
def seen( event, client=None, **kw ):
    '''Notifies someone how long another person has been afk.'''
    s,t,m = event
    arg = text.is_cmd( 'seen', (s,t,m) )
    if arg:
        u = model.User.find_by( arg )
        span = datetime.datetime.utcnow().replace(microsecond=0) - \
                               u.lastseen.replace(microsecond=0)

        note = '%s has been gone for %s' % (arg, span)
        client.say(t, note.encode('ascii'))
