# Contributing to pygeomag

## Notes

1. This is a direct port from the Legacy C code provided by NOAA.
2. It is using the WMM2020 Coefficient file (WMM.COF) valid
for 2020.0 - 2025.0.
3. The code is specifically not 100% pythonic in order to make adding updates simple (for example
uppercase variable names).
4. It has been written to work in both [MicroPython](https://micropython.org/) and
[CircuitPython](https://circuitpython.org/) and the fact that these do not have the full standard Python library.

## Reporting issues

If you find an issue, catch an exception, or find any other problems, please:

1. Look for or start a [GitHub Discussions](https://github.com/boxpet/pygeomag/discussions).
2. Once a bug has been validated, open a [GitHub Issue](https://github.com/boxpet/pygeomag/issues). Please don't open
one until it's been verified.

## Pull requests

1. Please do not open a [Pull request](https://github.com/boxpet/pygeomag/pulls) without starting a
[GitHub Discussions](https://github.com/boxpet/pygeomag/discussions) first. This repository is actively
being worked on, and do not want to create wasted work
2. Please do not try to make it more pythonic as it's built to match the original C code
3. If you do create a pull request, please make sure that:
   1. All tests pass
      1. `python -m coverage run -m unittest`
   2. Code coverage for the changes is at 100%
      1. `python -m coverage report` or
      2. `python -m coverage html`
   3. You follow the current coding styles
