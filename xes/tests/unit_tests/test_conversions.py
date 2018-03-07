import unittest
import os

from ..utility import QtTest
from ...model.XESModel import XESModel

from ...model.calib import detector_calibration


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

    def test_theta_step_to_ev_step(self):
        ev = 7058.0
        theta = 66.18
        d_theta = 0.0183
        th_d_ev = 1.0
        calc_d_ev = self.model.theta_step_to_ev_step(ev, theta, d_theta)
        self.assertAlmostEqual(th_d_ev, calc_d_ev, 2)

    def test_theta_step_to_ev_step_using_two_thetas(self):
        theta1 = 66.18
        theta2 = 66.18 + 0.0183
        th_d_ev = 1.0
        ev1 = self.model.theta_to_ev(theta1)
        ev2 = self.model.theta_to_ev(theta2)
        self.assertAlmostEqual(th_d_ev, abs(ev1-ev2), 2)

    def test_roi_pos_for_theta(self):
        theta = 66.18
        th_roi = detector_calibration['roi_start'], \
                 detector_calibration['roi_start'] + detector_calibration['roi_width']
        roi = self.model.theta_to_roi(theta)
        self.assertEqual(th_roi, roi)
        # TODO: test for other theta values

if __name__ == '__main__':
    unittest.main()
