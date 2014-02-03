from winnie import hook
from winnie import text
import config
import json
import urllib2

KEY_FILE = "/home/joshua/.lastfm.py"
def read_key():
    c = compile(open(KEY_FILE, 'U').read(), KEY_FILE, 'exec')
    ns = {}
    eval(c, ns)
    return (ns['API_KEY'], ns['SECRET'])

def get_tracks_for( user='jmkogut' ):
    key = read_key()
    uri = config.LASTFM_NP % (user, key[0] )
    data = json.loads( urllib2.urlopen(uri).read() )
    last = data.get('recenttracks').get('track')[0]
    return "np on last.fm (%s) // %s - %s" % (user, last.get("artist").get("#text"), last.get("name"))

@hook.cmd
def np( event, client=None, **kw ):
    s,t,m = event
    act = text.is_cmd( 'np', event, default=text.mask_to_nick(s) )
    if act:
        key = read_key()
        response = get_tracks_for( act )
        client.say(t, response.encode('ascii'))
    return
