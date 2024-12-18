import math
import sys

if not sys.implementation.name == "circuitpython":
    import datetime
    from typing import List, Tuple, Union

WWM_MODEL_2015_LOWER = 2015.0
WWM_MODEL_2015_UPPER = 2020.0
WWM_MODEL_2020_LOWER = 2020.0
WWM_MODEL_2020_UPPER = 2025.0

BLACKOUT_ZONE = 2000
CAUTION_ZONE = 6000


class BlackoutZoneException(Exception):
    """Horizontal intensity is in a Blackout Zone.

    The Blackout Zones are defined as regions around the north and south magnetic poles where the horizontal intensity
    of Earth's magnetic field (H) is less than 2000 nT. In these zones WMM declination values are inaccurate and
    compasses are unreliable.
    """


class CautionZoneException(Exception):
    """Horizontal intensity is in a Caution Zone.

    A Caution Zone is an areas around a Blackout Zone where caution must be exercised while using a compass. It is
    defined where Earth's magnetic field (H) is between 2000 and 6000 nT. Compass accuracy may be degraded in this
    region.
    """


class GeoMagUncertaintyResult:
    """The uncertainty values of a ``GeoMagResult``."""

    def __init__(self, result) -> None:
        self.x: float = None
        """Uncertainty of the North Component in nT."""
        self.y: float = None
        """Uncertainty of the East Component in nT."""
        self.z: float = None
        """Uncertainty of the Vertical Component in nT."""
        self.h: float = None
        """Uncertainty of the Horizontal Intensity in nT."""
        self.f: float = None
        """Uncertainty of the Total Intensity in nT."""
        self.i: float = None
        """Uncertainty of the Geomagnetic Inclination in degrees."""
        self.d: float = None
        """Uncertainty of the Geomagnetic Declination (Magnetic Variation) in degrees."""

        if WWM_MODEL_2020_LOWER <= result.time <= WWM_MODEL_2020_UPPER:
            self._error_model_wmm_2020(result)
        elif WWM_MODEL_2015_LOWER <= result.time < WWM_MODEL_2015_UPPER:
            self._error_model_wmm_2015(result)
        else:
            raise ValueError("GeoMagResult outside of known uncertainty estimates.")

    def _error_model_wmm_2015(self, result) -> None:
        """Calculate uncertainty estimates for 2015.0 to 2020.0."""
        self.x = 138.0
        self.y = 89.0
        self.z = 165.0
        self.h = 133.0
        self.f = 152.0
        self.i = 0.22
        self.d = math.sqrt(0.23**2 + (5430 / result.h) ** 2)

    def _error_model_wmm_2020(self, result) -> None:
        """Calculate uncertainty estimates for 2020.0 to 2025.0."""
        self.x = 131.0
        self.y = 94.0
        self.z = 157.0
        self.h = 128.0
        self.f = 148.0
        self.i = 0.21
        self.d = math.sqrt(0.26**2 + (5625 / result.h) ** 2)


class GeoMagResult:
    """The Magnetic Components values from ``GeoMag.calculate()``."""

    def __init__(self, time: float, alt: float, glat: float, glon: float) -> None:
        self.time: float = time
        """Time (in decimal year)."""
        self.alt: float = alt
        """Altitude, -1 to 850km referenced to the WGS 84 ellipsoid OR the Mean Sea Level (MSL)."""
        self.glat: float = glat
        """Geodetic Latitude, -90.00 to +90.00 degrees (North positive, South negative)."""
        self.glon: float = glon
        """Geodetic Longitude, -180.00 to +180.00 degrees (East positive, West negative)."""
        self.x: float = None
        """North Component."""
        self.y: float = None
        """East Component."""
        self.z: float = None
        """Vertical Component."""
        self.h: float = None
        """Horizontal Intensity."""
        self.f: float = None
        """Total Intensity."""
        self.i: float = None
        """Geomagnetic Inclination."""
        self.d: float = None
        """Geomagnetic Declination (Magnetic Variation)."""
        self.gv: float = None
        """Magnetic grid variation if the current geodetic position is in the arctic or antarctic."""
        self.in_blackout_zone: bool = False
        """Horizontal intensity is in a Blackout Zone."""
        self.in_caution_zone: bool = False
        """Horizontal intensity is in a Caution Zone."""

    @property
    def dec(self) -> float:
        """Geomagnetic Declination (Magnetic Variation)."""
        return self.d

    @property
    def dip(self) -> float:
        """Geomagnetic Inclination."""
        return self.i

    @property
    def inclination(self) -> float:
        """Geomagnetic Inclination."""
        return self.i

    @property
    def ti(self) -> float:
        """Total Intensity."""
        return self.f

    @property
    def total_intensity(self) -> float:
        """Total Intensity."""
        return self.f

    def calculate(self, raise_in_warning_zone: bool) -> None:
        """Calculate extra result values."""
        # COMPUTE X, Y, Z, AND H COMPONENTS OF THE MAGNETIC FIELD
        self.x = self.f * (
            math.cos(math.radians(self.d)) * math.cos(math.radians(self.i))
        )
        self.y = self.f * (
            math.cos(math.radians(self.i)) * math.sin(math.radians(self.d))
        )
        self.z = self.f * (math.sin(math.radians(self.i)))
        self.h = self.f * (math.cos(math.radians(self.i)))

        # Check if in Caution or Blackout Zones
        if self.h < BLACKOUT_ZONE:
            if raise_in_warning_zone:
                raise BlackoutZoneException(
                    f"The horizontal field strength at this location is {self.h:.1f}. Compass readings have VERY LARGE "
                    "uncertainties in areas where H smaller than 2000 nT"
                )
            self.in_blackout_zone = True

        elif self.h < CAUTION_ZONE:
            if raise_in_warning_zone:
                raise CautionZoneException(
                    f"The horizontal field strength at this location is {self.h:.1f}. Compass readings have large "
                    "uncertainties in areas where H smaller than 6000 nT"
                )
            self.in_caution_zone = True

    def calculate_uncertainty(self) -> GeoMagUncertaintyResult:
        """Calculate the uncertainty values for this ``GeoMagResult``.

        Uncertainty estimates provided by the **WMM2015** and **WMM2020** error model for the various field components.
        H is expressed in nT in the formula providing the error in D.

        These values can currently only be computed for ``GeoMagResult`` between 2015.0 and 2025.0 and using a value
        outside this will raise an Exception

        :return: A GeoMagUncertaintyResult object

        >>> from pygeomag import GeoMag
        >>> geo_mag = GeoMag(coefficients_file="wmm/WMM_2020.COF")
        >>> result = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2023.75)
        >>> uncertainty = result.calculate_uncertainty()
        >>> print(uncertainty.d)
        0.3935273117953904
        """
        return GeoMagUncertaintyResult(self)


class GeoMag:
    """Python port of the Legacy C code provided by NOAA for the World Magnetic Model (WMM).

    It defaults to using the WMM-2020 Coefficient file (WMM.COF) valid for 2020.0 - 2025.0.

    Included are the following coefficient files, if you have the need to calculate past values:

    .. table::
       :widths: auto

       ==============  ==========  ===============  ==========
       File            Model       Life Span        Creation
       ==============  ==========  ===============  ==========
       WMM.COF         WMM-2025    2025.0 - 2030.0  11/13/2024
       WMM_2025.COF    WMM-2025    2025.0 - 2030.0  11/13/2024
       WMM_2020.COF    WMM-2020    2020.0 - 2025.0  12/10/2019
       WMM_2015v2.COF  WMM-2015v2  2015.0 - 2020.0  09/18/2018
       WMM_2015.COF    WMM-2015    2015.0 - 2020.0  12/15/2014
       WMM_2010.COF    WMM-2010    2010.0 - 2015.0  11/20/2009
       ==============  ==========  ===============  ==========
    """

    def __init__(
        self,
        coefficients_file: str = None,
        coefficients_data: Tuple = None,
    ) -> None:
        """Create a GeoMag instance.

        Leaving both values as ``None`` will load the packages default coefficients file, supplying both will raise.

        :param str coefficients_file: Full or relative path to a coefficients file supplied by this package or WMM
        :param str coefficients_data: coefficients data from a python module
        """
        if coefficients_file is not None and coefficients_data is not None:
            raise ValueError(
                "Both coefficients_file and coefficients_data supplied, supply none or only one."
            )

        self._coefficients_data = coefficients_data
        self._coefficients_file = coefficients_file
        self._maxord = 12
        self._epoch = None
        self._model = None
        self._release_date = None
        self._c = None
        self._cd = None
        self._p = None
        self._fn = None
        self._fm = None
        self._k = None

    @property
    def life_span(self) -> Tuple[float, float]:
        """Return the life span for the selected coefficient file."""
        if self._epoch is None:
            self._load_coefficients()

        return self._epoch, self._epoch + 5

    @property
    def model(self) -> str:
        """Return the model name for the selected coefficient file."""
        if self._epoch is None:
            self._load_coefficients()

        return self._model

    @property
    def release_date(self) -> str:
        """Return the release date for the selected coefficient file."""
        if self._epoch is None:
            self._load_coefficients()

        return self._release_date

    @classmethod
    def _create_list(cls, length: int, default=None) -> List:
        """Create a list of length with an optional default."""
        return [default] * length

    @classmethod
    def _create_matrix(cls, rows: int, columns: int, default=None) -> List:
        """Create a 2 dimensional matrix of length with an optional default."""
        return [[default for _ in range(columns)] for _ in range(rows)]

    def _get_model_filename(self) -> str:
        """Determine the model filename to load the coefficients from."""
        # some lightweight versions of Python won't have access to methods like "os.path.dirname"
        if self._coefficients_file and self._coefficients_file[0] in "\\/":
            return self._coefficients_file

        filepath = __file__
        sep = "/" if "/" in filepath else "\\"
        filename = filepath.split(sep)[-1]

        if self._coefficients_file:
            return filepath.replace(filename, self._coefficients_file)

        coefficients_file = f"wmm{sep}WMM.COF"
        wmm_filepath = filepath.replace(filename, coefficients_file)
        try:
            with open(wmm_filepath):
                self._coefficients_file = wmm_filepath
                return wmm_filepath
        except OSError:
            """File not found, try in same directory"""

        coefficients_file = "WMM.COF"
        wmm_filepath_2 = filepath.replace(filename, coefficients_file)
        try:
            with open(wmm_filepath_2):
                self._coefficients_file = wmm_filepath_2
                return wmm_filepath_2
        except OSError:
            return wmm_filepath

    def _load_coefficients(self) -> None:  # noqa: PLR0915 - Too many statements
        """Load the coefficients model to calculate the Magnetic Components from."""
        if self._epoch is not None:
            return

        c = self._create_matrix(13, 13)
        cd = self._create_matrix(13, 13)
        snorm = self._create_list(169)
        fn = self._create_list(13)
        fm = self._create_list(13)
        k = self._create_matrix(13, 13)

        if self._coefficients_data:
            (epoch, model, release_date), coefficients = self._coefficients_data
        else:
            (epoch, model, release_date), coefficients = (
                self._read_coefficients_data_from_file()
            )

        # READ WORLD MAGNETIC MODEL SPHERICAL HARMONIC COEFFICIENTS
        c[0][0] = 0.0
        cd[0][0] = 0.0

        for n, m, gnm, hnm, dgnm, dhnm in coefficients:
            if m > self._maxord:
                break
            if m > n or m < 0:
                raise ValueError("Corrupt record in model file")
            if m <= n:
                c[m][n] = gnm
                cd[m][n] = dgnm
                if m != 0:
                    c[n][m - 1] = hnm
                    cd[n][m - 1] = dhnm

        # CONVERT SCHMIDT NORMALIZED GAUSS COEFFICIENTS TO UNNORMALIZED
        snorm[0] = 1.0
        fm[0] = 0.0
        for n in range(1, self._maxord + 1):
            snorm[n] = snorm[n - 1] * float(2 * n - 1) / float(n)
            j = 2
            m = 0
            D1 = 1
            D2 = (n - m + D1) / D1
            while D2 > 0:
                k[m][n] = float(((n - 1) * (n - 1)) - (m * m)) / float(
                    (2 * n - 1) * (2 * n - 3)
                )
                if m > 0:
                    flnmj = float((n - m + 1) * j) / float(n + m)
                    snorm[n + m * 13] = snorm[n + (m - 1) * 13] * math.sqrt(flnmj)
                    j = 1
                    c[n][m - 1] = snorm[n + m * 13] * c[n][m - 1]
                    cd[n][m - 1] = snorm[n + m * 13] * cd[n][m - 1]
                c[m][n] = snorm[n + m * 13] * c[m][n]
                cd[m][n] = snorm[n + m * 13] * cd[m][n]
                D2 -= 1
                m += D1
            fn[n] = float(n + 1)
            fm[n] = float(n)
        k[1][1] = 0.0

        self._epoch = epoch
        self._model = model
        self._release_date = release_date
        self._c = c
        self._cd = cd
        self._p = snorm
        self._fn = fn
        self._fm = fm
        self._k = k

    def _read_coefficients_data_from_file(self) -> Tuple[Tuple[str, str, str], list]:
        """Read coefficients data from file to be processed by ``_load_coefficients``."""
        data = []

        model_filename = self._get_model_filename()

        with open(model_filename) as coefficients_file:
            # READ WORLD MAGNETIC MODEL SPHERICAL HARMONIC COEFFICIENTS
            line_data = coefficients_file.readline()
            line_values = line_data.split()
            if len(line_values) != 3:  # noqa: PLR2004 Magic value used in comparison
                raise ValueError("Invalid header in model file")
            epoch, model, release_date = (
                t(s) for t, s in zip((float, str, str), line_values)
            )

            while True:
                line_data = coefficients_file.readline()

                # CHECK FOR LAST LINE IN FILE
                if line_data[:4] == "9999":
                    break

                # END OF FILE NOT ENCOUNTERED, GET VALUES
                line_values = line_data.split()
                if len(line_values) != 6:  # noqa: PLR2004 Magic value used in comparison
                    raise ValueError("Corrupt record in model file")
                n, m, gnm, hnm, dgnm, dhnm = (
                    t(s)
                    for t, s in zip((int, int, float, float, float, float), line_values)
                )

                data.append((n, m, gnm, hnm, dgnm, dhnm))

        return (epoch, model, release_date), data

    def calculate(  # noqa: PLR0912,PLR0913,PLR0915 - Too many branches,Too many arguments,Too many statements
        self,
        glat: float,
        glon: float,
        alt: float,
        time: float,
        allow_date_outside_lifespan: bool = False,
        raise_in_warning_zone: bool = False,
    ) -> GeoMagResult:
        """Calculate the Magnetic Components from a latitude, longitude, altitude and date.

        :param float glat: Geodetic Latitude, -90.00 to +90.00 degrees (North positive, South negative)
        :param float glon: Geodetic Longitude, -180.00 to +180.00 degrees (East positive, West negative)
        :param float alt: Altitude, -1 to 850km referenced to the WGS 84 ellipsoid OR the Mean Sea Level (MSL)
        :param float time: Time (in decimal year)
        :param bool allow_date_outside_lifespan: True, if you want an estimation outside the 5-year life span
        :param bool raise_in_warning_zone: True if you want to raise a BlackoutZoneException or CautionZoneException
            exception when the horizontal intensity is < 6000
        :return: A GeoMagResult object

        Calculate the geomagnetic declination at the Space Needle in Seattle, WA:

        >>> from pygeomag import GeoMag
        >>> geo_mag = GeoMag(coefficients_file="wmm/WMM_2025.COF")
        >>> result = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2025.25)
        >>> print(result.d)
        15.065629638512593

        And calculate it for the same spot 12 years previous:

        >>> from pygeomag import GeoMag
        >>> geo_mag = GeoMag(coefficients_file='wmm/WMM_2010.COF')
        >>> result = geo_mag.calculate(glat=47.6205, glon=-122.3493, alt=0, time=2013.25)
        >>> print(result.d)
        16.415602225952366
        """
        tc = self._create_matrix(13, 13)
        dp = self._create_matrix(13, 13)
        sp = self._create_list(13)
        cp = self._create_list(13)
        pp = self._create_list(13)

        # INITIALIZE CONSTANTS
        sp[0] = 0.0
        cp[0] = pp[0] = 1.0
        dp[0][0] = 0.0
        a = 6378.137
        b = 6356.7523142
        re = 6371.2
        a2 = a * a
        b2 = b * b
        c2 = a2 - b2
        a4 = a2 * a2
        b4 = b2 * b2
        c4 = a4 - b4

        self._load_coefficients()

        # TODO #1: Legacy C code static vars for speed
        #  Decide to either:
        #   1. Pull out the tracking of previous values
        #        which are in the legacy c app for speeding it up for getting the Secular Change
        #   2. Remove them
        # otime = oalt = olat = olon = -1000.0

        dt = time - self._epoch
        # TODO #1: Legacy C code static vars for speed
        # if otime < 0.0 and (dt < 0.0 or dt > 5.0) and not allow_date_past_lifespan:
        if True and (dt < 0.0 or dt > 5.0) and not allow_date_outside_lifespan:  # noqa: PLR2004 Magic value used in comparison
            raise ValueError("Time extends beyond model 5-year life span")

        rlon = math.radians(glon)
        rlat = math.radians(glat)
        srlon = math.sin(rlon)
        srlat = math.sin(rlat)
        crlon = math.cos(rlon)
        crlat = math.cos(rlat)
        srlat2 = srlat * srlat
        crlat2 = crlat * crlat
        sp[1] = srlon
        cp[1] = crlon

        # CONVERT FROM GEODETIC COORDINATES TO SPHERICAL COORDINATES
        # TODO #1: Legacy C code static vars for speed
        # if alt != oalt or glat != olat:
        if True:
            q = math.sqrt(a2 - c2 * srlat2)
            q1 = alt * q
            q2 = ((q1 + a2) / (q1 + b2)) * ((q1 + a2) / (q1 + b2))
            ct = srlat / math.sqrt(q2 * crlat2 + srlat2)
            st = math.sqrt(1.0 - (ct * ct))
            r2 = (alt * alt) + 2.0 * q1 + (a4 - c4 * srlat2) / (q * q)
            r = math.sqrt(r2)
            d = math.sqrt(a2 * crlat2 + b2 * srlat2)
            ca = (alt + d) / r
            sa = c2 * crlat * srlat / (r * d)
        # TODO #1: Legacy C code static vars for speed
        # if glon != olon:
        if True:
            for m in range(2, self._maxord + 1):
                sp[m] = sp[1] * cp[m - 1] + cp[1] * sp[m - 1]
                cp[m] = cp[1] * cp[m - 1] - sp[1] * sp[m - 1]
        aor = re / r
        ar = aor * aor
        br = bt = bp = bpp = 0.0
        for n in range(1, self._maxord + 1):
            ar = ar * aor
            m = 0
            D3 = 1
            D4 = (n + m + D3) / D3
            while D4 > 0:
                # COMPUTE UNNORMALIZED ASSOCIATED LEGENDRE POLYNOMIALS
                # AND DERIVATIVES VIA RECURSION RELATIONS
                # TODO #1: Legacy C code static vars for speed
                # if alt != oalt or glat != olat:
                if True:
                    if n == m:
                        self._p[n + m * 13] = st * self._p[n - 1 + (m - 1) * 13]
                        dp[m][n] = (
                            st * dp[m - 1][n - 1] + ct * self._p[n - 1 + (m - 1) * 13]
                        )
                    elif n == 1 and m == 0:
                        self._p[n + m * 13] = ct * self._p[n - 1 + m * 13]
                        dp[m][n] = ct * dp[m][n - 1] - st * self._p[n - 1 + m * 13]
                    elif n > 1 and n != m:
                        if m > n - 2:
                            self._p[n - 2 + m * 13] = 0.0
                        if m > n - 2:
                            dp[m][n - 2] = 0.0
                        self._p[n + m * 13] = (
                            ct * self._p[n - 1 + m * 13]
                            - self._k[m][n] * self._p[n - 2 + m * 13]
                        )
                        dp[m][n] = (
                            ct * dp[m][n - 1]
                            - st * self._p[n - 1 + m * 13]
                            - self._k[m][n] * dp[m][n - 2]
                        )

                # TIME ADJUST THE GAUSS COEFFICIENTS
                # TODO #1: Legacy C code static vars for speed
                # if time != otime:
                if True:
                    tc[m][n] = self._c[m][n] + dt * self._cd[m][n]
                    if m != 0:
                        tc[n][m - 1] = self._c[n][m - 1] + dt * self._cd[n][m - 1]

                # ACCUMULATE TERMS OF THE SPHERICAL HARMONIC EXPANSIONS
                par = ar * self._p[n + m * 13]
                if m == 0:
                    temp1 = tc[m][n] * cp[m]
                    temp2 = tc[m][n] * sp[m]
                else:
                    temp1 = tc[m][n] * cp[m] + tc[n][m - 1] * sp[m]
                    temp2 = tc[m][n] * sp[m] - tc[n][m - 1] * cp[m]
                bt = bt - ar * temp1 * dp[m][n]
                bp += self._fm[m] * temp2 * par
                br += self._fn[n] * temp1 * par

                # SPECIAL CASE:  NORTH/SOUTH GEOGRAPHIC POLES
                if st == 0.0 and m == 1:
                    if n == 1:
                        pp[n] = pp[n - 1]
                    else:
                        pp[n] = ct * pp[n - 1] - self._k[m][n] * pp[n - 2]
                    parp = ar * pp[n]
                    bpp += self._fm[m] * temp2 * parp

                D4 -= 1
                m += D3

        if st == 0.0:
            bp = bpp
        else:
            bp /= st

        # ROTATE MAGNETIC VECTOR COMPONENTS FROM SPHERICAL TO
        # GEODETIC COORDINATES
        bx = -bt * ca - br * sa
        by = bp
        bz = bt * sa - br * ca

        result = GeoMagResult(time, alt, glat, glon)

        # COMPUTE DECLINATION (DEC), INCLINATION (DIP) AND
        # TOTAL INTENSITY (TI)
        bh = math.sqrt((bx * bx) + (by * by))
        result.f = math.sqrt((bh * bh) + (bz * bz))
        result.d = math.degrees(math.atan2(by, bx))
        result.i = math.degrees(math.atan2(bz, bh))

        # COMPUTE MAGNETIC GRID VARIATION IF THE CURRENT
        # GEODETIC POSITION IS IN THE ARCTIC OR ANTARCTIC
        # (I.E. GLAT > +55 DEGREES OR GLAT < -55 DEGREES)
        #
        # OTHERWISE, SET MAGNETIC GRID VARIATION TO -999.0
        result.gv = gv_default = -999.0
        if math.fabs(glat) >= 55.0:  # noqa: PLR2004 Magic value used in comparison
            if glat > 0.0 and glon >= 0.0:
                result.gv = result.d - glon
            if glat > 0.0 and glon < 0.0:
                result.gv = result.d + math.fabs(glon)
            if glat < 0.0 and glon >= 0.0:
                result.gv = result.d + glon
            if glat < 0.0 and glon < 0.0:
                result.gv = result.d - math.fabs(glon)
            if result.gv > +180.0:  # noqa: PLR2004 Magic value used in comparison
                result.gv -= 360.0
            if result.gv < -180.0:  # noqa: PLR2004 Magic value used in comparison
                result.gv += 360.0
        if result.gv == gv_default:
            result.gv = None

        result.calculate(raise_in_warning_zone)

        # TODO #1: Legacy C code static vars for speed
        # otime = time
        # oalt = alt
        # olat = glat
        # olon = glon

        return result
