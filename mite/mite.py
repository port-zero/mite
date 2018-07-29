"""Main mite module"""
import requests

from mite import errors

class Mite():
    """
    The class for interacting with mite. Create an instance using a team and
    api key and start requesting!
    """
    # TODO: reduce code duplication

    def __init__(self, team, api_key):
        """
        Constructs a new Mite object.

        """
        self.team = team
        self.api_key = api_key
        self.url = "https://{}.mite.yo.lk{}"

    def request(self, scheme, url, data=None, params=None):
        """
        Low-level request interface to mite. Takes a HTTP request scheme (lower
        case!), a URL to request (relative), and optionally data to add to the
        request. Either returns the JSON body of the request or raises a 
        HttpException.

        """
        url = self.url.format(self.team, url)
        headers = {
            "X-MiteApikey": self.api_key,
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
        return self.request("get", url, data, params)

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

    def list_entries(self, **kwargs):
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

    def get_entry(self, id_):
        """
        Get a time entry by its ID.
        """
        return self.get("/time_entries/{}.json".format(id_))

    def _wrap_entry(self, key, data):
        return { key: kwargs }

    def create_entry(self, **kwargs):
        """
        Creates a new time entry on Mite. Takes a data dictionary with the keys
        `date_at` (a date string in `YYYY-MM-DD` format), `minutes` (an int),
        `note` (the entry text), `user_id`, `project_id`, `service_id`, and
        `locked`. All of them are optional.
        """
        data = _wrap_dict("time_entry", kwargs)

        return self.post("/time_entries.json", data)

    def edit_entry(self, id_, **kwargs):
        """
        Edits a time entry by ID. Takes the same data as `create_entry`, but
        requires an ID to work. It also takes a `force` parameter that, when set
        to True, allows administrators to edit locked entries.
        """
        data = _wrap_dict("time_entry", kwargs)

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
            data = self._wrap_dict("tracker",
                self._wrap_dict("tracking_time_entry", kwargs))
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

    def list_customers(self, **kwargs):
        """
        List all active customers. You can filter by `name`, `limit`, or `page`.
        """
        return self.get("/customers.json", params=kwargs)

    def list_archived_customers(self, **kwargs):
        """
        List all archived customers. You can filter by `name`, `limit`, or
        `page`.
        """
        return self.get("/customers/archived.json", params=kwargs)

    def get_customer(self, id_):
        """
        Get a single customer by ID.
        """
        return self.get("/customers/{}.json".format(id_))

    def create_customer(self, name, **kwargs):
        """
        Creates a customer with a name. All other parameters are optional. They
        are: `note`, `active_hourly_rate`, `hourly_rate`,
        `hourly_rates_per_service`, and `archived`.
        """
        data = self._wrap_dict("customer", kwargs)
        data["customer"]["name"] = name
        return self.post("/customers.json", data=data)

    def edit_customer(self, id_, **kwargs):
        """
        Edits a customer by ID. All fields available at creation can be updated
        as well. If you want to update hourly rates retroactively, set the
        argument `update_hourly_rate_on_time_entries` to True.
        """
        data = self._wrap_dict("customer", kwargs)
        return self.patch("/customers/{}.json".format(id_), data=data)

    def delete_customer(self, id_):
        """
        Deletes a customer by ID. If the customer has associated projects, you
        will get HTTP 422 (Unprocessable Entity) back.
        """
        return self.delete("/customers/{}.json".format(id_))

    def list_projects(self, **kwargs):
        """
        List all active projects. You can filter by `name`, `customer_id`,
        `limit`, or `page`.
        """
        return self.get("/projects.json", params=kwargs)

    def list_archived_projects(self, **kwargs):
        """
        List all archived projects. You can filter by `name`, `customer_id`,
        `limit`, or `page`.
        """
        return self.get("/projects/archived.json", params=kwargs)

    def get_project(self, id_):
        """
        Get a project by its ID.
        """
        return self.get("/projects/{}.json".format(id_))

    def create_project(self, name, **kwargs):
        """
        Creates a project with a name. All other parameters are optional. They
        are: `note`, `customer_id`, `budget`, `budget_type`, 
        `active_hourly_rate`, `hourly_rate`, `hourly_rates_per_service`, and
        `archived`.
        """
        data = self._wrap_dict("project", kwargs)
        data["customer"]["name"] = name
        return self.post("/projects.json", data=data)

    def edit_project(self, id_, **kwargs):
        """
        Edits a project by ID. All fields available at creation can be updated
        as well. If you want to update hourly rates retroactively, set the
        argument `update_hourly_rate_on_time_entries` to True.
        """
        data = self._wrap_dict("project", kwargs)
        return self.patch("/projects/{}.json".format(id_), data=data)

    def delete_project(self, id_):
        """
        Deletes a project by ID. If the project has associated time entries, you
        will get HTTP 422 (Unprocessable Entity) back.
        """
        return self.delete("/projects/{}.json".format(id_))

    def list_services(self, **kwargs):
        """
        List all active services. You can filter by `name`, `customer_id`,
        `limit`, or `page`.
        """
        return self.get("/services.json", params=kwargs)

    def list_archived_services(self, **kwargs):
        """
        List all archived services. You can filter by `name`, `customer_id`,
        `limit`, or `page`.
        """
        return self.get("/services/archived.json", params=kwargs)

    def get_service(self, id_):
        """
        Get a service by its ID.
        """
        return self.get("/services/{}.json".format(id_))

    def create_service(self, name, **kwargs):
        """
        Creates a service with a name. All other parameters are optional. They
        are: `note`, `hourly_rate`, `billable`, and `archived`.
        """
        data = self._wrap_dict("service", kwargs)
        data["customer"]["name"] = name
        return self.post("/services.json", data=data)

    def edit_service(self, id_, **kwargs):
        """
        Edits a service by ID. All fields available at creation can be updated
        as well. If you want to update hourly rates retroactively, set the
        argument `update_hourly_rate_on_time_entries` to True.
        """
        data = self._wrap_dict("service", kwargs)
        return self.patch("/services/{}.json".format(id_), data=data)

    def delete_service(self, id_):
        """
        Deletes a service by ID. If the service has associated time entries, you
        will get HTTP 422 (Unprocessable Entity) back.
        """
        return self.delete("/services/{}.json".format(id_))

    def list_users(self, **kwargs):
        """
        List all active users. You can filter by `name`, `email`, `customer_id`,
        `limit`, or `page`.
        """
        return self.get("/users.json", params=kwargs)

    def list_archived_users(self, **kwargs):
        """
        List all archived users. You can filter by `name`, `email`,
        `customer_id`, `limit`, or `page`.
        """
        return self.get("/users/archived.json", params=kwargs)

    def get_user(self, id_):
        """
        Get a user by its ID.
        """
        return self.get("/users/{}.json".format(id_))
