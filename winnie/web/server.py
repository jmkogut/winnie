import threading

from paste import httpserver
from framework.Router import Router

from winnie.util.logger import Logger
logger = Logger()

from winnie.util.singletons import Singleton
from winnie.web import routes
from winnie.settings import HTTP_ADDRESS as address

from framework.Controllers import JSONController as json

class Server(threading.Thread):
    """
    HTTP server for winnie
    """
    __metaclass__ = Singleton

    def __init__(self):
        self.running = True
        self.router = None

        threading.Thread.__init__(self)

    def run(self):
        self.router = Server.build_routes()
        Server.run_server(self.router, address)
    
    @staticmethod
    def build_routes():
        router = Router()
        for (route,handler) in routes.routes:
            route += '/?$'
            logger.info("Added %s for %s" % (handler.handlername, route))
            router.add_route(route, handler)
        
        # Listing
        router.add_route('^',
            json(lambda request: [(handler.handlername, route) for (route, handler) in routes.routes])
        )

        return router

    @staticmethod
    def run_server(router, listen):
        return httpserver.serve(router, **listen)
