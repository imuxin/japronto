from japronto.exception import Error


class Response(object):
    __slots__ = []


class TextResponse(Response):
    __slots__ = ['code', 'text', 'headers', 'cookies']
    def __init__(self, code=200, text='', headers={}, cookies={}) -> None:
        self.code = code
        self.text = text
        self.headers = headers
        self.cookies = cookies

    def __iter__(self):
        for key in self.__slots__:
            yield key, getattr(self, key)


class JsonResponse(Response):
    __slots__ = ['code', 'json', 'headers', 'cookies']
    def __init__(self, code=200, json={}, headers={}, cookies={}) -> None:
        self.code = code
        self.json = json
        self.headers = headers
        self.cookies = cookies

    def __iter__(self):
        for key in self.__slots__:
            yield key, getattr(self, key)
