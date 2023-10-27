#This will be the file for the actual unit tests

import unittest

from unitTests import getArea
from math import pi

class TestCircleArea(unittest.TestCase):
    def testArea(self):
        #Test areas when radius >= 0
        self.assertAlmostEqual(getArea(1), pi)
        self.assertAlmostEqual(getArea(0), 0)
        self.assertAlmostEqual(getArea(2.1), pi * 2.1**2)

    def testVals(self):
        self.assertRaises(ValueError, getArea, -2)

    def testType(self):
        self.assertRaises(TypeError, getArea, 3 + 5j)
        self.assertRaises(TypeError, getArea, True)
        self.assertRaises(TypeError, getArea, "Hello!")