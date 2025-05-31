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
.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff


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

.. image:: https://www.ncei.noaa.gov/sites/g/files/anmtlf171/files/inline-images/D.jpg
   :alt: US/UK World Magnetic Model - Epoch 2025.0: Main Field Declination (D)

To see how much the value changes per year (The contour interval is 2 arcminutes/year):

.. image:: https://www.ncei.noaa.gov/sites/g/files/anmtlf171/files/inline-images/D_SV.jpg
   :alt: US/UK World Magnetic Model - Epoch 2025.0: Annual Change Declination (D)

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

High Resolution
---------------

Starting in 2025, a high resolution model was released you can read more about it here:
`World Magnetic Model High Resolution (WMMHR) <https://www.ncei.noaa.gov/products/world-magnetic-model-high-resolution>`_

**From NOAA**

    The World Magnetic Model High Resolution (WMMHR) is an advanced geomagnetic field model that provides a more detailed,
    accurate depiction of the geomagnetic field than the World Magnetic Model (WMM). WMMHR2025 includes core field and
    secular variation coefficients for degrees n = 1 to 15. This model also covers the crustal field (from n=16 through
    n=133).  As a result, it has more coefficients ((18,210 non-zero coefficients instead of 336) and more digits (4 instead
    of 1) in each coefficient.

Installation
------------

Install using `pip <http://www.pip-installer.org/en/latest>`_ with:

.. code-block:: shell

   pip install pygeomag

Example
-------

The primary way to initialize `GeoMag` is by providing the WMM.COF file content as a string. Your application is responsible for reading this data from a file.

Calculate the geomagnetic declination at the Space Needle in Seattle, WA using WMM-2025:

.. code-block:: python

   from pygeomag import GeoMag
   import os # For path joining

   # Construct path relative to the script or package
   # For example, if your script is outside the pygeomag package
   # and pygeomag is installed, you might need to locate package data.
   # For this example, let's assume 'pygeomag/wmm/WMM_2025.COF' is accessible.
   # A more robust way for installed packages is to use importlib.resources (Python 3.7+)

   cof_file_path = os.path.join(os.path.dirname(__file__), "pygeomag", "wmm", "WMM_2025.COF")
   # If running from top level of repo, path might be "pygeomag/wmm/WMM_2025.COF"
   # For an installed package, you'd use a helper or hardcode relative path if known
   # For simplicity, we'll assume a known path for this example.
   # Replace with actual path to your COF file.
   try:
       # Path for running example from outside pygeomag directory, assuming pygeomag is a subdir
       # For actual use within a project, manage paths appropriately.
       # This example assumes a specific structure which might not hold for all users.
       # A better approach for finding package data is `importlib.resources`.
       module_dir = os.path.dirname(pygeomag.__file__) # Gets /path/to/.../pygeomag
       cof_file_path = os.path.join(module_dir, "wmm", "WMM_2025.COF")

       with open(cof_file_path, "r") as f:
           cof_data_string = f.read()

       geo_mag = GeoMag(coefficients_data=cof_data_string)
       result = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2025.25)
       print(f"Declination (WMM-2025): {result.d}")

       # For a high-resolution model (e.g., WMMHR_2025.COF)
       hr_cof_file_path = os.path.join(module_dir, "wmm", "WMMHR_2025.COF")
       with open(hr_cof_file_path, "r") as f:
           hr_cof_data_string = f.read()

       geo_mag_hr = GeoMag(coefficients_data=hr_cof_data_string, high_resolution=True)
       result_hr = geo_mag_hr.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2025.00)
       print(f"Declination (WMMHR-2025): {result_hr.d}")

   except FileNotFoundError:
       print("Error: WMM.COF file not found. Adjust path if necessary.")
   except ImportError: # pygeomag might not be in path if running standalone
        print("Error: pygeomag module not found. Ensure it's installed or in PYTHONPATH.")


.. note::
   The parameters `coefficients_file` and `base_year` for `GeoMag.__init__` are deprecated.
   Applications should manage file I/O and pass the COF data as a string to `coefficients_data`.

Validation
----------

All test values from the official NOAA WMM documentation are tested here for WMM-2025, WMMHR-2025, WMM-2020, WMM-2015v2,
WMM-2015 and WMM-2010.

For the WMM-2025 and WMMHR-2025 the test data went from 1 decmial place to 6 for x, y, z, h and f. The code copied from the
legacy C application uses a different formula and thus isn't quite the same. I am looking at the newer code to see if it
makes sense to re-port over.

Notes
-----

This is a direct port from the Legacy C code provided by NOAA. It defaults to using the WMM-2025 Coefficient file
(WMM.COF) valid for 2025.0 - 2030.0. The code is specifically not 100% pythonic in order to make adding updates simple
(for example uppercase variable names).

At this point Annual change also known as Secular Variation is not in this package the Legacy C version does a direct
``year+1.value - year2.value`` and both the test values and other existing code bases do something different.

Documentation
-------------

More documentation and examples can be found at `Read the Docs <http://pygeomag.readthedocs.io/>`_.

Using with MicroPython
----------------------

`pyGeoMag` is designed for compatibility with MicroPython, enabling geomagnetic calculations on platforms like the Raspberry Pi Pico (RP2040).

**Installation:**
Copy the `pygeomag` library (or minimally `pygeomag/geomag.py` and `pygeomag/__init__.py`) to your MicroPython board's filesystem. Tools like `ampy` or `rshell` can assist with this.

**Example (MicroPython):**

.. code-block:: python

   # On MicroPython device (e.g., Raspberry Pi Pico)
   # Assuming WMM_2025.COF content is in a file named 'WMM_2025.COF' in the root
   try:
       with open('WMM_2025.COF', 'r') as f:
           cof_content = f.read()

       from pygeomag import GeoMag

       geo_mag = GeoMag(coefficients_data=cof_content)
       # Example calculation
       # result = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2025.25)
       # print(result.d)

   except OSError as e:
       print("Error opening or reading COF file:", e)
   except ImportError:
       print("Error: pygeomag library not found.")

   # Alternatively, for memory-constrained devices, COF data can be embedded
   # as a large string directly in the script, though this increases .py file size.
   # WMM_2025_DATA = """
   # 2025.0 WMM-2025 11/13/2024
   #  1  0  -29404.5    0.0     10.3     0.0
   # ... (many more lines of coefficients) ...
   # 9999999999999999999999999999999999999999
   # """ # Ensure the '9999...' line is present if using full file content.
   # geo_mag_embedded = GeoMag(coefficients_data=WMM_2025_DATA)

**Performance:**
The `calculate` method in `pyGeoMag` includes optimizations like `@micropython.native`, which can enhance performance on compatible MicroPython boards (e.g., RP2040).
