from japronto.response.cresponse import Response


class BaseMiddleware(object):
    def __init__(self, app) -> None:
        self.app = app

    def process_req(self, req):
        pass

    def process_resp(self, req, resp):
        """
        You must return Response.
        """
        return resp

    def __call__(self, handler, req):
        resp = self.process_req(req)
        if isinstance(resp, Response):
            return resp

        if isinstance(self.app, self.__class__):
            resp = self.app(handler, req)
        else:
            resp = handler(req)
        return self.process_resp(req, resp)
