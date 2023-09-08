import math


class GeoMagResult:
    """The result values from 'GeoMag.calculate()'."""

    def __init__(self, time, alt, glat, glon):
        self.time = time
        self.alt = alt
        self.glat = glat
        self.glon = glon
        self.x = None
        self.y = None
        self.z = None
        self.h = None
        self.f = None
        self.i = None
        self.d = None
        self.gv = None

    @property
    def dec(self):
        """Additional name for variable d."""
        return self.d

    @property
    def dip(self):
        """Additional name for variable i."""
        return self.i

    @property
    def inclination(self):
        """Additional name for variable i."""
        return self.i

    @property
    def ti(self):
        """Additional name for variable f."""
        return self.f

    @property
    def total_intensity(self):
        """Additional name for variable f."""
        return self.f

    def compute(self):
        """Calculate extra result values."""
        # COMPUTE X, Y, Z, AND H COMPONENTS OF THE MAGNETIC FIELD
        self.x = self.f * (math.cos(math.radians(self.d)) * math.cos(math.radians(self.i)))
        self.y = self.f * (math.cos(math.radians(self.i)) * math.sin(math.radians(self.d)))
        self.z = self.f * (math.sin(math.radians(self.i)))
        self.h = self.f * (math.cos(math.radians(self.i)))


class GeoMag:
    """Python port of the Legacy C code provided by NOAA for the World Magnetic Model (WMM)."""

    def __init__(self, maxord=12, coefficients_file=None):
        self.maxord = maxord
        self.coefficients_file = coefficients_file

        self.epoch = None
        self.c = None
        self.cd = None
        self.p = None
        self.fn = None
        self.fm = None
        self.k = None

    def calculate(self, glat, glon, alt, time, allow_date_past_lifespan=False):
        """Calculate the Magnetic Components from a latitude, longitude, altitude and date."""
        tc = self.create_matrix(13, 13)
        dp = self.create_matrix(13, 13)
        sp = self.create_list(13)
        cp = self.create_list(13)
        pp = self.create_list(13)

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

        self.load_coefficients()

        # TODO #1: Legacy C code static vars for speed
        #  Decide to either:
        #   1. Pull out the tracking of previous values
        #        which are in the legacy c app for speeding it up for getting the Secular Change
        #   2. Remove them
        # otime = oalt = olat = olon = -1000.0

        dt = time - self.epoch
        # TODO #1: Legacy C code static vars for speed
        # if otime < 0.0 and (dt < 0.0 or dt > 5.0) and not allow_date_past_lifespan:
        if True and (dt < 0.0 or dt > 5.0) and not allow_date_past_lifespan:
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
            for m in range(2, self.maxord + 1):
                sp[m] = sp[1] * cp[m - 1] + cp[1] * sp[m - 1]
                cp[m] = cp[1] * cp[m - 1] - sp[1] * sp[m - 1]
        aor = re / r
        ar = aor * aor
        br = bt = bp = bpp = 0.0
        for n in range(1, self.maxord + 1):
            ar = ar * aor
            m = 0
            D3 = 1  # noqa pyCharm: Variable in function should be lowercase
            D4 = (n + m + D3) / D3  # noqa pyCharm: Variable in function should be lowercase
            while D4 > 0:
                # COMPUTE UNNORMALIZED ASSOCIATED LEGENDRE POLYNOMIALS
                # AND DERIVATIVES VIA RECURSION RELATIONS
                # TODO #1: Legacy C code static vars for speed
                # if alt != oalt or glat != olat:
                if True:
                    if n == m:
                        self.p[n + m * 13] = st * self.p[n - 1 + (m - 1) * 13]
                        dp[m][n] = st * dp[m - 1][n - 1] + ct * self.p[n - 1 + (m - 1) * 13]
                    elif n == 1 and m == 0:
                        self.p[n + m * 13] = ct * self.p[n - 1 + m * 13]
                        dp[m][n] = ct * dp[m][n - 1] - st * self.p[n - 1 + m * 13]
                    elif n > 1 and n != m:
                        if m > n - 2:
                            self.p[n - 2 + m * 13] = 0.0
                        if m > n - 2:
                            dp[m][n - 2] = 0.0
                        self.p[n + m * 13] = ct * self.p[n - 1 + m * 13] - self.k[m][n] * self.p[n - 2 + m * 13]
                        dp[m][n] = ct * dp[m][n - 1] - st * self.p[n - 1 + m * 13] - self.k[m][n] * dp[m][n - 2]

                # TIME ADJUST THE GAUSS COEFFICIENTS
                # TODO #1: Legacy C code static vars for speed
                # if time != otime:
                if True:
                    tc[m][n] = self.c[m][n] + dt * self.cd[m][n]
                    if m != 0:
                        tc[n][m - 1] = self.c[n][m - 1] + dt * self.cd[n][m - 1]

                # ACCUMULATE TERMS OF THE SPHERICAL HARMONIC EXPANSIONS
                par = ar * self.p[n + m * 13]
                if m == 0:
                    temp1 = tc[m][n] * cp[m]
                    temp2 = tc[m][n] * sp[m]
                else:
                    temp1 = tc[m][n] * cp[m] + tc[n][m - 1] * sp[m]
                    temp2 = tc[m][n] * sp[m] - tc[n][m - 1] * cp[m]
                bt = bt - ar * temp1 * dp[m][n]
                bp += self.fm[m] * temp2 * par
                br += self.fn[n] * temp1 * par

                # SPECIAL CASE:  NORTH/SOUTH GEOGRAPHIC POLES
                if st == 0.0 and m == 1:
                    if n == 1:
                        pp[n] = pp[n - 1]
                    else:
                        pp[n] = ct * pp[n - 1] - self.k[m][n] * pp[n - 2]
                    parp = ar * pp[n]
                    bpp += self.fm[m] * temp2 * parp

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
        if math.fabs(glat) >= 55.0:
            if glat > 0.0 and glon >= 0.0:
                result.gv = result.d - glon
            if glat > 0.0 and glon < 0.0:  # noqa pyCharm: simplify chained comparison
                result.gv = result.d + math.fabs(glon)
            if glat < 0.0 and glon >= 0.0:  # noqa pyCharm: simplify chained comparison
                result.gv = result.d + glon
            if glat < 0.0 and glon < 0.0:
                result.gv = result.d - math.fabs(glon)
            if result.gv > +180.0:
                result.gv -= 360.0
            if result.gv < -180.0:
                result.gv += 360.0
        if result.gv == gv_default:
            result.gv = None

        result.compute()

        # TODO #1: Legacy C code static vars for speed
        # otime = time
        # oalt = alt
        # olat = glat
        # olon = glon

        return result

    @classmethod
    def create_list(cls, length, default=None):
        """Create a list of length with an optional default."""
        return [default] * length

    @classmethod
    def create_matrix(cls, rows, columns, default=None):
        """Create a 2 dimensional matrix of length with an optional default."""
        return [[default for _ in range(columns)] for _ in range(rows)]

    def get_model_filename(self):
        """Determine the model filename to load the coefficients from."""
        if self.coefficients_file is None:
            self.coefficients_file = "wmm/WMM.COF"

        # some lightweight versions of Python won't have access to methods like "os.path.dirname"
        if self.coefficients_file[0] in "\\/":
            return self.coefficients_file
        filepath = __file__
        filepath = filepath.replace("geomag.py", self.coefficients_file)

        return filepath

    def load_coefficients(self):
        """Load the coefficients model to calculate the Magnetic Components from."""
        if self.epoch is not None:
            return

        c = self.create_matrix(13, 13)
        cd = self.create_matrix(13, 13)
        snorm = self.create_list(169)
        fn = self.create_list(13)
        fm = self.create_list(13)
        k = self.create_matrix(13, 13)

        model_filename = self.get_model_filename()

        with open(model_filename) as coefficients_file:
            # READ WORLD MAGNETIC MODEL SPHERICAL HARMONIC COEFFICIENTS
            c[0][0] = 0.0
            cd[0][0] = 0.0

            line_data = coefficients_file.readline()
            line_values = line_data.split()
            if len(line_values) != 3:
                raise ValueError("Invalid header in model file")
            epoch, model = (t(s) for t, s in zip((float, str), line_values))

            while True:
                line_data = coefficients_file.readline()

                # CHECK FOR LAST LINE IN FILE
                if line_data[:4] == "9999":
                    break

                # END OF FILE NOT ENCOUNTERED, GET VALUES
                line_values = line_data.split()
                if len(line_values) != 6:
                    raise ValueError("Corrupt record in model file")
                n, m, gnm, hnm, dgnm, dhnm = (t(s) for t, s in zip((int, int, float, float, float, float), line_values))

                if m > self.maxord:
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
        for n in range(1, self.maxord + 1):
            snorm[n] = snorm[n - 1] * float(2 * n - 1) / float(n)
            j = 2
            m = 0
            D1 = 1  # noqa pyCharm: Variable in function should be lowercase
            D2 = (n - m + D1) / D1  # noqa pyCharm: Variable in function should be lowercase
            while D2 > 0:
                k[m][n] = float(((n - 1) * (n - 1)) - (m * m)) / float((2 * n - 1) * (2 * n - 3))
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

        self.epoch = epoch
        self.c = c
        self.cd = cd
        self.p = snorm
        self.fn = fn
        self.fm = fm
        self.k = k
