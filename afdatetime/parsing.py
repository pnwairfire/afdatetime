"""afdatetime.parsing
"""

__author__      = "Joel Dubowy"

import datetime
import re

__all__ = [
    'parse',
    'parse_time_and_date',
    'fill_in_date',
    'parse_datetime',
    'parse_datetimes',
    'parse_utc_offset',
    'is_round_hour'
]

RECOGNIZED_DATETIME_FORMATS = [
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y/%m/%dT%H:%M:%S',
    '%Y/%m/%dT%H:%M:%SZ',
    '%Y%m%dT%H%M%S',
    '%Y%m%dT%H%M%SZ',
    '%Y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%SZ',
    '%Y/%m/%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%SZ',
    '%Y%m%d %H%M%S',
    '%Y%m%d %H%M%SZ',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%Y%m%d'
]

def parse(datetime_str, extra_formats=[]):
    if isinstance(datetime_str, datetime.date):
        return datetime_str

    for format in RECOGNIZED_DATETIME_FORMATS + extra_formats:
        try:
            return datetime.datetime.strptime(datetime_str, format)
        except ValueError:
            # Go on to next format
            pass
    # If we got here, none of them matched, so raise error
    raise ValueError("Invalid datetime format '%s'" % (datetime_str))


TIME_PATTERN = "%H:%M:%S"
DATE_PATTERN = "%Y-%m-%d"
ONE_DAY = datetime.timedelta(days=1)
def parse_time_and_date(t, d):
    if not t and not d:
        return None

    if t and d:
        pattern = 'T'.join([DATE_PATTERN, TIME_PATTERN])
        val = 'T'.join([d,t])
    elif t:
        pattern = TIME_PATTERN
        val = t
    elif d:
        pattern = DATE_PATTERN
        val = d

    try:
        dt = datetime.datetime.strptime(val, pattern)
    except ValueError:
        msg = ""
        if t:
            msg += " Time must be of the format '%s'." % (TIME_PATTERN)
        if d:
            msg += " Date must be of the format '%s'." % (DATE_PATTERN)
        raise ValueError(msg)

    if d:
        return dt
    else:
        return fill_in_date(dt)

def fill_in_date(dt):
    t = dt.time()
    n = datetime.datetime.utcnow()
    if (t > n.time()):
        d = n.date()
    else:
        d = n.date() + ONE_DAY

    return datetime.datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)

##
## Originally in bluesky package
##

def parse_datetime(v, k=None):
    """Parses datetime string and returns datetime object

    args:
     - v -- datetime string value

    kwargs:
     - k -- optional field name, to be used in exception message
    """
    try:
        return parse(v, extra_formats=['%Y-%m-%d %H:%M:%S'])
    except ValueError as e:
        # datetime_parsing will raise ValueError if invalid format; re-raise
        # wih specific msg
        raise ValueError("Invalid datetime format: {}{}".format(v,
            " (for '{}')".format(k) if k else ''))
    except TypeError as e:
        # TypeError will e raised if v is not a string; re-raise wih specific msg
        raise ValueError("Invalid datetime format: {}{}".format(v,
            " (for '{}')".format(k) if k else ''))

def parse_datetimes(d, *keys):
    r = {}
    for k in keys:
        try:
            r[k] = parse_datetime(d[k], k)
        except KeyError as e:
            raise ValueError("Missing '{}' datetime field".format(k))
    return r

OFFSET_MATCHER = re.compile('([+-]?\d{2}):?(\d{2})')
def parse_utc_offset(utc_offset_str):
    """Parses iso8601 formmated utc offset to float value

    Examples:
     > parse_utc_offset('+00:00')
     0.0
     > parse_utc_offset('+04:00')
     4.0
     > parse_utc_offset('-03:30')
     -3.5
     > parse_utc_offset('+0400')
     4.0


    TODO: look at other options:
     - https://bitbucket.org/micktwomey/pyiso8601/
     - https://github.com/dateutil/dateutil/
     - http://labix.org/python-dateutil
     - http://arrow.readthedocs.org/en/latest/
    """
    if isinstance(utc_offset_str, (float, int)):
        return float(utc_offset_str)

    if not utc_offset_str:
        raise ValueError("UTC offset not defined")

    m = OFFSET_MATCHER.match(utc_offset_str)
    if not m:
        raise ValueError("Invalid UTC offset string format: {}".format(utc_offset_str))

    hours = float(m.group(1))
    minutes = float(m.group(2))
    if hours < -13 or hours > 13 or minutes < 0 or minutes > 59:
        raise ValueError("Invalid UTC offset: {}".format(utc_offset_str))
    hour_fraction = minutes / 60.0
    return (hours - hour_fraction) if (hours < 0) else (hours + hour_fraction)

def is_round_hour(dt):
    """Returns true if datetime object is a round our

    TODO: move to different module
    """
    return dt.minute == dt.second == dt.microsecond == 0
