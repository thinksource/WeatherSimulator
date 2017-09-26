import unittest
import config

from utility import *
from datetime import datetime
from time import mktime
from main import generate_place

conf=config.conf

class UtilityTests(unittest.TestCase):
    def test_random_date(self):
        format = "%d/%m/%Y"
        dt = random_date(config.conf["start_time"], config.conf["end_time"])
        dbegin = mktime(time.strptime(config.conf["start_time"], format))
        dend = mktime(time.strptime(config.conf["end_time"], format))
        self.assertTrue(dt >= datetime.fromtimestamp(dbegin))
        self.assertTrue(datetime.fromtimestamp(dend) >= dt)

    def test_random_temp(self):
        t = random_temp(75, conf)
        self.assertTrue(isinstance(t, float))
        self.assertTrue(t > -100)
        self.assertTrue(t < 100)
        t=random_temp(-18, conf)
        self.assertTrue(isinstance(t, float))
        self.assertTrue(t > -100)
        self.assertTrue(t < 100)

    def test_random_pressure(self):
        p=random_pressure(18)
        self.assertTrue(isinstance(p, float))
        self.assertTrue(p > 500)
        self.assertTrue(p < 2000)

    def test_random_humidity(self):
        d=random_humidity("sunny")
        self.assertTrue(isinstance(d, int))
        self.assertTrue(d >= 0)
        self.assertTrue(d <= 100)

    def test_address(self):
        ad=get_address(-33.865, 151.2094)
        self.assertEqual(ad, "Sydney")
        ad=get_address(41.8369,-87.6847)
        self.assertEqual(ad, "Chicago")

    # assert the empty string
    def test_empty_address(self):
        ad=get_address(-87.89,0.25)
        self.assertEqual(ad, "")

   #sometimes it may fail as no googlekey and google may not response correct height
    def test_height(self):
        h=get_height(-37.83, 144.98)
        self.assertTrue(isinstance(h, float))
        self.assertTrue(h > 18)
        self.assertTrue(h < 19)

    # assert the zero height
    def test_zeroheight(self):
        h=get_height(-18.15,163.15)
        self.assertTrue(h == 0)

class MyTests(unittest.TestCase):
    def test_place_generate(self):
        p=generate_place(-37.83, 144.98)
        self.assertEqual(p["address"], 'Melbourne')
        a=p["location"].split(",")
        self.assertEqual(str(-37.83), a[0])
        self.assertEqual(str(144.98), a[1])

if __name__=='__main__':
    unittest.main()
