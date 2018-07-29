# mite-python

An idiomatic Python wrapper for the Mite API. Work in progess.

## Todo

Currently unimplemented is a wrapper around:

- Projects
- Services
- Users

## Installation

`mite` can be obtained through pip:

```
pip install mite
```

## Usage

All requests are encapsulated in a `Mite` object. To construct this object, you
need to supply it with an API key and a team name (your subdomain on Mite):

```python
from mite import Mite

mite = Mite("<api key>", "<team name")
```

Then you can start requesting. Let’s get a list of time entries!

```python
print(mite.list_entries())
```

This will return a dictionary representing the JSON body of the response. If it
fails it will throw an exception that inherits from `mite.HttpException`, for
instance `mite.NotFound` for `404 Not Found` errors.

For a comprehensive list of functions, take a look at [the generated
documentation]().

<hr/>

Have fun!
