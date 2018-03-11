import unittest
import os
import time

from ..utility import QtTest
from ...model.XESSpectrum import XESSpectrum

from ...model.calib import detector_calibration


# import numpy as np

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')


class XESSpectrumTest(QtTest):
    def setUp(self):
        self.spectrum = XESSpectrum()

    def tearDown(self):
        del self.spectrum

    def test_add_data_point_to_spectrum(self):
        self.assertEqual(0, len(self.spectrum.all_data))
        self.spectrum.add_data('test.tif', 66.18, 103, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.assertEqual(1, len(self.spectrum.all_data))

    def test_gather_data_for_theta(self):
        theta = 66.18
        th_counts = self.helper_add_data_points()
        counts, exp_time = self.spectrum.gather_data_for_theta(theta)
        self.assertEqual(th_counts, counts)

    def helper_add_data_points(self):
        self.spectrum.add_data('test1.tif', 66.18, 103, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test2.tif', 66.28, 93, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test3.tif', 66.18, 108, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test4.tif', 66.18, 102, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test5.tif', 66.48, 120, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test6.tif', 66.18, 105, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test7.tif', 66.18, 103, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test8.tif', 66.18, 101, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('test9.tif', 66.68, 107, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        self.spectrum.add_data('testA.tif', 66.18, 103, 15.0, time.asctime(), 34.0, 80.0, 102.1)
        return 725
