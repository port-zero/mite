class HttpException(Exception):
    name = ""
    status_code = None

    def __repr__(self):
        return "HTTP {} {}".format(self.status_code, self.name)

    def __str__(self):
        return repr(self)

    def __unicode__(self):
        return repr(self)


class NotFound(HttpException):
    name = "Not Found"
    status_code = 404


exceptions = [
    NotFound
]


def get_exception(status_code):
    for cls in exceptions:
        if cls.status_code == status_code:
            return cls()
