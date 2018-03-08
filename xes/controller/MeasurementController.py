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
        self.widget.ev_start_le.editingFinished.connect(self.ev_values_changed)
        self.widget.ev_end_le.editingFinished.connect(self.ev_values_changed)
        self.widget.ev_step_le.editingFinished.connect(self.ev_values_changed)
        self.widget.time_per_step_le.editingFinished.connect(self.time_per_step_changed)
        self.widget.num_repeats_sb.valueChanged.connect(self.num_repeats_changed)

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
        self.update_total_time('theta')

    def ev_values_changed(self):
        try:
            ev_start = float(self.widget.ev_start_le.text())
            ev_end = float(self.widget.ev_end_le.text())
            ev_step = float(self.widget.ev_step_le.text())
        except ValueError:
            # TODO: Print msg about using float values
            return
        num_steps = round(abs((ev_end-ev_start)/ev_step))
        self.widget.num_steps_lbl.setText(str(num_steps))
        actual_ev_end = ev_start + num_steps*ev_step
        self.widget.theta_end_le.setText(str(actual_ev_end))

        theta_start = self.model.ev_to_theta(ev_start)
        theta_end = self.model.ev_to_theta(ev_end)
        theta_step = self.model.ev_step_to_theta_step(ev_start, theta_start, ev_step)
        self.widget.theta_start_le.setText(str(theta_start))
        self.widget.theta_end_le.setText(str(theta_end))
        self.widget.theta_step_le.setText(str(theta_step))
        self.update_total_time('ev')

    def time_per_step_changed(self):
        self.update_total_time('time_per_step')

    def update_total_time(self, sender):
        num_steps = int(self.widget.num_steps_lbl.text())
        time_per_step = float(self.widget.time_per_step_le.text())
        num_repeats = int(self.widget.num_repeats_sb.value())
        total_time = num_steps * time_per_step * num_repeats
        self.widget.total_time_lbl.setText(str(total_time))

    def num_repeats_changed(self):
        self.update_total_time('repeats')
