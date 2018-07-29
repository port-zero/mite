class HttpException(Exception):
    name = ""
    status_code = None

    def __init__(self, status_code=None):
        if status_code:
            self.status_code = status_code

    def __repr__(self):
        return "HTTP {} {}".format(self.status_code, self.name)

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)


class BadRequest(HttpException):
    name = "Bad Request"
    status_code = 400


class Unauthorized(HttpException):
    name = "Unauthorized"
    status_code = 401


class Forbidden(HttpException):
    name = "Forbidden"
    status_code = 403


class NotFound(HttpException):
    name = "Not Found"
    status_code = 404


class MethodNotAllowed(HttpException):
    name = "Method Not Allowed"
    status_code = 405


class Locked(HttpException):
    name = "Locked"
    status_code = 423


class TooManyRequests(HttpException):
    name = "Too Many Requests"
    status_code = 429


class InternalServerError(HttpException):
    name = "Internal Server Error"
    status_code = 500


class BadGateway(HttpException):
    name = "Bad Gateway"
    status_code = 502


class ServiceUnavailable(HttpException):
    name = "Service Unavailable"
    status_code = 503


class ConnectionTimeout(HttpException):
    name = "Connection Timeout"
    status_code = 522


exceptions = [
]

def _find_exceptions():
    for name, obj in globals().items():
        try:
            is_http_exception = issubclass(obj, HttpException)
        except TypeError:
            is_http_exception = False
        if not is_http_exception or obj.status_code is None:
            continue
        exceptions.append(obj)

_find_exceptions()
del _find_exceptions


def get_exception(status_code):
    for cls in exceptions:
        if cls.status_code == status_code:
            return cls()
    return HttpException(status_code=status_code)
