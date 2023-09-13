import os
from unittest import TestCase

from pygeomag import GeoMag, GeoMagResult


def get_test_filename(filename):
    return os.path.join(os.path.dirname(__file__), filename)


class TestGeoMagResult(TestCase):
    def test_d_property(self):
        result = GeoMagResult(0, 0, 0, 0)
        result.d = 5
        self.assertEqual(result.d, result.dec)

    def test_f_properties(self):
        result = GeoMagResult(0, 0, 0, 0)
        result.f = 5
        self.assertEqual(result.f, result.ti)
        self.assertEqual(result.f, result.total_intensity)

    def test_i_property(self):
        result = GeoMagResult(0, 0, 0, 0)
        result.i = 5
        self.assertEqual(result.i, result.dip)
        self.assertEqual(result.i, result.inclination)


class TestGeoMag(TestCase):
    def test_calculate_declination_from_wmm(self):
        geo_mag = GeoMag()

        with open(get_test_filename("test_values/WMM2020testvalues.txt")) as test_values_file:
            for row, test_parameter in enumerate(test_values_file):
                if test_parameter[0] == "#":
                    continue

                time, alt, glat, glon, x, y, z, h, f, i, d, gv, _, _, _, _, _, _, _ = (
                    t(s)
                    for t, s in zip(
                        (
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                            float,
                        ),
                        test_parameter.split(),
                    )
                )

                result = geo_mag.calculate(glat, glon, alt, time)
                gv_test = -999 if result.gv is None else result.gv

                self.assertAlmostEqual(x, result.x, 1, f"Row {row}: X (nT) expected {x}, result {result.x}")
                self.assertAlmostEqual(y, result.y, 1, f"Row {row}: Y (nT) expected {y}, result {result.y}")
                self.assertAlmostEqual(z, result.z, 1, f"Row {row}: Z (nT) expected {z}, result {result.z}")
                self.assertAlmostEqual(h, result.h, 1, f"Row {row}: H (nT) expected {h}, result {result.h}")
                self.assertAlmostEqual(f, result.f, 1, f"Row {row}: F (nT) expected {f}, result {result.f}")
                self.assertAlmostEqual(i, result.i, 2, f"Row {row}: I (Deg) expected {i}, result {result.i}")
                self.assertAlmostEqual(d, result.d, 2, f"Row {row}: D (Deg) expected {d}, result {result.d}")
                self.assertAlmostEqual(gv, gv_test, 2, f"Row {row}: GV (Deg) expected {gv}, result {result.gv}")

    def test_calculate_declination_time_beyond_model_bypass(self):
        geo_mag = GeoMag()
        result = geo_mag.calculate(0, 80, 0, 2030, allow_date_past_lifespan=True)
        self.assertIsInstance(result, GeoMagResult)

    def test_calculate_declination_time_beyond_model_raises(self):
        geo_mag = GeoMag()
        with self.assertRaisesRegex(ValueError, "Time extends beyond model 5-year life span"):
            geo_mag.calculate(0, 80, 0, 2030)

    def test_create_list(self):
        self.assertEqual(GeoMag._create_list(2), [None, None])
        self.assertEqual(GeoMag._create_list(3, 0), [0, 0, 0])
        self.assertNotEqual(GeoMag._create_list(4, 0), [1, 1, 1, 1])

    def test_create_matrix(self):
        self.assertEqual(GeoMag._create_matrix(2, 2), [[None, None], [None, None]])
        self.assertEqual(GeoMag._create_matrix(2, 3, 0), [[0, 0, 0], [0, 0, 0]])
        self.assertNotEqual(GeoMag._create_matrix(2, 4), [[1, 1, 1, 1], [1, 1, 1, 1]])

    def test_get_model_filename_default(self):
        geo_mag = GeoMag()
        model_filename = geo_mag._get_model_filename()
        self.assertEqual(model_filename[-11:], "wmm/WMM.COF")

    def test_get_model_filename_different(self):
        geo_mag = GeoMag(coefficients_file="wmm/WMM_NEW.COF")
        model_filename = geo_mag._get_model_filename()
        self.assertEqual(model_filename[-15:], "wmm/WMM_NEW.COF")

    def test_get_model_filename_fullpath(self):
        geo_mag = GeoMag(coefficients_file="/wmm/WMM_NEW.COF")
        model_filename = geo_mag._get_model_filename()
        self.assertEqual(model_filename, "/wmm/WMM_NEW.COF")

    def test_load_coefficients_invalid_header(self):
        geo_mag = GeoMag(coefficients_file="../test/test_files/INVALID_HEADER.COF")
        with self.assertRaisesRegex(ValueError, "Invalid header in model file"):
            geo_mag.calculate(0, 80, 0, 2030)

    def test_load_coefficients_invalid_row(self):
        geo_mag = GeoMag(coefficients_file="../test/test_files/INVALID_ROW.COF")
        with self.assertRaisesRegex(ValueError, "Corrupt record in model file"):
            geo_mag.calculate(0, 80, 0, 2030)

    def test_load_coefficients_invalid_row_data(self):
        geo_mag = GeoMag(coefficients_file="../test/test_files/INVALID_ROW_DATA.COF")
        with self.assertRaisesRegex(ValueError, "Corrupt record in model file"):
            geo_mag.calculate(0, 80, 0, 2030)

    def test_load_coefficients_maxord(self):
        maxord_11_value = -3.4655
        maxord_12_value = -3.4599
        self.assertNotEqual(maxord_11_value, maxord_12_value)
        geo_mag = GeoMag()
        geo_mag._maxord = 11
        result = geo_mag.calculate(0, 80, 0, 2020)
        self.assertAlmostEqual(result.d, maxord_11_value, 4)
        geo_mag = GeoMag()
        geo_mag._maxord = 12
        result = geo_mag.calculate(0, 80, 0, 2020)
        self.assertAlmostEqual(result.d, maxord_12_value, 4)

    def test_load_coefficients_missing_file(self):
        geo_mag = GeoMag(coefficients_file="missing.cof")
        with self.assertRaisesRegex(FileNotFoundError, "No such file or directory"):
            geo_mag.calculate(0, 80, 0, 2030)
