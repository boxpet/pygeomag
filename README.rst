Welcome to pyGeoMag's documentation!
====================================

.. image:: https://dl.circleci.com/status-badge/img/circleci/5uMninjUXjCnNMzvVzq9EJ/A7hoBacfgFtGdDUiyiXcBy/tree/main.svg?style=svg&circle-token=13df862914431a3f89a9bc1bcc8bb5b2a177d815
   :target: https://dl.circleci.com/status-badge/redirect/circleci/5uMninjUXjCnNMzvVzq9EJ/A7hoBacfgFtGdDUiyiXcBy/tree/main
   :alt: CircleCI
.. image:: https://codecov.io/gh/boxpet/pygeomag/graph/badge.svg?token=ECHON65OG8
   :target: https://codecov.io/gh/boxpet/pygeomag
   :alt: codecov
.. image:: https://img.shields.io/pypi/v/pygeomag
   :target: https://pypi.org/project/pygeomag/
   :alt: PyPI
.. image:: https://readthedocs.org/projects/pygeomag/badge/?version=latest
   :target: https://pygeomag.readthedocs.io/
   :alt: Documentation Status
.. image:: https://img.shields.io/github/license/boxpet/pygeomag.svg
   :target: https://github.com/boxpet/pygeomag/blob/main/LICENSE
   :alt: License: MIT
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Code style: Black

**What is declination?**

Declination is the angle that adjusts a compass reading from Magnetic North to True North. Many
maps will show it in the legend, so you can adjust your compass (either physically or mentally).

**Why do you need this?**

In Washington State, the declination angle is between 14° and 16° West depending on your location. Meaning if I just
pull out my compass and head North, I'm really heading at about 15°. And now if I walk 500 feet on that course, I'll be
about 130 feet to the East of where I wanted to be.

Now say I'm building a device that includes a magnetometer. I get it all calibrated to point to Magnetic North, show
this value on the device and now the user is pointing in the wrong direction. And of course, the values change yearly.
In the last 10 years, it's dropped just over a full degree in the Greater Seattle area. Here is where pyGeoMag comes in.

To help see how much the magnetic field changes as you travel across the globe, here is projection for 2020 from
NOAA:

.. image:: https://www.ncei.noaa.gov/sites/default/files/2022-02/Miller%20Projection%20Main%20Field-%20Annual%20Change%20Declination%20%28D%29.jpg
   :alt: US/UK World Magnetic Model - Epoch 2020.0: Main Field Declination

To see how much the value changes per year (The contour interval is 2 arcminutes/year):

.. image:: https://www.ncei.noaa.gov/sites/default/files/2022-02/Miller%20Projection%20Secular%20Variation-%20Annual%20Change%20Declination%20%28D%29.jpg
   :alt: US/UK World Magnetic Model - Epoch 2020.0: Annual Change Declination

If you want to look up these values, you can use NOAA's
`Magnetic Field Caculators <https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml>`_ in a browser or install their
**CrowdMag** app on your `Android <https://play.google.com/store/apps/details?id=gov.noaa.ngdc.wmm2>`_ or
`iOS <https://itunes.apple.com/app/id910578825>`_ device.

**pyGeoMag** is an implementation written in Python of the
`World Magnetic Model (WMM) <https://www.ncei.noaa.gov/products/world-magnetic-model>`_, specifically to be used in
lightweight versions (like MicroPython and CircuitPython).

**From NOAA**

   The World Magnetic Model (WMM) is the standard model for navigation, attitude, and heading referencing systems using
   the geomagnetic field. Additional WMM uses include civilian applications, including navigation and heading systems.

   The model is a joint product of the United States' National Geospatial-Intelligence Agency (NGA) and the United
   Kingdom's Defence Geographic Centre (DGC). NCEI and the British Geological Survey (BGS) jointly developed the WMM.
   The U.S. Department of Defense, the U.K. Ministry of Defence, the North Atlantic Treaty Organization (NATO), and the
   International Hydrographic Organization (IHO) use the WMM.

Installation
------------

Install using `pip <http://www.pip-installer.org/en/latest>`_ with:

.. code-block:: shell

   pip install pygeomag

Example
-------

Calculate the geomagnetic declination at the Space Needle in Seattle, WA:

.. code-block:: pycon

   >>> from pygeomag import GeoMag
   >>> geo_mag = GeoMag()
   >>> result = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2023.75)
   >>> print(result.d)
   15.25942260585284

And calculate it for the same spot 10 years ago:

.. code-block:: pycon

   >>> from pygeomag import GeoMag
   >>> geo_mag = GeoMag(coefficients_file='wmm/WMM_2010.COF')
   >>> result = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2013.75)
   >>> print(result.d)
   16.32554283003356

Validation
----------

All test values from the official NOAA WMM documentation are tested here for WMM-2020, WMM-2015v2, WMM-2015 and
WMM-2010.

Notes
-----

This is a direct port from the Legacy C code provided by NOAA. It defaults to using the WMM-2020 Coefficient file
(WMM.COF) valid for 2020.0 - 2025.0. The code is specifically not 100% pythonic in order to make adding updates simple
(for example uppercase variable names).

At this point Annual change also known as Secular Variation is not in this package the Legacy C version does a direct
``year+1.value - year2.value`` and both the test values and other existing code bases do something different.

Documentation
-------------

More documentation and examples can be found at `Read the Docs <http://pygeomag.readthedocs.io/>`_.
