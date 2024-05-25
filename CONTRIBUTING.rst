Contributing to pyGeoMag
========================

Notes
-----

#. This is a direct port from the Legacy C code provided by NOAA.
#. It defaults to using the WMM-2020 Coefficient file (WMM.COF) valid for 2020.0 - 2025.0.
#. The code is specifically not 100% pythonic in order to make adding updates simple (for example uppercase variable
   names).
#. It has been written to work in both `MicroPython <https://micropython.org/>`_ and
   `CircuitPython <https://circuitpython.org/>`_ and the fact that these do not have the full standard Python library.

Reporting issues
----------------

If you find an issue, catch an exception, or find any other problems, please:

#. Look for or start a `GitHub Discussions <https://github.com/boxpet/pygeomag/discussions>`_.
#. Once a bug has been validated, open a `GitHub Issue <https://github.com/boxpet/pygeomag/issues>`_. Please don't open
   one until it's been verified.

Pull requests
-------------

#. Please do not open a `Pull request <https://github.com/boxpet/pygeomag/pulls>`_ without starting a
   `GitHub Discussions <https://github.com/boxpet/pygeomag/discussions>`_ first. This repository is actively being
   worked on, and do not want to create wasted work
#. Please do not try to make it more pythonic as it's built to match the original C code
#. If you do create a pull request, please make sure that:

   #. All tests pass (you will need to run ``pip install -r requirements-test.txt``)

      #. ``pytest --cov --xdoctest``

   #. Code coverage for the changes is at 100%

      #. ``python -m coverage report`` to view in the console or
      #. ``python -m coverage html`` to build out html files to look at what's missing

   #. Documentation builds without errors (you will need to run ``pip install -r docs/requirements.txt``)

      #. ``sphinx-build -W -b html docs/ docs/build/html``

   #. Make sure that the code can be compiles with ``mpy-cross`` (there is a good guide on setting that up
      `here <https://learn.adafruit.com/building-circuitpython/build-circuitpython>`_

   #. Make sure the project builds (you will need to run ``pip install -r requirements-build.txt``)

      #. ``python -m build``

   #. You follow the current coding styles
