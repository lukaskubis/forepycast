# forecast.py
from __future__ import print_function

import json
from builtins import super

import requests

from .data import DataPoint

_API_URL = 'https://api.darksky.net/forecast'


class Forecast(DataPoint):

    def __init__(self, key, latitude, longitude, time=None, timeout=None, **queries):
        super(Forecast, self).__init__({})
        self._queries = None
        self.timeout = None
        self.response_headers = None
        self._parameters = dict(key=key, latitude=latitude, longitude=longitude,
                                time=time)
        self.refresh(timeout, **queries)

    def __setattr__(self, key, value):
        if key in ('_queries', '_parameters', '_data'):
            return object.__setattr__(self, key, value)
        return super().__setattr__(key, value)

    def __getattr__(self, key):
        currently = object.__getattribute__(self, 'currently')
        _data = object.__getattribute__(currently, '_data')
        if key in _data.keys():
            return _data[key]
        return object.__getattribute__(self, key)

    def __enter__(self):
        return self

    def __exit__(self, exit_type, value, tb):
        del self

    @property
    def url(self):
        time = self._parameters['time']
        timestr = ',{}'.format(time) if time else ''
        uri_format = '{url}/{key}/{latitude},{longitude}{timestr}'
        return uri_format.format(url=_API_URL, timestr=timestr, **self._parameters)

    def refresh(self, timeout=None, **queries):
        self._queries = queries
        self.timeout = timeout
        request_params = {
            'params': self._queries,
            'headers': {'Accept-Encoding': 'gzip'},
            'timeout': timeout
        }

        response = requests.get(self.url, **request_params)
        self.response_headers = response.headers
        response.raise_for_status()
        return super().__init__(json.loads(response.text))
