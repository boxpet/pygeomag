import math


def round_to_digits(number, number_of_digits=0):
    """
    Round to number of digits, removing all if `0` and not Pythons round to even number strategy.

    >>> from pygeomag import round_to_digits
    >>> round_to_digits(45.7625, 0)
    46
    >>> round_to_digits(45.7625, 1)
    45.8
    >>> round_to_digits(45.7625, 2)
    45.76
    """
    multiplier = 10**number_of_digits
    abs_rounded_value = math.floor(abs(number) * multiplier + 0.5) / multiplier
    rounded_value = math.copysign(abs_rounded_value, number)
    return int(rounded_value) if number_of_digits == 0 else rounded_value


def decimal_degrees_to_degrees_minutes(decimal_degrees):
    """
    Convert decimal degrees to degrees and minutes.

    >>> from pygeomag import decimal_degrees_to_degrees_minutes
    >>> decimal_degrees_to_degrees_minutes(45.7625)
    (45, 45.75)
    """
    if not isinstance(decimal_degrees, (int, float)):
        raise TypeError("value is not a number")

    degrees = int(decimal_degrees)
    minutes = round_to_digits((float(decimal_degrees) - degrees) * 60, 12)

    return degrees, abs(minutes)


def decimal_degrees_to_degrees_minutes_seconds(decimal_degrees):
    """
    Convert decimal degrees to degrees, minutes and seconds.

    >>> from pygeomag import decimal_degrees_to_degrees_minutes_seconds
    >>> decimal_degrees_to_degrees_minutes_seconds(45.7625)
    (45, 45, 45.0)
    """
    degrees, decimal_minutes = decimal_degrees_to_degrees_minutes(decimal_degrees)
    minutes = int(decimal_minutes)
    seconds = round_to_digits((float(decimal_minutes) - minutes) * 60, 12)

    return degrees, minutes, seconds


def degrees_minutes_seconds_to_decimal_degrees(degrees, minutes, seconds):
    """
    Convert degrees, minutes and seconds  to decimal degrees.

    >>> from pygeomag import degrees_minutes_seconds_to_decimal_degrees
    >>> degrees_minutes_seconds_to_decimal_degrees(45, 45, 45)
    45.7625
    """
    if not isinstance(degrees, (int, float)):
        raise TypeError("degrees is not a number")
    if not isinstance(minutes, (int, float)):
        raise TypeError("minutes is not a number")
    if not isinstance(seconds, (int, float)):
        raise TypeError("seconds is not a number")

    return degrees + minutes / 60 + seconds / 3600


def degrees_minutes_to_decimal_degrees(degrees, minutes):
    """
    Convert degrees and minutes  to decimal degrees (45.7625).

    >>> from pygeomag import degrees_minutes_to_decimal_degrees
    >>> degrees_minutes_to_decimal_degrees(45, 45.75)
    45.7625
    """
    if not isinstance(degrees, (int, float)):
        raise TypeError("degrees is not a number")
    if not isinstance(minutes, (int, float)):
        raise TypeError("minutes is not a number")

    return degrees + minutes / 60


def pretty_print_degrees(decimal_degrees, is_latitude, show_seconds=False, full_words=False, number_of_digits=0):
    """
    Format decimal degrees into a human-readable string.

    :param float, int decimal_degrees: Decimal degrees you want converted
    :param bool is_latitude: True for latitude, False for longitude
    :param bool show_seconds: True to show seconds, False for just degrees and minutes
    :param bool full_words: True to use full words like "North", False for single characters like "N"
    :param int number_of_digits: The amount of digits to round the last value to
    :return: Human-readable string

    >>> from pygeomag import pretty_print_degrees
    >>> pretty_print_degrees(decimal_degrees=45.7625, is_latitude=True)
    "45° 46' N"
    >>> pretty_print_degrees(decimal_degrees=45.7625, is_latitude=True, number_of_digits=2)
    "45° 45.75' N"
    >>> pretty_print_degrees(decimal_degrees=45.7625, is_latitude=True, full_words=True, number_of_digits=2)
    '45 Degrees 45.75 Minutes North'
    """
    if show_seconds:
        degrees, minutes, seconds = decimal_degrees_to_degrees_minutes_seconds(decimal_degrees)
        seconds = round_to_digits(seconds, number_of_digits)
        string_format = "{degrees}{degrees_word} {minutes}{minutes_word} {seconds}{seconds_word} {ordinal_word}"
    else:
        degrees, minutes = decimal_degrees_to_degrees_minutes(decimal_degrees)
        minutes = round_to_digits(minutes, number_of_digits)
        seconds = 0
        string_format = "{degrees}{degrees_word} {minutes}{minutes_word} {ordinal_word}"

    if full_words:
        degrees_word = " Degrees"
        minutes_word = " Minutes"
        seconds_word = " Seconds"
    else:
        degrees_word = "\xB0"
        minutes_word = "'"
        seconds_word = '"'

    if is_latitude and decimal_degrees >= 0:
        ordinal_word = "North"
    elif is_latitude and decimal_degrees < 0:
        ordinal_word = "South"
    elif not is_latitude and decimal_degrees >= 0:
        ordinal_word = "East"
    else:
        ordinal_word = "West"

    if not full_words:
        ordinal_word = ordinal_word[0]

    return string_format.format(
        degrees=abs(degrees),
        degrees_word=degrees_word,
        minutes=minutes,
        minutes_word=minutes_word,
        seconds=seconds,
        seconds_word=seconds_word,
        ordinal_word=ordinal_word,
    )
