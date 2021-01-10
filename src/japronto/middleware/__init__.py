from collections import defaultdict
import copy
from functools import wraps

from ..common.provider_api import MWProvider
from ..common import utils
from .demo import Middleware as Demo
from ..response import JsonResponse


ROUTE_SKIP_MW_MAPPING = defaultdict(list)


def resp_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        err_body = {
            'err_code': 0,
            'err_msg': 'ok'
        }
        try:
            resp = func(*args, **kwargs)
            resp.json.update(**err_body)
        except Exception as e:
            err_body.update(
                err_code=getattr(e, 'code', 400),
                err_msg=str(e.args[0])
            )
            resp = JsonResponse(json=err_body)
        req = args[2]
        return req.Response(**dict(resp))

    return wrapper


class Middlewares(object):
    def __init__(self, app):
        self.app = app
        self._middlewares = IMW
        self._pipeline = None

    def add_middleware(self, mw):
        """insert middleware to the head of the list."""
        self._middlewares.insert(0, mw)

    def add_middlewares(self, mws):
        mws_copy = copy.copy(mws)
        mws_copy.extend(self._middlewares)
        self._middlewares = mws_copy

    def __init_route_skip_mw(self):
        for mw, skip_views in ROUTE_SKIP_MW_MAPPING.items():
            getattr(MWProvider, mw).skip_views = skip_views

    @property
    def pipeline(self):
        if not self._pipeline:
            app = self.app
            for mw in reversed(self._middlewares):
                app = mw(app)
            self._pipeline = app
            # NOTE(ql): lock the middlewares, these should only ever be
            # instantiated before running keystone.
            MWProvider.lock_provider_registry()
            self.__init_route_skip_mw()
        return self._pipeline

    @resp_handler
    def __call__(self, handler, req):
        return self.pipeline(handler, req)


def skip_middlewares(*mws):
    def _skip_middlewares(view_func):
        for mw in mws:
            ROUTE_SKIP_MW_MAPPING[mw].append(utils.unique_func_name(view_func))
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            return view_func(*args, **kwargs)
        return wrapper
    return _skip_middlewares


IMW = [Demo]
