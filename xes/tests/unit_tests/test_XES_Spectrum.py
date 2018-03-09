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
        self.spectrum.add_data('test.tif', 66.18, 103, time.asctime(), 34.0, 80.0, 102.1)
        self.assertEqual(1, len(self.spectrum.all_data))

        # TODO: Continue working on the data structure.
