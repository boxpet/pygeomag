from unittest import TestCase

from pygeomag import (
    decimal_degrees_to_degrees_minutes,
    decimal_degrees_to_degrees_minutes_seconds,
    degrees_minutes_seconds_to_decimal_degrees,
    degrees_minutes_to_decimal_degrees,
    pretty_print_degrees,
    round_to_digits,
)


class TestFormat(TestCase):
    def test_round_precision(self):
        self.assertEqual(round_to_digits(-1.559453, 6), -1.559453)
        self.assertEqual(round_to_digits(-1.559453, 5), -1.55945)
        self.assertEqual(round_to_digits(-1.559453, 4), -1.5595)
        self.assertEqual(round_to_digits(-1.559453, 3), -1.559)
        self.assertEqual(round_to_digits(-1.559453, 2), -1.56)
        self.assertEqual(round_to_digits(-1.559453, 1), -1.6)
        self.assertEqual(round_to_digits(-1.559453, 0), -2)
        self.assertEqual(round_to_digits(1.559453, 6), 1.559453)
        self.assertEqual(round_to_digits(1.559453, 5), 1.55945)
        self.assertEqual(round_to_digits(1.559453, 4), 1.5595)
        self.assertEqual(round_to_digits(1.559453, 3), 1.559)
        self.assertEqual(round_to_digits(1.559453, 2), 1.56)
        self.assertEqual(round_to_digits(1.559453, 1), 1.6)
        self.assertEqual(round_to_digits(1.559453, 0), 2)
        self.assertEqual(round_to_digits(1.4, 1), 1.4)
        self.assertEqual(round_to_digits(1.5, 1), 1.5)
        self.assertEqual(round_to_digits(1.4, 0), 1)
        self.assertEqual(round_to_digits(1.5, 0), 2)

    def test_decimal_degrees_to_degrees_minutes(self):
        self.assertEqual(decimal_degrees_to_degrees_minutes(45.7625), (45, 45.75))

    def test_decimal_degrees_to_degrees_minutes_exception(self):
        with self.assertRaisesRegex(TypeError, "value is not a number"):
            decimal_degrees_to_degrees_minutes("exception")

    def test_decimal_degrees_to_degrees_minutes_seconds(self):
        self.assertEqual(
            decimal_degrees_to_degrees_minutes_seconds(45.7625), (45, 45, 45.0)
        )

    def test_degrees_minutes_seconds_to_decimal_degrees(self):
        self.assertEqual(
            degrees_minutes_seconds_to_decimal_degrees(45, 45, 45), 45.7625
        )

    def test_degrees_minutes_seconds_to_decimal_degrees_exception(self):
        with self.assertRaisesRegex(TypeError, "degrees is not a number"):
            degrees_minutes_seconds_to_decimal_degrees("exception", 0, 0)
        with self.assertRaisesRegex(TypeError, "minutes is not a number"):
            degrees_minutes_seconds_to_decimal_degrees(0, "exception", 0)
        with self.assertRaisesRegex(TypeError, "seconds is not a number"):
            degrees_minutes_seconds_to_decimal_degrees(0, 0, "exception")

    def test_degrees_minutes_to_decimal_degrees(self):
        self.assertEqual(degrees_minutes_to_decimal_degrees(45, 45.75), 45.7625)

    def test_degrees_minutes_to_decimal_degrees_exception(self):
        with self.assertRaisesRegex(TypeError, "degrees is not a number"):
            degrees_minutes_to_decimal_degrees("exception", 0)
        with self.assertRaisesRegex(TypeError, "minutes is not a number"):
            degrees_minutes_to_decimal_degrees(0, "exception")

    def test_pretty_print_degrees(self):
        self.assertEqual(
            pretty_print_degrees(decimal_degrees=45.7625, is_latitude=True), "45° 46' N"
        )
        self.assertEqual(
            pretty_print_degrees(decimal_degrees=-45.7625, is_latitude=True),
            "45° 46' S",
        )
        self.assertEqual(
            pretty_print_degrees(decimal_degrees=45.7625, is_latitude=False),
            "45° 46' E",
        )
        self.assertEqual(
            pretty_print_degrees(decimal_degrees=-45.7625, is_latitude=False),
            "45° 46' W",
        )
        self.assertEqual(
            pretty_print_degrees(
                decimal_degrees=45.7625, is_latitude=True, show_seconds=True
            ),
            "45° 45' 45\" N",
        )
        self.assertEqual(
            pretty_print_degrees(
                decimal_degrees=45.7625, is_latitude=True, number_of_digits=2
            ),
            "45° 45.75' N",
        )
        self.assertEqual(
            pretty_print_degrees(
                decimal_degrees=45.7625,
                is_latitude=True,
                full_words=True,
                number_of_digits=2,
            ),
            "45 Degrees 45.75 Minutes North",
        )
