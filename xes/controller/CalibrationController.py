# -*- coding: utf8 -*-
import os
from sys import platform as _platform
import logging
import time
import numpy as np
from epics import caput, caget

from qtpy import QtWidgets, QtCore

from ..widgets.MainWidget import MainWidget
from ..model.XESModel import XESModel

from .epics_config import motor_pvs, detector_pvs, beam_pvs
from.utils import caput_pil, str3


class CalibrationController(QtCore.QObject):
    def __init__(self, widget, model):
        """
        :param widget:
        :type widget: MainWidget
        :param model:
        :type model: XESModel
        """
        super(CalibrationController, self).__init__()
        self.main_widget = widget
        self.model = model
        self.widget = self.main_widget.calibration_widget
        self.setup_connections()

    def setup_connections(self):
        self.widget.theta_zero_le.editingFinished.connect(self.theta_zero_edit_finished)
        self.widget.slope_le.editingFinished.connect(self.slope_edit_finished)
        self.widget.roi_left_sb.valueChanged.connect(self.roi_left_value_changed)
        self.widget.roi_range_sb.valueChanged.connect(self.roi_range_value_changed)
        self.widget.roi_start_sb.valueChanged.connect(self.roi_start_value_changed)
        self.widget.roi_width_sb.valueChanged.connect(self.roi_width_value_changed)

    def theta_zero_edit_finished(self):
        self.model.calibration['theta_0'] = float(self.widget.theta_zero_le.text())

    def slope_edit_finished(self):
        self.model.calibration['slope'] = float(self.widget.slope_le.text())

    def roi_left_value_changed(self):
        self.model.calibration['roi_left'] = self.widget.roi_left_sb.value()

    def roi_range_value_changed(self):
        self.model.calibration['roi_range'] = self.widget.roi_range_sb.value()

    def roi_start_value_changed(self):
        self.model.calibration['roi_start'] = self.widget.roi_start_sb.value()

    def roi_width_value_changed(self):
        self.model.calibration['roi_width'] = self.widget.roi_width_sb.value()

    def load_settings(self, settings):
        theta_zero = settings.value("theta_zero", defaultValue=None)
        if theta_zero is not None:
            self.widget.theta_zero_le.setText(theta_zero)
        slope = settings.value("slope", defaultValue=None)
        if slope is not None:
            self.widget.slope_le.setText(slope)
        roi_start = settings.value("roi_start", defaultValue=None)
        if roi_start is not None:
            self.widget.roi_start_sb.setValue(int(roi_start))
        roi_width = settings.value("roi_width", defaultValue=None)
        if roi_width is not None:
            self.widget.roi_width_sb.setValue(int(roi_width))
        roi_left = settings.value("roi_left", defaultValue=None)
        if roi_left is not None:
            self.widget.roi_left_sb.setValue(int(roi_left))
        roi_range = settings.value("roi_range", defaultValue=None)
        if roi_range is not None:
            self.widget.roi_range_sb.setValue(int(roi_range))

    def save_settings(self, settings):
        settings.setValue("theta_zero", self.widget.theta_zero_le.text())
        settings.setValue("slope", self.widget.slope_le.text())
        settings.setValue("roi_start", str(self.widget.roi_start_sb.value()))
        settings.setValue("roi_width", str(self.widget.roi_width_sb.value()))
        settings.setValue("roi_left", str(self.widget.roi_left_sb.value()))
        settings.setValue("roi_range", str(self.widget.roi_range_sb.value()))
