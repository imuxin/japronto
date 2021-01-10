from ..common import provider_api
from ..common import utils
from ..response.cresponse import Response


class BaseMiddleware(object):
    _provider_api = ''

    def __init__(self, app) -> None:
        self.app = app
        self.skip_views = []
        self.__register_provider_api()

    def __register_provider_api(self):
        provider_api.MWProvider._register_provider_api(
            name=self._provider_api, obj=self)

    def process_req(self, req):
        pass

    def process_resp(self, req, resp):
        """
        You must return Response.
        """
        return resp

    def __call__(self, handler, req):
        """
        process_req and process_resp will skip if handler func is in
        `self.skip_views`
        """
        is_skip = utils.unique_func_name(handler) in self.skip_views
        if not is_skip:
            resp = self.process_req(req)
            if isinstance(resp, Response):
                return resp

        if isinstance(self.app, self.__class__):
            resp = self.app(handler, req)
        else:
            resp = handler(req)
        if not is_skip:
            resp = self.process_resp(req, resp)
        return resp
