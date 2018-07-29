"""Main mite module"""
import requests

from mite import errors

class Mite():
    """
    The class for interacting with mite. Create an instance using a team and
    api key and start requesting!
    """

    def __init__(self, team, api_key):
        """
        Constructs a new Mite object.

        """
        self.team = team
        self.api_key = api_key
        self.url = "https://{}.mite.yo.lk/{}"

    def request(self, scheme, url, data=None):
        """
        Low-level request interface to mite. Takes a HTTP request scheme (lower
        case!), a URL to request (relative), and optionally data to add to the
        request. Either returns the JSON body of the request or raises a 
        HttpException.

        """
        url = self.url.format(config.TEAM, url)
        headers = {
            "X-MiteApikey": config.API_KEY,
            "User-Agent":
                "mite Python wrapper: https://github.com/port-zero/mite",
            "Content-Type": "application/json",
        }
        # this is a nice little hack to make the API nicer
        # we pass the scheme as string, but have it as attributes in requests
        fn = requests.__getattribute__(scheme)

        res = fn(url, headers=headers, data=json.dumps(data or {}))

        if res.status_code >= 300:
            self._raise_exception(res.status_code)

        return res.json()

    def _raise_exception(self, code):
        raise errors.get_exception(code)

    def get(self, url, data=None):
        """
        Low-level GET request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("post", url, data)

    def put(self, url, data=None):
        """
        Low-level PUT request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("put", url, data)

    def post(self, url, data=None):
        """
        Low-level POST request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("post", url, data)

    def delete(self, url, data=None):
        """
        Low-level DELETE request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("delete", url, data)

    def push_update(self, data):
        """
        Pushes a new update to Mite. Takes a data dictionary with the keys
        `date_at` (a date string in `YYYY-MM-DD` format), `minutes` (an int),
        and `note` (the entry text).

        """
        data = {
            "time_entry": data
        }

        return self.post("/time_entries.json", data)
