from os import stat
from japronto.exception import NotImplemented

from .base import BaseMiddleware

class Middleware(BaseMiddleware):
    def process_resp(self, req, resp):
        return resp
