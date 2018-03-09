# -*- coding: utf8 -*-
import os
from sys import platform as _platform
import logging
import time
import numpy as np
from epics import caput, caget

from qtpy import QtWidgets, QtCore

from ..widgets.MainWidget import MainWidget
from ..widgets.MeasurementWidget import MeasurementWidget
from ..model.XESModel import XESModel
from threading import Thread

from .epics_config import motor_pvs, detector_pvs
from.utils import caput_pil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MeasurementController(QtCore.QObject):
    def __init__(self, widget, model):
        """
        :param widget:
        :type widget: MainWidget
        :param model:
        :type model: XESModel
        """
        super(MeasurementController, self).__init__()

        self.main_widget = widget
        self.widget = widget.measurement_widget
        self.model = model
        self.collection_aborted = False
        self.collection_paused = False
        self.old_pv_values = {}
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
        self.widget.start_collection_btn.clicked.connect(self.start_collection_btn_clicked)
        self.widget.abort_collection_btn.clicked.connect(self.abort_collection_btn_clicked)
        self.widget.pause_collection_btn.clicked.connect(self.pause_collection_btn_clicked)

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
        self.widget.ev_end_le.setText(str(actual_ev_end))

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

    def start_collection_btn_clicked(self):
        self.toggle_measurement_buttons(False)
        self.widget.pause_collection_btn.setText("Pause")
        self.save_current_pv_values()
        theta_values = self.prepare_theta_values()
        exp_time = float(self.widget.time_per_step_le.text())
        num_repeats = self.widget.num_repeats_sb.value()
        if theta_values is None:
            return

        collection_thread = Thread(target=self.start_collection_on_thread,
                                   kwargs={
                                       'theta_values': theta_values,
                                       'exp_time': exp_time,
                                       'num_repeats': num_repeats,
                                   })
        collection_thread.start()
        while collection_thread.isAlive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.1)

        self.restore_old_pv_values()
        self.toggle_measurement_buttons(True)

    def prepare_theta_values(self):
        if self.widget.equal_theta_unit_rb.isChecked():
            theta_start = float(self.widget.theta_start_le.text())
            theta_end = float(self.widget.theta_end_le.text())
            num_steps = int(self.widget.num_steps_lbl.text())
            theta_values = np.linspace(theta_start, theta_end, num_steps)
        elif self.widget.equal_ev_unit_rb.isChecked():
            theta_values = []
            ev_start = float(self.widget.ev_start_le.text())
            ev_end = float(self.widget.ev_end_le.text())
            num_steps = int(self.widget.num_steps_lbl.text())
            ev_values = np.linspace(ev_start, ev_end, num_steps)
            for ev_val in ev_values:
                theta_values.append(self.model.ev_to_theta(ev_val))
        else:
            theta_values = None
        return theta_values

    def start_collection_on_thread(self, theta_values, exp_time, num_repeats):
        logger.info('Using the following Theta Values', theta_values)
        caput_pil(detector_pvs['exp_time'], exp_time, wait=True)
        caput_pil(detector_pvs['acquire_period'], exp_time + 0.002, wait=True)
        for ind in range(num_repeats):
            for theta in theta_values:
                while self.collection_paused:
                    if self.collection_aborted:
                        break
                    time.sleep(0.1)
                if self.collection_aborted:
                    break
                caput(motor_pvs['theta'], str(theta))
                next_file_name = self.get_next_file_name()
                self.widget.update_current_values(theta, self.model.theta_to_ev(theta), next_file_name)
                QtWidgets.QApplication.processEvents()
                caput(detector_pvs['acquire'], 1, wait=True, timeout=exp_time+60.0)
            if self.collection_aborted:
                break
            theta_values = np.flipud(theta_values)
        self.collection_aborted = False
        self.collection_paused = False

    @staticmethod
    def get_next_file_name():
        base_name = caget(detector_pvs['TIFF_base_name'], as_string=True)
        next_number = caget(detector_pvs['TIFF_next_number'], as_string=True)
        next_file_name = ''.join([base_name, next_number])
        return next_file_name

    def toggle_measurement_buttons(self, toggle):
        self.widget.num_repeats_sb.setEnabled(toggle)
        for widget_item in self.widget.all_widgets:
            widget_item.setEnabled(toggle)
        self.widget.start_collection_btn.setVisible(toggle)
        self.widget.start_collection_btn.setEnabled(toggle)
        self.widget.abort_collection_btn.setVisible(not toggle)
        self.widget.abort_collection_btn.setEnabled(not toggle)
        self.widget.pause_collection_btn.setVisible(not toggle)
        self.widget.pause_collection_btn.setEnabled(not toggle)

    def save_current_pv_values(self):
        self.old_pv_values = {}
        self.old_pv_values[motor_pvs['theta']] = caget(motor_pvs['theta'])

    def restore_old_pv_values(self):
        for pv in self.old_pv_values:
            caput(pv, self.old_pv_values[pv], wait=True)

    def abort_collection_btn_clicked(self):
        self.collection_aborted = True

    def pause_collection_btn_clicked(self):
        self.collection_paused = not self.collection_paused
        if self.collection_paused:
            self.widget.pause_collection_btn.setText('Resume')
        else:
            self.widget.pause_collection_btn.setText('Pause')
