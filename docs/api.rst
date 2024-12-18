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

   .. autoattribute:: pygeomag.GeoMagResult.glat
   .. autoattribute:: pygeomag.GeoMagResult.glon
   .. autoattribute:: pygeomag.GeoMagResult.alt
   .. autoattribute:: pygeomag.GeoMagResult.time
   .. autoattribute:: pygeomag.GeoMagResult.f
   .. autoproperty:: pygeomag.GeoMagResult.ti
   .. autoproperty:: pygeomag.GeoMagResult.total_intensity
   .. autoattribute:: pygeomag.GeoMagResult.h
   .. autoattribute:: pygeomag.GeoMagResult.x
   .. autoattribute:: pygeomag.GeoMagResult.y
   .. autoattribute:: pygeomag.GeoMagResult.z
   .. autoattribute:: pygeomag.GeoMagResult.i
   .. autoproperty:: pygeomag.GeoMagResult.dip
   .. autoproperty:: pygeomag.GeoMagResult.inclination
   .. autoattribute:: pygeomag.GeoMagResult.d
   .. autoproperty:: pygeomag.GeoMagResult.dec
   .. autoattribute:: pygeomag.GeoMagResult.gv
   .. autoattribute:: pygeomag.GeoMagResult.in_blackout_zone
   .. autoattribute:: pygeomag.GeoMagResult.in_caution_zone

.. autoclass:: pygeomag.GeoMagUncertaintyResult

   .. autoattribute:: pygeomag.GeoMagUncertaintyResult.f
   .. autoattribute:: pygeomag.GeoMagUncertaintyResult.h
   .. autoattribute:: pygeomag.GeoMagUncertaintyResult.x
   .. autoattribute:: pygeomag.GeoMagUncertaintyResult.y
   .. autoattribute:: pygeomag.GeoMagUncertaintyResult.z
   .. autoattribute:: pygeomag.GeoMagUncertaintyResult.i
   .. autoattribute:: pygeomag.GeoMagUncertaintyResult.d


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
