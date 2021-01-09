from .demo import Middleware as Demo
from ..common.decorator import resp_handler

class Middlewares(object):
    def __init__(self, app):
        self.app = app
        self._middlewares = IMW

    def add_middleware(self, mdw):
        self._middlewares.append(mdw)

    @resp_handler
    def __call__(self, handler, req):
        app = self.app
        for mw in reversed(self._middlewares):
            app = mw(app)
        return app(handler, req)


IMW = [Demo]
