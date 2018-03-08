# -*- coding: utf8 -*-
import os
from sys import platform as _platform

from qtpy import QtWidgets, QtCore

from ..widgets.MeasurementWidget import MeasurementWidget
from ..model.XESModel import XESModel


class MeasurementController(object):
    def __init__(self, widget, model):
        """
        :param widget:
        :type widget: MeasurementWidget
        :param model:
        :type model: XESModel
        """
        self.widget = widget
        self.model = model
        self.setup_connections()

    def setup_connections(self):
        self.widget.theta_start_le.editingFinished.connect(self.theta_values_changed)
        self.widget.theta_end_le.editingFinished.connect(self.theta_values_changed)
        self.widget.theta_step_le.editingFinished.connect(self.theta_values_changed)

    def theta_values_changed(self):
        try:
            theta_start = float(self.widget.theta_start_le.text())
            theta_end = float(self.widget.theta_end_le.text())
            theta_step = float(self.widget.theta_step_le.text())
        except ValueError:
            # TODO: Print msg about using float values
            return
        num_steps = round(abs((theta_end-theta_start)/theta_step))
        self.widget.num_steps_lbl.setText(str(num_steps))
        actual_theta_end = theta_start + num_steps*theta_step
        self.widget.theta_end_le.setText(str(actual_theta_end))

        ev_start = self.model.theta_to_ev(theta_start)
        ev_end = self.model.theta_to_ev(theta_end)
        ev_step = self.model.theta_step_to_ev_step(ev_start, theta_start, theta_step)
        self.widget.ev_start_le.setText(str(ev_start))
        self.widget.ev_end_le.setText(str(ev_end))
        self.widget.ev_step_le.setText(str(ev_step))
