import unittest
import os
import glob
from PIL import Image

from ..utility import QtTest
from ...model.XESModel import XESModel
from ...model.XESSpectrum import XESSpectrum

from ...model.calib import detector_calibration


import numpy as np

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')


class ROITest(QtTest):
    def setUp(self):
        self.model = XESModel()

    def tearDown(self):
        del self.model

    def test_sum_all_image(self):
        roi_start = 0
        roi_width = 487
        roi_left = 0
        roi_range = 195

        im_data = self.helper_read_example_image()
        roi_sum = self.model.sum_rect_roi(im_data, roi_start, roi_width, roi_left, roi_range)
        self.assertEqual(22265, roi_sum)

        self.helper_close_image_file()

    def test_sum_image_parts(self):
        im_data = self.helper_read_example_image()
        roi_start = 20
        roi_width = 10
        roi_left = 24
        roi_range = 10
        roi_sum1 = self.model.sum_rect_roi(im_data, roi_start - roi_width, roi_width-1, roi_left, roi_range)
        roi_sum2 = self.model.sum_rect_roi(im_data, roi_start, roi_width-1, roi_left, roi_range)
        roi_sum3 = self.model.sum_rect_roi(im_data, roi_start + roi_width, roi_width, roi_left, roi_range)
        roi_sum_all = self.model.sum_rect_roi(im_data, roi_start - roi_width, 3*roi_width, roi_left, roi_range)
        self.assertEqual(roi_sum_all - roi_sum1 - roi_sum3, roi_sum2)

        roi_sum1 = self.model.sum_rect_roi(im_data, roi_start, roi_width, roi_left-roi_range, roi_range-1)
        roi_sum2 = self.model.sum_rect_roi(im_data, roi_start, roi_width, roi_left, roi_range-1)
        roi_sum3 = self.model.sum_rect_roi(im_data, roi_start, roi_width, roi_left+roi_range, roi_range)
        roi_sum_all = self.model.sum_rect_roi(im_data, roi_start, roi_width, roi_left-roi_range, 3*roi_range)
        self.assertEqual(roi_sum_all - roi_sum1 - roi_sum3, roi_sum2)

        self.helper_close_image_file()

    def test_general_roi_sum(self):
        im_data = self.helper_read_example_image()

        max_ind = np.unravel_index(np.argmax(im_data), im_data.shape)
        roi = np.zeros_like(im_data, dtype=bool)
        roi[max_ind] = True
        roi_sum = self.model.sum_general_roi(im_data, roi)
        self.assertEqual(roi_sum, im_data[max_ind])

        roi_all = np.ones_like(im_data, dtype=bool)
        all_sum = self.model.sum_general_roi(im_data, roi_all)

        roi_all[max_ind] = False
        all_minus_max_sum = self.model.sum_general_roi(im_data, roi_all)
        self.assertEqual(all_sum - all_minus_max_sum, roi_sum)

        self.helper_close_image_file()

    def test_roi_for_theta(self):
        ind = 10
        self.model.calibration = {
            'roi_left': 0.0,
            'roi_range': 195.0,
            'roi_start': 13061.0,
            'roi_width': 10.0,
            'slope': -192.54,
            'theta_zero': -0.3,
        }
        files_list = self.helper_load_fe_wire_files_into_model()
        self.model.set_current_image(ind)
        roi_start, roi_end = self.model.theta_to_roi(self.model.current_spectrum.all_data[ind]['theta'])
        self.assertFalse(self.model.current_roi_data[0][int(roi_start)-1])
        self.assertTrue(self.model.current_roi_data[0][int(roi_start)])
        self.assertTrue(self.model.current_roi_data[0][int(roi_start)]+1)

    def helper_read_example_image(self):
        filename = os.path.normpath(os.path.join(data_path, 'FeWire_001.tif'))
        self.img_file = open(filename, 'rb')
        self.im = Image.open(self.img_file)
        im_data = np.array(self.im)[::-1]
        return im_data

    def helper_close_image_file(self):
        self.im.close()
        self.img_file.close()

    def helper_load_fe_wire_files_into_model(self):
        fe_wire_data_path = os.path.join(data_path, 'Fe_Wire')
        file_list = sorted(glob.glob(os.path.join(fe_wire_data_path, 'FeWire_*.tif')))
        self.model.xes_spectra.append(XESSpectrum())
        self.model.open_files(-1, file_list)
        self.model.add_data_set_to_spectrum(-1)
        return file_list


if __name__ == '__main__':
    unittest.main()
