# -*- coding: utf8 -*-
from mock import MagicMock
import os
import glob
import sys
import gc
import time
from PIL import Image
import numpy as np

from qtpy import QtWidgets, QtCore
from qtpy.QtTest import QTest

from ..ehook import excepthook
from ..utility import QtTest, unittest_data_path, enter_value_into_text_field, click_button
from ...model.XESModel import XESModel
from ...model.XESSpectrum import XESSpectrum
from ...widgets.MainAnalysisWidget import MainAnalysisWidget
from ...widgets.RawImageWidget import RawImageWidget

from ...controller.MainAnalysisController import MainAnalysisController
from ...controller.RawImageController import RawImageController

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, os.pardir, 'data')


class TestRawImageController(QtTest):
    def setUp(self):
        self.main_controller = MainAnalysisController()
        self.main_widget = self.main_controller.widget
        self.widget = self.main_widget.raw_image_widget
        self.model = self.main_controller.model
        self.controller = self.main_controller.raw_image_controller  # type: RawImageController

    def tearDown(self):
        del self.model
        del self.main_controller
        del self.main_widget
        gc.collect()

    def test_image_shows_raw_data(self):
        # sys.excepthook = excepthook
        ind = 0
        file_list = self.helper_load_fe_wire_files()
        im_data = self.helper_load_single_image_data(file_list[ind])

        self.model.set_current_image(ind)
        raw_image_data = self.widget.img_view.img_data

        self.assertTrue(np.array_equal(im_data, raw_image_data))

    def test_clicking_on_images_shows_position(self):
        x = 100
        y = 24
        ind = 0

        file_list = self.helper_load_fe_wire_files()
        self.model.set_current_image(ind)

        self.controller.process_mouse_left_clicked(x, y)
        self.assertEqual(x, int(self.widget.x_pos_pixel_lbl.text()))
        self.assertEqual(y, int(self.widget.y_pos_pixel_lbl.text()))

    def test_clicking_on_image_modifies_roi(self):
        x = 200
        y = 24
        ind = 0

        file_list = self.helper_load_fe_wire_files()
        self.model.set_current_image(ind)
        state = self.model.current_roi_data.T[x][y]

        self.controller.process_mouse_left_clicked(x, y)

        self.assertNotEqual(state, self.model.current_roi_data.T[x][y])

    def helper_load_fe_wire_files(self):
        fe_wire_data_path = os.path.join(data_path, 'Fe_Wire')
        file_list = sorted(glob.glob(os.path.join(fe_wire_data_path, 'FeWire_*.tif')))
        QtWidgets.QFileDialog.getOpenFileNames = MagicMock(return_value=file_list)
        click_button(self.main_widget.load_raw_data_files_btn)
        return file_list

    def helper_load_single_image_data(self, file_name):
        img_file = open(file_name, 'rb')
        im = Image.open(img_file)
        im_data = np.array(im)[::-1]

        im.close()
        img_file.close()
        return im_data
