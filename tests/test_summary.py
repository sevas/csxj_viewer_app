__author__ = 'sevas'

import sys
sys.path.append('../summary/')
sys.path.append('../dependencies/')
import unittest
from datetime import date, time

from views import get_latest_hour, get_latest_day

class TestUtilFuncs(unittest.TestCase):
    def test_get_latest_hour(self):
        hours = ['10.54.12', '00.00.00', '02.30.34']
        self.assertEquals(get_latest_hour(hours), '10.54.12')


    def test_get_latest_day(self):
        days = ['2011-04-19', '2011-04-18', '2011-04-20']
        self.assertEquals(get_latest_day(days), '2011-04-20')
