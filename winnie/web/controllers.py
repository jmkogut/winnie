from winnie.data import model
from winnie.protocols.irc.communicator import Communicator
from framework.Controllers import JSONController as json
from winnie import errors

@json
def json_api(request, entity=None, action=None, id=None):
    if not (entity and action): raise errors.web.InvalidRequest('Please specify an entity and an action.')
    
    allowed_entities = {
        "intelligence": model.intelligence,
        "account": model.account,
        "account_mask": model.account_mask,
        "phrase": model.phrase,
        "phrase_category": model.phrase_category
    }
    
    if entity not in allowed_entities: raise errors.web.InvalidRequest('Entity is not valid.')

    allowed_actions = {
        'get': lambda entity, id: entity.get(id).as_dict(),
        'list': lambda entity, _: [e.id for e in entity.select()]
    }
    
    if action not in allowed_actions: raise errors.web.InvalidRequest('Action is not valid.')

    return allowed_actions[action](allowed_entities[entity], id)

@json
def servers(request):
    c = Communicator()
    return c.server_list

@json
def channels(request):
    c = Communicator()
    return [channel for channel in c.channels]

@json
def channel_info(request, channel=None):
    return {
        "name": channel or "None"
    }

@json
def account_info(request, id=0):
    account = model.account.get(id)
    return {
        'email': account.email
        #'masks': account_masks.selectBy(account=account)
    }

@json
def info(request):
    c = Communicator()
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

@json
def get_log(request, since=None):
    pass
