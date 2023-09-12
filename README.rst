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

Installation
------------

Install using `pip <http://www.pip-installer.org/en/latest>`_ with:

.. code-block:: shell

   pip install pygeomag

Example
-------

Calculate the geomagnetic declination for the NOAA office in Boulder, CO.

.. code-block:: pycon

   >>> from pygeomag import GeoMag
   >>> geo_mag = GeoMag()
   >>> result = geo_mag.calculate(glat=39.9938, glon=-105.2603, alt=0, time=2023.75)
   >>> print(result.d)
   7.85173924057477

Testing
-------

This code is 100% tested. All test values from the official NOAA WMM are tested here, as well as additional values to
get to 100% coverage.

Contributing
------------

Please see `CONTRIBUTING.rst <https://github.com/boxpet/pygeomag/blob/main/CONTRIBUTING.rst>`_.

Notes
-----

This is a direct port from the Legacy C code provided by NOAA. It is using the WMM2020 Coefficient file (WMM.COF) valid
for 2020.0 - 2025.0. The code is specifically not 100% pythonic in order to make adding updates simple (for example
uppercase variable names).

At this point Annual change also known as Secular Variation is not in this package the Legacy C version does a direct
``year+1.value - year2.value`` and both the test values and other existing code bases do something different.

Documentation
-------------

More documentation and examples can be found at `Read the Docs <http://pygeomag.readthedocs.io/>`_.
