.. include:: ../README.rst

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Core
====

.. autoclass:: pygeomag.GeoMag
   :members: calculate

.. autoclass:: pygeomag.GeoMagResult

Time utils
==========

There are methods for converting both a ``time.struct_time``, ``datetime.date`` and ``datetime.datetime`` object to a
decimal year:

.. automodule:: pygeomag.time
   :members:

Formatting utils
================

There are methods from going between decimal degrees and degrees minutes and seconds:

.. automodule:: pygeomag.format
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
