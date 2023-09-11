import math


def round_precision(value, precision=0):
    """Round to precision digits, removing all if `0` and not Pythons round to even number strategy."""
    multiplier = 10**precision
    abs_rounded_value = math.floor(abs(value) * multiplier + 0.5) / multiplier
    rounded_value = math.copysign(abs_rounded_value, value)
    return int(rounded_value) if precision == 0 else rounded_value


def decimal_degrees_to_degrees_minutes(value):
    """
    Convert decimal degrees to degrees and minutes.

    >>> from pygeomag import decimal_degrees_to_degrees_minutes
    >>> decimal_degrees_to_degrees_minutes(45.7625)
    (45, 45.75)
    """
    if not isinstance(value, (int, float)):
        raise TypeError("value is not a number")

    degrees = int(value)
    minutes = round_precision((float(value) - degrees) * 60, 12)

    return degrees, abs(minutes)


def decimal_degrees_to_degrees_minutes_seconds(value):
    """
    Convert decimal degrees to degrees, minutes and seconds.

    >>> from pygeomag import decimal_degrees_to_degrees_minutes_seconds
    >>> decimal_degrees_to_degrees_minutes_seconds(45.7625)
    (45, 45, 45.0)
    """
    degrees, decimal_minutes = decimal_degrees_to_degrees_minutes(value)
    minutes = int(decimal_minutes)
    seconds = round_precision((float(decimal_minutes) - minutes) * 60, 12)

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


def pretty_print_degrees(value, is_latitude, show_seconds=False, verbose=False, precision=0):
    """
    Format decimal degrees into a human-readable string.

    :param value: (float, int) Decimal degrees you want converted
    :param is_latitude: (bool) True for latitude, False for longitude
    :param show_seconds: (bool) True to show seconds, False for just degrees and minutes
    :param verbose: (bool) True to use full words like "North", False for single characters like "N"
    :param precision: (int) The amount of digits to round the last value to
    :return: (str) human-readable string
    """
    if show_seconds:
        degrees, minutes, seconds = decimal_degrees_to_degrees_minutes_seconds(value)
        seconds = round_precision(seconds, precision)
        string_format = "{degrees}{degrees_word} {minutes}{minutes_word} {seconds}{seconds_word} {ordinal_word}"
    else:
        degrees, minutes = decimal_degrees_to_degrees_minutes(value)
        minutes = round_precision(minutes, precision)
        seconds = 0
        string_format = "{degrees}{degrees_word} {minutes}{minutes_word} {ordinal_word}"

    if verbose:
        degrees_word = " Degrees"
        minutes_word = " Minutes"
        seconds_word = " Seconds"
    else:
        degrees_word = "\xB0"
        minutes_word = "'"
        seconds_word = '"'

    if is_latitude and value >= 0:
        ordinal_word = "North"
    elif is_latitude and value < 0:
        ordinal_word = "South"
    elif not is_latitude and value >= 0:
        ordinal_word = "East"
    else:
        ordinal_word = "West"

    if not verbose:
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
