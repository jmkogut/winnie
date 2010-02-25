import threading

from paste import httpserver
from framework.Router import Router

from winnie.util import Singleton
from winnie.web.urls import urls
from winnie.settings import HTTP_ADDRESS as address

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
        self.router = Server.build_routes(urls)
        Server.run_server(self.router, address)
    
    @staticmethod
    def build_routes(routes):
        router = Router()
        for (route,handler) in routes:
            router.add_route(route, handler)

        return router

    @staticmethod
    def run_server(router, listen):
        return httpserver.serve(router, **listen)
