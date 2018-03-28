import unittest
import os
from PIL import Image

from ..utility import QtTest
from ...model.XESModel import XESModel

from ...model.calib import detector_calibration


import numpy as np

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, '../data')


class ConverterTest(QtTest):
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

    def helper_read_example_image(self):
        filename = os.path.normpath(os.path.join(data_path, 'FeWire_001.tif'))
        self.img_file = open(filename, 'rb')
        self.im = Image.open(self.img_file)
        im_data = np.array(self.im)[::-1]
        return im_data

    def helper_close_image_file(self):
        self.im.close()
        self.img_file.close()


if __name__ == '__main__':
    unittest.main()
