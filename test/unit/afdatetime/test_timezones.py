"""Unit tests for pyairfire.datetime.parsing"""

__author__ = "Joel Dubowy"
__copyright__ = "Copyright 2016, AirFire, PNW, USFS"

import datetime
from py.test import raises

from afdatetime.timezones import UtcOffsetFinder
from afdatetime.timezones import DstAccurateTimeZone


class TestUtcOffsetFinder(object):

    def test_pdt(self):
        actual = UtcOffsetFinder().find(45.0, -118.4,
            datetime.datetime(2015, 2, 1, 10, 9, 8))
        expected = (datetime.timedelta(hours=-8), '-08:00')
        assert expected == actual

    def test_pst(self):
        actual = UtcOffsetFinder().find(45.0, -118.4,
            datetime.datetime(2015, 8, 1, 10, 9, 8))
        expected = (datetime.timedelta(hours=-7), '-07:00')
        assert expected == actual

class TestDstAccurateTimeZone(object):

    def test_pst(self):
        actual = DstAccurateTimeZone().find(45.0, -118.4,
            datetime.datetime(2015, 2, 1, 10, 9, 8))
        expected = {'name': 'America/Los_Angeles', 'abbreviation': 'PST', 'dst': False}
        assert expected == actual

    def test_pdt(self):
        actual = DstAccurateTimeZone().find(45.0, -118.4,
            datetime.datetime(2015, 8, 1, 10, 9, 8))
        expected = {'name': 'America/Los_Angeles', 'abbreviation': 'PDT', 'dst': True}
        assert expected == actual


