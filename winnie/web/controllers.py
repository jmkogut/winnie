from winnie.protocols.irc.communicator import Communicator
from framework.Controllers import Controller as controller

@controller
def hello(request):
    return 'Hello, World!<br />You called %s' % request.path_info

@controller
def server(request):
	return "Goodbye!"

@controller
def channels(request):
    c = Communicator()
    
    return ", ".join([channel for channel in c.channels])
