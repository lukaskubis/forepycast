darkskylib
==========

This  library for the `Dark Sky
API <https://darksky.net/dev/docs>`__ provides access to detailed
weather information from around the globe.

Quick start
-----------

Before you start using this library, you need to get your API key
`here <https://darksky.net/dev/register>`__.


API Calls
~~~~~~~~~

Function ``forecast`` handles all request parameters and returns a
``Forecast`` object.

.. code:: python

    >>> from darksky.forecast import Forecast
    >>> boston = Forecast(key, 42.3601, -71.0589)
    >>>

The first 3 positional arguments are identical to the 3 required
parameters for API call. The optional query parameters need to be
provided as keyword arguments.

Using ``time`` argument will get you a **time machine call**.
Using ``timeout`` argument will set default `request timeout <http://docs.python-requests.org/en/master/api/#requests.request>`__ .

.. code:: python

    >>> BOSTON = key, 42.3601, -71.0589
    >>> from datetime import datetime as dt
    >>> t = dt(2013, 5, 6, 12).isoformat()
    >>> boston = Forecast(*BOSTON, time=t)
    >>> boston.time
    1367866800

Data Points and Data Blocks
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The values as well as ``DataPoint`` and ``DataBlock`` objects are
accessed using instance attributes or dictionary keys. You can access
current values directly, without going through ``currently`` data point.

.. code:: python

    >>> boston['currently']['temperature']
    60.72
    >>> boston.temperature
    60.72

**Data blocks** are indexable and iterable by their ``data`` values.

.. code:: python

    >>> len(boston.hourly)
    24
    >>>
    >>> boston.hourly[1].temperature
    59.49
    >>>
    >>> # list temperatures for next 10 hours
    ... [hour.temperature for hour in boston.hourly[:10]]
    [60.83, 59.49, 58.93, 57.95, 56.01, 53.95, 51.21, 49.21, 47.95, 46.31]

Nonexistent attributes will raise ``AttributeError`` and dictionary keys
``KeyError`` the way you'd expect.

Raw data
~~~~~~~~

To get the raw data dictionary, you can either access it through
instance attributes or navigate to it through dictionary keys, the same
way you would navigate the actual dictionary.

.. code:: python

    >>> boston.hourly[2]
    {'ozone': 290.06, 'temperature': 58.93, 'pressure': 1017.8, 'windBearing': 274, 'dewPoint': 52.58, 'cloudCover': 0.29, 'apparentTemperature': 58.93, 'windSpeed': 7.96, 'summary': 'Partly Cloudy', 'icon': 'partly-cloudy-night', 'humidity': 0.79, 'precipProbability': 0, 'precipIntensity': 0, 'visibility': 8.67, 'time': 1476410400}
    >>>
    >>> boston['hourly']['data'][2]
    {'ozone': 290.06, 'temperature': 58.93, 'pressure': 1017.8, 'windBearing': 274, 'dewPoint': 52.58, 'cloudCover': 0.29, 'apparentTemperature': 58.93, 'windSpeed': 7.96, 'summary': 'Partly Cloudy', 'icon': 'partly-cloudy-night', 'humidity': 0.79, 'precipProbability': 0, 'precipIntensity': 0, 'visibility': 8.67, 'time': 1476410400}

Flags and Alerts
~~~~~~~~~~~~~~~~

All dashes ``-`` in attribute names of **Flags** objects are replaced by
underscores ``_``. This doesn't affect the dictionary keys.

.. code:: python

    >>> # instead of 'boston.flags.isd-stations'
    ... boston.flags.isd_stations
    ['383340-99999', '383390-99999', '383410-99999', '384620-99999', '384710-99999']
    >>>
    >>> boston.flags['isd-stations']
    ['383340-99999', '383390-99999', '383410-99999', '384620-99999', '384710-99999']

Even though **Alerts** are represented by a list, the data accessibility
through instance attributes is preserved for alerts in the list.

.. code:: python

    >>> boston.alerts[0].title
    'Freeze Watch for Norfolk, MA'

Updating data
~~~~~~~~~~~~~

Use ``refresh()`` method to update data of a ``Forecast`` object. The
``refresh()`` method takes optional queries (including ``time``, making
it a **Time machine** object) as keyword arguments. Calling
``refresh()`` without any arguments will set all queries to default
values. Use ``timeout`` argument to set the request timeout.

.. code:: python

    >>> boston.refresh()
    >>> (boston.time, boston.temperature, len(boston.hourly))
    (1476403500, 60.72, 49)
    >>>
    >>> boston.refresh(units='si', extend='hourly')
    >>> (boston.time, boston.temperature, len(boston.hourly))
    (1476404205, 15.81, 169)
    >>>
    >>> boston.refresh(units='us')
    >>> (boston.time, boston.temperature, len(boston.hourly))
    (1476404489, 60.57, 49)

For Developers
~~~~~~~~~~~~~~

Response headers are stored in a dictionary under ``response_headers``
attribute.

.. code:: python

    >>> boston.response_headers['X-response-Time']
    '146.035ms'

Example script
--------------

.. code:: python

    from darksky.forecast import Forecast
    from datetime import date, timedelta

    BOSTON = 42.3601, 71.0589

    weekday = date.today()
    with Forecast('API_KEY', *BOSTON) as boston:
        print(boston.daily.summary, end='\n---\n')
        for day in boston.daily:
            day = dict(day = date.strftime(weekday, '%a'),
                       sum = day.summary,
                       tempMin = day.temperatureMin,
                       tempMax = day.temperatureMax
                       )
            print('{day}: {sum} Temp range: {tempMin} - {tempMax}'.format(**day))
            weekday += timedelta(days=1)

Output:

::

    Light rain on Friday and Saturday, with temperatures bottoming out at 48°F on Tuesday.
    ---
    Sun: Partly cloudy in the morning. Temp range: 44.86 - 57.26°F
    Mon: Mostly cloudy in the morning. Temp range: 44.26 - 55.28°F
    Tue: Clear throughout the day. Temp range: 36.85 - 47.9°F
    Wed: Partly cloudy starting in the afternoon, continuing until evening. Temp range: 33.23 - 47.93°F
    Thu: Light rain overnight. Temp range: 35.75 - 49.71°F
    Fri: Light rain in the morning and afternoon. Temp range: 45.47 - 57.11°F
    Sat: Drizzle in the morning. Temp range: 43.3 - 62.08°F
    Sun: Clear throughout the day. Temp range: 39.81 - 60.84°F

License
-------

The code is available under terms of `MIT
License <https://raw.githubusercontent.com/lukaskubis/darkskylib/master/LICENSE>`__
