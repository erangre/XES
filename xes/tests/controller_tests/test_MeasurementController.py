# -*- coding: utf8 -*-
from mock import MagicMock
import os
import sys
import gc
import time

import numpy as np

from qtpy import QtWidgets, QtCore
from qtpy.QtTest import QTest

from ..ehook import excepthook
from ..utility import QtTest, unittest_data_path, enter_value_into_text_field
from ...model.XESModel import XESModel
from ...widgets.MeasurementWidget import MeasurementWidget

from ...controller.MeasurementController import MeasurementController


class TestMeasurementController(QtTest):
    def setUp(self):
        self.model = XESModel()
        self.measure_widget = MeasurementWidget()
        self.measure_controller = MeasurementController(widget=self.measure_widget, model=self.model)

    def tearDown(self):
        del self.model
        del self.measure_widget
        del self.measure_controller
        gc.collect()

    def test_set_theta_values(self):
        # sys.excepthook = excepthook
        start_theta = 66.18
        num_steps = 20.0
        theta_step = 0.0183
        end_theta = start_theta + num_steps*theta_step
        enter_value_into_text_field(self.measure_controller.widget.theta_start_le, start_theta)
        enter_value_into_text_field(self.measure_controller.widget.theta_end_le, end_theta)
        enter_value_into_text_field(self.measure_controller.widget.theta_step_le, theta_step)
        QtWidgets.QApplication.processEvents()

        calc_steps = self.measure_controller.widget.num_steps_lbl.text()
        self.assertEqual(num_steps, int(calc_steps))
