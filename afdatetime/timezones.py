import pytz

from timezonefinder import TimezoneFinder

class UtcOffsetFinder(object):
    """Finds utc offset given lat, lng, and datetime

    The reason for implementing this as a class is to allow single
    TimeZoneFinder instantiation for multiple utc_offset look-ups.
    """

    def __init__(self):
        self._timezone_finder = TimezoneFinder()

    def find(self, lat, lng, dt):
        """Returns utc offset information for a lat, lng, datetime
        combination.

        Args:
         - lat -- latitude of location
         - lng -- longitude of location
         - dt -- datetime (as UTC offset varies with date)

        Returns (datetime.timedelta, utc_offset_str) tuple
        """
        tz_str = self._timezone_finder.timezone_at(lng=lng, lat=lat)
        if not tz_str:
            return None, None

        tz = pytz.timezone(tz_str)
        td = tz.utcoffset(dt)
        offset_seconds = td.total_seconds()
        hours = int(offset_seconds / 3600)
        minutes = int((abs(offset_seconds) % 3600) / 60)
        hours_str = ('-' if hours<0 else '+') + str(abs(hours)).rjust(2,'0')
        minutes_str = str(minutes).rjust(2,'0')
        return td, hours_str + ':' + minutes_str
