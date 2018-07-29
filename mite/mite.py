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

    def request(self, scheme, url, data=None, params=None):
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

        res = fn(url, headers=headers, json=data, params=params)

        if res.status_code >= 300:
            self._raise_exception(res.status_code)

        if not res.content:
            return None

        try:
            return res.json()
        except ValueError:
            return res.content

    def _raise_exception(self, code):
        raise errors.get_exception(code)

    def get(self, url, data=None, params=None):
        """
        Low-level GET request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("post", url, data, params)

    def put(self, url, data=None, params=None):
        """
        Low-level PUT request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("put", url, data, params)

    def post(self, url, data=None, params=None):
        """
        Low-level POST request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("post", url, data, params)

    def patch(self, url, data=None, params=None):
        """
        Low-level PATCH request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("patch", url, data, params)

    def delete(self, url, data=None, params=None):
        """
        Low-level DELETE request interface to mite. Takes a URL to request
        (relative), and optionally data to add to the request. Either returns
        the JSON body of the request or raises a HttpException.

        """
        return self.request("delete", url, data, params)

    def get_account(self):
        """
        Get account data.
        """
        return self.get("/account.json")

    def get_me(self):
        """
        Get your user data.
        """
        return self.get("/myself.json")

    def get_entries(self, **kwargs):
        """
        Get all time entries. Accepts the filters `user_id`, `customer_id`,
        `project_id`, `service_id`, `note`, `at`, `from`, `to`, `billable`,
        `locked`, `tracking`, `sort`, `direction`, `group_by`, `limit`, and
        `page`. Pass them as keyword arguments. More information about them
        can be found in the [Mite
        docs](https://mite.yo.lk/en/api/time-entries.html).
        """
        return self.get("/time_entries.json", params=kwargs)

    def get_daily(self, date=None):
        """
        Get time entries for a date (defaults to today).
        """
        if date == None:
            return self.get("/daily.json")
        url = "/daily/{}/{}/{}.json".format(date.year, date.month, date.day)
        return self.get(url)

    def get_entry_by_id(self, id_):
        """
        Get a time entry by its ID.
        """
        return self.get("/time_entries/{}.json".format(id_))

    def _wrap_entry(self, data):
        return {
            "time_entry": kwargs
        }

    def create_entry(self, **kwargs):
        """
        Creates a new time entry on Mite. Takes a data dictionary with the keys
        `date_at` (a date string in `YYYY-MM-DD` format), `minutes` (an int),
        `note` (the entry text), `user_id`, `project_id`, `service_id`, and
        `locked`. All of them are optional.
        """
        data = _wrap_entry(kwargs)

        return self.post("/time_entries.json", data)

    def edit_entry(self, id_, **kwargs):
        """
        Edits a time entry by ID. Takes the same data as `create_entry`, but
        requires an ID to work. It also takes a `force` parameter that, when set
        to True, allows administrators to edit locked entries.
        """
        data = _wrap_entry(kwargs)

        return self.patch("/time_entries/{}.json".format(id_), data)

    def delete_entry(self, id_):
        """
        Deletes an entry by ID.
        """
        return self.delete("/time_entries/{}.json".format(id_))

    def show_tracker(self):
        """
        Gets the current time tracker state for the authenticated user.
        """
        return self.get("/tracker.json")

    def start_tracker(self, id_, **kwargs):
        """
        Starts a tracker for the time entry identified by `id_`.
        """
        data = None
        if kwargs:
            data = {
                "tracker": {
                    "tracking_time_entry": kwargs
                }
            }
        return self.patch("/tracker/{}.json".format(id_), data=data)

    def stop_tracker(self, id_):
        """
        Stops a tracker for the time entry identified by `id_`.
        """
        return self.delete("/tracker/{}.json".format(id_))

    def list_bookmarks(self):
        """
        Gets all bookmarks.
        """
        return self.get("/time_entries/bookmarks.json")

    def get_bookmark(self, id_):
        """
        Get a bookmark by ID.
        """
        return self.get("/time_entries/boomarks/{}.json".format(id_))

    def time_entries_for_bookmark(self, id_):
        """
        Get all time entries associated with a bookmark.
        """
        return self.get("/time_entries/bookmarks/:{}/follow.json".format(id_))
