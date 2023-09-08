import datetime
import os
import time
from unittest import TestCase

from pygeomag import (
    calculate_decimal_year,
    decimal_year_from_date,
    decimal_year_from_struct_time,
)


class TestHelpers(TestCase):
    def test_calculate_decimal_year(self):
        test_parameters = (
            (2020, 2020.0),
            (2020.5, 2020.5),
            (1593676800, 2020.5),
            (1593676800.0, 2020.5),
            (datetime.date(2020, 7, 2), 2020.5),
            (datetime.datetime(2020, 7, 2), 2020.5),
            (time.struct_time((2020, 7, 2, 0, 0, 0, 0, 0, 0)), 2020.5),
        )

        for test_parameter in test_parameters:
            year = calculate_decimal_year(test_parameter[0])
            self.assertAlmostEqual(test_parameter[1], year, 4)

    def test_calculate_decimal_year_exception(self):
        with self.assertRaisesRegex(TypeError, "Unsupported date format"):
            calculate_decimal_year("invalid")

    def test_decimal_year_from_date(self):
        test_parameters = (
            ((2020, 1, 1), 2020.0),
            ((2020, 1, 2), 2020.0027),
            ((2020, 7, 2), 2020.5),
            ((2022, 1, 1), 2022.0),
            ((2022, 1, 2), 2022.0027),
            ((2022, 7, 2), 2022.4986),
        )

        for test_parameter in test_parameters:
            date = datetime.date(*test_parameter[0])
            year = decimal_year_from_date(date)
            self.assertAlmostEqual(test_parameter[1], year, 4)

    def test_decimal_year_from_datetime(self):
        test_parameters = (
            ((2020, 1, 1, 0, 0, 0), 2020.0),
            ((2020, 1, 1, 23, 59, 59), 2020.0),
            ((2020, 1, 2, 0, 0, 0), 2020.0027),
            ((2020, 7, 2, 0, 0, 0), 2020.5),
            ((2022, 1, 1, 0, 0, 0), 2022.0),
            ((2022, 1, 1, 23, 59, 59), 2022.0),
            ((2022, 1, 2, 0, 0, 0), 2022.0027),
            ((2022, 7, 2, 0, 0, 0), 2022.4986),
        )

        for test_parameter in test_parameters:
            date = datetime.datetime(*test_parameter[0])
            year = decimal_year_from_date(date)
            self.assertAlmostEqual(test_parameter[1], year, 4)

    def test_decimal_year_from_struct_time(self):
        # tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst, result
        test_parameters = (
            ((2020, 1, 1, 0, 0, 0, 0, 0, 0), 2020.0),
            ((2020, 1, 1, 23, 59, 59, 0, 0, 0), 2020.0),
            ((2020, 1, 2, 0, 0, 0, 0, 0, 0), 2020.0027),
            ((2020, 7, 2, 0, 0, 0, 0, 0, 0), 2020.5),
            ((2022, 1, 1, 0, 0, 0, 0, 0, 0), 2022.0),
            ((2022, 1, 1, 23, 59, 59, 0, 0, 0), 2022.0),
            ((2022, 1, 2, 0, 0, 0, 0, 0, 0), 2022.0027),
            ((2022, 7, 2, 0, 0, 0, 0, 0, 0), 2022.4986),
        )

        for test_parameter in test_parameters:
            struct_time = time.struct_time(test_parameter[0])
            year = decimal_year_from_struct_time(struct_time)
            self.assertAlmostEqual(test_parameter[1], year, 4)

    def test_decimal_year_from_struct_time_with_dst(self):
        # With tm_isdst=1, it's an hour later, so technically still the 1st. Making sure these return the same value

        # (tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst), result
        test_parameters = (
            ((2020, 7, 2, 0, 0, 0, 3, 184, 1), 2020.5),
            ((2020, 7, 2, 0, 0, 0, 0, 0, 0), 2020.5),
        )

        # Needed in case running in a timezone with no DST, like UTC
        os.environ["TZ"] = "US/Pacific"
        time.tzset()

        with_dst = time.mktime(time.struct_time(test_parameters[0][0]))
        without_dst = time.mktime(time.struct_time(test_parameters[1][0]))
        self.assertNotEqual(with_dst, without_dst)
