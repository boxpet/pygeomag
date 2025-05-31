.. _micropython_usage:

Using with MicroPython
========================

`pyGeoMag` has been designed to be compatible with MicroPython, allowing for geomagnetic calculations on microcontroller platforms like the Raspberry Pi Pico (RP2040).

Installation on MicroPython
---------------------------
To use `pyGeoMag` on a MicroPython device, you'll need to transfer the library files to the device's filesystem. Typically, this involves copying the `pygeomag` directory (or at least `pygeomag/geomag.py`, `pygeomag/__init__.py`, and any other necessary modules from `pygeomag`) to your device. Tools like `ampy <https://github.com/adafruit/ampy>`_ or `rshell <https://github.com/dhylands/rshell>`_ can be used for this.

For a minimal setup, you might only need `geomag.py` (renamed to `pygeomag.py` on the device or placed in a `pygeomag` folder) if you are not using other utility functions.

Handling COF Data
-----------------
The most significant change for MicroPython usage is that the library no longer handles file loading directly. Your application is responsible for reading the WMM.COF file content and passing it to the `GeoMag` class.

Example:
~~~~~~~~
Here's how you might load the COF data from a file on your MicroPython device's filesystem (e.g., an SD card or internal flash):

.. code-block:: python

   # main.py on your MicroPython device
   from pygeomag import GeoMag

   COF_FILENAME = "WMM_2025.COF" # Or your chosen WMM file

   try:
       with open(COF_FILENAME, "r") as f:
           cof_data_string = f.read()

       # Initialize GeoMag with the string content
       geo_mag_mp = GeoMag(coefficients_data=cof_data_string)

       # Perform a calculation
       # Make sure to use keyword arguments for clarity and MicroPython compatibility
       result = geo_mag_mp.calculate(glat=47.6205, glon=-122.3493, alt=0.0, time=2025.25)
       print("Declination:", result.d)

   except OSError as e:
       print(f"Failed to load or read {COF_FILENAME}: {e}")
   except ImportError:
       print("Failed to import pygeomag. Ensure library is on device.")


Embedding COF Data (for memory-constrained devices):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If filesystem access is complex or you want to bundle the data, you can embed the COF data as a multi-line string within your Python script. Be mindful that WMM COF files can be several kilobytes, which will increase your script's size and memory footprint.

.. code-block:: python

   from pygeomag import GeoMag

   # Example of embedding COF data string
   # WMM_2020_MINI_DATA = """2020.0 WMM-2020 12/10/2019
   #  1  0  -29438.5    0.0     11.7     0.0
   #  1  1   -1501.1    0.0     -0.1     0.0
   # ... (many more lines of coefficients) ...
   #  12 12    -0.4     0.0      0.0     0.0
   # 9999999999999999999999999999999999999999"""
   # Note: The example above is illustrative. Actual COF data is much longer.
   # The "9999..." line is expected by pygeomag's current parsing logic.

   # geo_mag_embedded = GeoMag(coefficients_data=WMM_2020_MINI_DATA)
   # result = geo_mag_embedded.calculate(glat=0, glon=0, alt=0, time=2022.0)
   # print(result.d)

Performance
-----------
The `calculate` method in `pyGeoMag` is decorated with `@micropython.native`, which can provide a significant speedup on compatible MicroPython ports like the RP2040.

Considerations
--------------
*   **Memory:** Standard WMM.COF files are text and can be moderately large. High-resolution models are significantly larger. Consider if the full precision of the COF file is needed or if it can be truncated for devices with very limited RAM (this would be an advanced modification requiring careful validation).
*   **Floating Point Precision:** MicroPython's floating-point precision (typically 32-bit single precision on many boards) might lead to slight differences compared to CPython (64-bit double precision) results. The HWIL tests account for this with tolerances.
*   **`datetime` module:** The core `pyGeoMag` library avoids direct use of `datetime` for its calculations if you provide time as a decimal year. If you were using the deprecated `base_year` with `datetime` objects, you'd need `micropython-datetime` if that functionality is still desired through the deprecated path.
