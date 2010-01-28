import memcache

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import Intelligence, Account, Phrase
import md5
def index(request, channel):
    c = memcache.Client(('localhost',))
    desired_chans = c.get('winniepooh.desiredchans') or []

    if ('#'+channel) not in desired_chans:
        desired_chans.append('#'+channel)
        c.set('winniepooh.desiredchans', desired_chans)

    return render_to_response('Test/index.html', {'channel':channel})

def since(request, channel, hash):
    c = memcache.Client(('localhost',))
    log = c.get('winniepooh.log')
    
    print hash

    if (log):
        output = []
        found = False
        
        for stamp,line in log:
            digest = md5.new(stamp.__str__()).hexdigest()
            #print "[%s] %s"%(digest,line)
            
            if len(hash) is not 32:
                found = True
            line = unicode(line)
            if found and (line.find('#%s'%channel) > -1 or line.find(' ++')==0 or line.find(' **')==0):
                output.append((
                    digest,
                    line
                ))

            if digest == hash:
                found = True
    else:
        output = [('', 'winniepooh is not currently running')]

    return render_to_response('Test/response.json', {'items':smart_unicode(output)})

def stats(request):
    c = memcache.Client(('localhost',))
    
    c.set('winniepooh.statcredits', 1)
    stats = c.get('winniepooh.stats')
    
    if stats:
        output = stats
    else:
        output = []

    return render_to_response('Test/response.json', {'items':output})

def nick(request, nick):
    intelligences = Intelligence.objects.filter(mask__startswith="%s!"%nick).order_by('-created')[:10]

    return render_to_response('Test/nick.html', {'items':intelligences, 'nick':nick})
