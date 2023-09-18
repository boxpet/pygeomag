API
===

GeoMag
------

.. autoexception:: pygeomag.BlackoutZoneException

.. autoexception:: pygeomag.CautionZoneException

.. autoclass:: pygeomag.GeoMag
   :members:

   .. automethod:: __init__

.. autoclass:: pygeomag.GeoMagResult
   :members: calculate_uncertainty

.. autoclass:: pygeomag.GeoMagUncertaintyResult

Time utils
----------

There are methods for converting both a ``time.struct_time``, ``datetime.date`` and ``datetime.datetime`` object to a
decimal year:

.. automodule:: pygeomag.time
   :members:

Formatting utils
----------------

There are methods from going between decimal degrees and degrees minutes and seconds:

.. automodule:: pygeomag.format
   :members:
