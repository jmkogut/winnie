from winnie.data import model

from winnie.protocols.irc.communicator import Communicator
from framework.Controllers import JSONController as json

@json
def servers(request):
    c = Communicator()
    return c.server_list

@json
def channels(request, server=None):
    c = Communicator()
    return [channel for channel in c.channels]

@json
def statistics(request):
    c = Communicator()
    return {
        'factoids': model.intelligence.select().count()
    }
