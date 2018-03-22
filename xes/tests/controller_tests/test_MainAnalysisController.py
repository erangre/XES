# -*- coding: utf8 -*-
from mock import MagicMock
import os
import sys
import gc
import time
import glob

import numpy as np

from qtpy import QtWidgets, QtCore
from qtpy.QtTest import QTest

from ..ehook import excepthook
from ..utility import QtTest, unittest_data_path, enter_value_into_text_field, click_button
from ...model.XESModel import XESModel
from ...widgets.MainWidget import MainWidget

from ...controller.MainAnalysisController import MainAnalysisController

unittest_path = os.path.dirname(__file__)
data_path = os.path.join(unittest_path, os.pardir, 'data')


class TestMeasurementController(QtTest):
    def setUp(self):
        self.controller = MainAnalysisController()
        self.widget = self.controller.widget
        self.model = self.controller.model

    def tearDown(self):
        del self.controller
        gc.collect()

    def test_load_files_shows_correct_number_of_files(self):
        # sys.excepthook = excepthook
        file_list = self.helper_load_fe_wire_files()
        self.assertEqual(len(file_list), int(self.widget.num_files_lbl.text()))
        self.assertEqual(len(file_list), len(self.model.xes_spectra[-1].all_data))

    def test_load_files_finds_theta_values(self):
        file_list = self.helper_load_fe_wire_files()
        theta_values = np.linspace(66.935, 65.820, 201)
        found_theta_values = self.model.xes_spectra[-1].theta_values
        for theta, found_theta in zip(theta_values, found_theta_values):
            self.assertAlmostEqual(theta, found_theta, 3)
        print(self.model.xes_spectra[-1].all_data)
        self.fail()
        # sorted_theta_values = np.sort(theta_values)
        # sorted_found_theta_values = np.sort(found_theta_values)
        # # self.assertTrue(np.array_equal(np.sort(np.around(theta_values, 3)),
        # #                                np.sort(np.around(self.model.xes_spectra[-1].theta_values, 3))))
        # for theta, found_theta in zip(sorted_theta_values, sorted_found_theta_values):
        #     self.assertAlmostEqual(theta, found_theta, 3)

    def helper_load_fe_wire_files(self):
        fe_wire_data_path = os.path.join(data_path, 'Fe_Wire')
        file_list = sorted(glob.glob(os.path.join(fe_wire_data_path, 'FeWire_*.tif')))
        QtWidgets.QFileDialog.getOpenFileNames = MagicMock(return_value=file_list)
        click_button(self.widget.load_raw_data_files_btn)
        return file_list
