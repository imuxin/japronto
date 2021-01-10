from .base import BaseMiddleware

class Middleware(BaseMiddleware):
    _provider_api = 'demo'

    def process_resp(self, req, resp):
        return resp
