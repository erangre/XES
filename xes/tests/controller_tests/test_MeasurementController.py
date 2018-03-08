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

    def test_set_theta_values_updates_num_steps(self):
        # sys.excepthook = excepthook
        num_steps = 20
        self.helper_input_theta_values(num_steps=num_steps)
        calc_steps = self.measure_controller.widget.num_steps_lbl.text()
        self.assertEqual(num_steps, int(calc_steps))
        self.fail()

    def test_set_theta_values_updates_theta_end(self):
        end_theta = 66.9
        start_theta, theta_step, end_theta, num_steps = self.helper_input_theta_values(end_theta=end_theta)
        self.assertAlmostEqual(end_theta, float(self.measure_controller.widget.theta_end_le.text()), 1)

    def test_set_theta_values_updates_ev_values(self):
        start_theta, theta_step, end_theta, num_steps = self.helper_input_theta_values()
        start_ev = float(self.measure_controller.widget.ev_start_le.text())
        end_ev = float(self.measure_controller.widget.ev_end_le.text())
        ev_step = float(self.measure_controller.widget.ev_step_le.text())
        self.assertAlmostEqual(start_ev, self.model.theta_to_ev(start_theta), 5)
        self.assertAlmostEqual(end_ev, self.model.theta_to_ev(end_theta), 5)
        self.assertAlmostEqual(ev_step, self.model.theta_step_to_ev_step(start_ev, start_theta, theta_step), 5)

    def helper_input_theta_values(self, start_theta=66.18, num_steps=20, theta_step=0.0183, end_theta=None):
        if end_theta is None:
            end_theta = start_theta + num_steps*theta_step
        enter_value_into_text_field(self.measure_controller.widget.theta_start_le, start_theta)
        enter_value_into_text_field(self.measure_controller.widget.theta_end_le, end_theta)
        enter_value_into_text_field(self.measure_controller.widget.theta_step_le, theta_step)
        return start_theta, theta_step, end_theta, num_steps
