import http.client


class Error(Exception):
    """Base error class.

    Child classes should define an HTTP status code, title, and a
    message_format.

    """

    code = None
    title = None
    message_format = None

    def __init__(self, message=None, **kwargs):
        try:
            message = self._build_message(message, **kwargs)
        except KeyError:
            message = self.message_format

        super(Error, self).__init__(message)

    def _build_message(self, message, **kwargs):
        """Build and returns an exception message.

        :raises KeyError: given insufficient kwargs

        """
        if message:
            return message
        return self.message_format % kwargs


class NotFound(Error):
    message_format = ("Not Found")
    code = int(http.client.NOT_FOUND)
    title = http.client.responses[http.client.NOT_FOUND]


class InternalServerError(Error):
    message_format = ("Internal Server Error")
    code = int(http.client.INTERNAL_SERVER_ERROR)
    title = http.client.responses[http.client.INTERNAL_SERVER_ERROR]

class NotImplemented(Error):
    message_format = ("The action you have requested has not"
                      " been implemented.")
    code = int(http.client.NOT_IMPLEMENTED)
    title = http.client.responses[http.client.NOT_IMPLEMENTED]
