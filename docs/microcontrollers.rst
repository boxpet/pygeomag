Microcontroller Usage
=====================

CircuitPython
-------------

There are two downloads from the release:

#. **boxpet_geomag**: which will contain the library and the current coefficient file.

   - ``boxpet_geomag/geomag.mpy``
   - ``boxpet_geomag/wmm_2020.mpy``

#. **boxpet_geomag_full**: which will contain the above and the previous coefficient files (move compiled and text).

You will need to copy the ``boxpet_geomag`` folder to your board's lib folder or root filesystem.

Using the compiled version (``.mpy``) of the coefficients will take slightly smaller amount of space and be considerably
faster.

.. code-block:: pycon

   >>> from boxpet_geomag.geomag import GeoMag
   >>> from boxpet_geomag.wmm_2020 import WMM_2020
   >>> geo_mag = GeoMag(coefficients_data=WMM_2020)
   >>> result = geo_mag.calculate(glat=39.9938, glon=-105.2603, alt=0, time=2023.75)
   >>> print(result.d)
   7.85171

If you are wanting to find values in the past, you can copy additional coefficient files:

.. table::
   :widths: auto

   ==============  ==========  ===============  ==========
   File            Model       Date Range       Creation
   ==============  ==========  ===============  ==========
   wmm_2020.mpy    WMM-2020    2020.0 - 2025.0  12/10/2019
   wmm_2015v2.mpy  WMM-2015v2  2015.0 - 2020.0  09/18/2018
   wmm_2015.mpy    WMM-2015    2015.0 - 2020.0  12/15/2014
   wmm_2010.mpy    WMM-2010    2010.0 - 2015.0  11/20/2009
   ==============  ==========  ===============  ==========

CircuitPython floating point numbers are different then Python (see note below). But since this library would likely be
used to point a person or device in a general direction (not pin point accuracy), this shouldn't cause any issues.

.. note::
   From the `CircuitPython <https://learn.adafruit.com/circuitpython-essentials/circuitpython-expectations>`_ docs:

   **Floating Point Numbers and Digits of Precision for Floats in CircuitPython**

   Floating point numbers are single precision in CircuitPython (not double precision as in Python). The largest
   floating point magnitude that can be represented is about +/-3.4e38. The smallest magnitude that can be represented
   with full accuracy is about +/-1.7e-38, though numbers as small as +/-5.6e-45 can be represented with reduced
   accuracy.

   CircuitPython's floats have 8 bits of exponent and 22 bits of mantissa (not 24 like regular single precision floating
   point), which is about five or six decimal digits of precision.
