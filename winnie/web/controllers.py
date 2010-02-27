from winnie.data import model
from winnie.protocols.irc.connection import Connection
from winnie.protocols.irc.connection import ConnectionModel as cmodel

from framework.Controllers import JSONController as json
from winnie import errors

@json
def simple_api(request, entity=None, action=None, id=None):
    if not (entity and action): raise errors.web.InvalidRequest('Please specify an entity and an action.')
    
    allowed_entities = {
        "intelligence": model.intelligence,
        "account": model.account,
        "account_mask": model.account_mask,
        "phrase": model.phrase,
        "phrase_category": model.phrase_category,

        "channel": cmodel.channel,
        "server": cmodel.server,
    }
    
    if entity not in allowed_entities: raise errors.web.InvalidRequest('Entity is not valid.')

    allowed_actions = {
        'get': lambda entity, id: entity.get(id).as_dict(),
        'list': lambda entity, _: [e.ref() for e in entity.select()]
    }
    
    if action not in allowed_actions: raise errors.web.InvalidRequest('Action is not valid.')

    return allowed_actions[action](allowed_entities[entity], id)

@json
def log(request, channel=None, since=None):
    if not channel: raise errors.web.InvalidRequest("You must supply a channel")
    return cmodel.log.selectBy(channel=channel, since=since)

@json
def info(request):
    c = Connection()
    return {
        'database': {    
            'intelligence': model.intelligence.select().count(),
            'accounts': model.account.select().count(),
            'account_masks': model.account_mask.select().count()
        }
    }

@json
def echo(request, str="Nothing entered"):
    return str
