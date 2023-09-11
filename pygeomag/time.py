SECONDS_PER_DAY = 86400


def decimal_year_from_struct_time(date):
    """
    Calculate the decimal year (2022.5) from a 'time.struct_time'.

    >>> import time
    >>> from pygeomag import decimal_year_from_struct_time
    >>> value = time.struct_time((2020, 7, 2, 0, 0, 0, 0, 0, 0))
    >>> decimal_year_from_struct_time(value)
    2020.5
    """
    # Inline imports to not fail on lightweight versions of Python
    import time

    # we want to clear out tm_wday, tm_yday, and tm_isdst because they can mess with the result from mktime
    # For instance, if tm_isdst is 1 it would subtract an hour from 2022-07-02T00:00:00 making it 2022-07-01T23:00:00
    # and thus a different day
    date = time.struct_time(tuple(date[:6]) + (0, 0, 0))
    year = date.tm_year
    current_year = time.mktime(time.struct_time((year, 1, 1, 0, 0, 0, 0, 0, 0)))
    following_year = time.mktime(time.struct_time((year + 1, 1, 1, 0, 0, 0, 0, 0, 0)))
    days_in_year = (following_year - current_year) / SECONDS_PER_DAY
    days_passed = int((time.mktime(date) - current_year) / SECONDS_PER_DAY)
    return year + float(days_passed) / days_in_year


def decimal_year_from_date(date):
    """
    Calculate the decimal year (2022.5) from a 'datetime.date' or 'datetime.datetime'.

    >>> import datetime
    >>> from pygeomag import decimal_year_from_date
    >>> value = datetime.datetime(2020, 7, 2)
    >>> decimal_year_from_date(value)
    2020.5
    """
    # Inline imports to not fail on lightweight versions of Python
    import datetime

    if isinstance(date, datetime.datetime):
        date = date.date()
    year = date.year
    current_year = datetime.date(year + 1, 1, 1)
    following_year = datetime.date(year, 1, 1)
    days_in_year = (current_year - following_year).days
    days_passed = (date - datetime.date(year, 1, 1)).days
    return year + float(days_passed) / days_in_year


def calculate_decimal_year(date):
    """
    Calculate the decimal year (2022.5) from a value (i.e. 'datetime.datetime' or 'time.struct_time').

    If you know using either date format will work in your version of Python, you can use this wrapper method.

    >>> import datetime
    >>> from pygeomag import calculate_decimal_year
    >>> calculate_decimal_year(datetime.datetime(2020, 7, 2))
    2020.5
    """
    # Inline imports to not fail on lightweight versions of Python
    import datetime
    import time

    if isinstance(date, (float, int)):
        if date < 3000:
            return float(date)
        else:
            return decimal_year_from_struct_time(time.localtime(date))
    elif isinstance(date, datetime.date):
        return decimal_year_from_date(date)
    elif isinstance(date, time.struct_time):
        return decimal_year_from_struct_time(date)

    raise TypeError("Unsupported date format")
