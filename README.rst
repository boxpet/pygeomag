.. image:: https://dl.circleci.com/status-badge/img/circleci/5uMninjUXjCnNMzvVzq9EJ/A7hoBacfgFtGdDUiyiXcBy/tree/main.svg?style=svg&circle-token=13df862914431a3f89a9bc1bcc8bb5b2a177d815
   :target: https://dl.circleci.com/status-badge/redirect/circleci/5uMninjUXjCnNMzvVzq9EJ/A7hoBacfgFtGdDUiyiXcBy/tree/main
   :alt: CircleCI
.. image:: https://codecov.io/gh/boxpet/pygeomag/graph/badge.svg?token=ECHON65OG8
   :target: https://codecov.io/gh/boxpet/pygeomag
   :alt: codecov
.. image:: https://img.shields.io/pypi/v/pygeomag
   :target: https://pypi.org/project/pygeomag/
   :alt: PyPI
.. image:: https://img.shields.io/github/license/boxpet/pygeomag.svg
   :target: https://github.com/boxpet/pygeomag/blob/main/LICENSE
   :alt: License: MIT
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

########
pyGeoMag
########

pyGeoMag is an implementation in Python of the `World Magnetic Model (WMM)
<https://www.ncei.noaa.gov/products/world-magnetic-model>`_.

**From NOAA**

   The World Magnetic Model (WMM) is the standard model for navigation, attitude, and heading referencing systems using
   the geomagnetic field. Additional WMM uses include civilian applications, including navigation and heading systems.

   The model is a joint product of the United States’ National Geospatial-Intelligence Agency (NGA) and the United
   Kingdom’s Defence Geographic Centre (DGC). NCEI and the British Geological Survey (BGS) jointly developed the WMM.
   The U.S. Department of Defense, the U.K. Ministry of Defence, the North Atlantic Treaty Organization (NATO), and the
   International Hydrographic Organization (IHO) use the WMM.

It has been written, specifically to be used on lightweight versions of Python.

************
Installation
************

Install using `pip <http://www.pip-installer.org/en/latest>`_ with:

.. code-block:: shell

   pip install pygeomag

*******
Example
*******

Calculate the geomagnetic declination for the NOAA office in Boulder, CO.

**Input Parameters**

- ``glat`` (Geodetic Latitude): -90.00 to +90.00 degrees (North positive, South negative)
- ``glon`` (Geodetic Longitude): -180.00 to +180.00 degrees (East positive, West negative)
- ``alt`` (Altitude): -1 to 850km referenced to the WGS 84 ellipsoid OR the Mean Sea Level (MSL)
- ``time`` (Time in decimal year): 2020.0 to 2025.0

**Magnetic Components (output)**

- ``result.f`` (``.ti``, ``.total_intensity``): Total Intensity
- ``result.h``: Horizontal Intensity
- ``result.x``: North Component
- ``result.y``: East Component
- ``result.z``:  Vertical Component
- ``result.i`` (``.dip``, ``.inclination``): Geomagnetic Inclination
- ``result.d`` (``.dec``): Geomagnetic Declination (Magnetic Variation)
- ``result.gv``: Magnetic grid variation if the current geodetic position is in the arctic or antarctic

.. code-block:: pycon

   >>> from pygeomag import GeoMag
   >>> geo_mag = GeoMag()
   >>> result = geo_mag.calculate(glat=39.9938, glon=-105.2603, alt=0, time=2023.75)
   >>> print(result.d)
   7.848099459256507

*****
Utils
*****

Date utils
==========

There are methods for converting both a ``time.struct_time``, ``datetime.date`` and ``datetime.datetime`` object to a
decimal year:

.. code-block:: pycon

   >>> import time
   >>> from pygeomag import decimal_year_from_struct_time
   >>> value = time.struct_time((2020, 7, 2, 0, 0, 0, 0, 0, 0))
   >>> decimal_year_from_struct_time(value)
   2020.5

   >>> import datetime
   >>> from pygeomag import decimal_year_from_date
   >>> value = datetime.datetime(2020, 7, 2)
   >>> decimal_year_from_date(value)
   2020.5

If you know using either date format will work in your version of Python, you can
use the wrapper method:

.. code-block:: pycon

   >>> import datetime
   >>> from pygeomag import calculate_decimal_year
   >>> decimal_year_from_date(datetime.datetime(2020, 7, 2))
   2020.5

Formatting utils
================

There are methods from going between decimal degrees and degrees minutes and seconds:

.. code-block:: pycon

   >>> from pygeomag import decimal_degrees_to_degrees_minutes
   >>> decimal_degrees_to_degrees_minutes(45.7625)
   (45, 45.75)

   >>> from pygeomag import decimal_degrees_to_degrees_minutes_seconds
   >>> decimal_degrees_to_degrees_minutes_seconds(45.7625)
   (45, 45, 45.0)

   >>> from pygeomag import degrees_minutes_seconds_to_decimal_degrees
   >>> degrees_minutes_seconds_to_decimal_degrees(45, 45, 45)
   45.7625

   >>> from pygeomag import degrees_minutes_to_decimal_degrees
   >>> degrees_minutes_to_decimal_degrees(45, 45.75)
   45.7625

And also one to take decimal degrees and print it in a more human-readable format:

.. code-block:: pycon

   >>> from pygeomag import pretty_print_degrees
   >>> pretty_print_degrees(value=45.7625, is_latitude=True)
   "45° 46' N"
   >>> pretty_print_degrees(value=45.7625, is_latitude=True, precision=2)
   "45° 45.75' N"
   >>> pretty_print_degrees(value=45.7625, is_latitude=True, verbose=True, precision=2)
   '45 Degrees 45.75 Minutes North'

*******
Testing
*******

This code is 100% tested. All test values from the official NOAA WMM are tested here, as well as additional values to
get to 100% coverage.

************
Contributing
************

Please see `CONTRIBUTING.rst <https://github.com/boxpet/pygeomag/blob/main/CONTRIBUTING.rst>`_.

*****
Notes
*****

This is a direct port from the Legacy C code provided by NOAA. It is using the WMM2020 Coefficient file (WMM.COF) valid
for 2020.0 - 2025.0. The code is specifically not 100% pythonic in order to make adding updates simple (for example
uppercase variable names).

At this point Annual change also known as Secular Variation is not in this package the Legacy C version does a direct
``year+1.value - year2.value`` and both the test values and other existing code bases do something different.
