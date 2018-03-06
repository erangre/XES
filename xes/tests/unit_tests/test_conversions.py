import unittest
from ..utility import QtTest
from ...model.XESModel import XESModel
import os
# import numpy as np

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')


class ConverterTest(QtTest):
    def setUp(self):
        self.model = XESModel()

    def tearDown(self):
        del self.model

    def test_theta_to_ev(self):
        theta = 66.18
        th_ev = 7058
        calc_ev = self.model.theta_to_ev(theta)
        self.assertAlmostEqual(th_ev, calc_ev, 0)

    def test_ev_to_theta(self):
        ev = 7058
        th_theta = 66.18
        calc_theta = self.model.ev_to_theta(ev)
        self.assertAlmostEqual(th_theta, calc_theta, 2)


if __name__ == '__main__':
    unittest.main()
