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
from ..model.XESSpectrum import XESSpectrum
from threading import Thread

from .epics_config import motor_pvs, detector_pvs, beam_pvs
from.utils import caput_pil, str3

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
        self.beam_data = {}
        self.beam_data['IC1'] = 0
        self.beam_data['IC2'] = 0
        self.beam_data['APS'] = 0
        self.beam_data_count = 0
        self.xes_spectra = []

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
        self.widget.theta_end_le.setText(str3(actual_theta_end))

        ev_start = self.model.theta_to_ev(theta_start)
        ev_end = self.model.theta_to_ev(theta_end)
        ev_step = self.model.theta_step_to_ev_step(ev_start, theta_start, theta_step)
        self.widget.ev_start_le.setText(str3(ev_start))
        self.widget.ev_end_le.setText(str3(ev_end))
        self.widget.ev_step_le.setText(str3(ev_step))
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
        self.widget.ev_end_le.setText(str3(actual_ev_end))

        theta_start = self.model.ev_to_theta(ev_start)
        theta_end = self.model.ev_to_theta(ev_end)
        theta_step = self.model.ev_step_to_theta_step(ev_start, theta_start, ev_step)
        self.widget.theta_start_le.setText(str3(theta_start))
        self.widget.theta_end_le.setText(str3(theta_end))
        self.widget.theta_step_le.setText(str3(theta_step))
        self.update_total_time('ev')

    def time_per_step_changed(self):
        self.update_total_time('time_per_step')

    def update_total_time(self, sender):
        num_steps = int(self.widget.num_steps_lbl.text())
        time_per_step = float(self.widget.time_per_step_le.text())
        num_repeats = int(self.widget.num_repeats_sb.value())
        total_time = num_steps * time_per_step * num_repeats
        self.widget.total_time_lbl.setText(str3(total_time))

    def num_repeats_changed(self):
        self.update_total_time('repeats')

    def start_collection_btn_clicked(self):
        self.xes_spectra.append(XESSpectrum())
        self.current_spectrum = self.xes_spectra[-1]
        self.toggle_measurement_buttons(False)
        self.widget.pause_collection_btn.setText("Pause")
        self.save_current_pv_values()
        theta_values, ev_values = self.prepare_theta_values()
        exp_time = float(self.widget.time_per_step_le.text())
        num_repeats = self.widget.num_repeats_sb.value()
        if theta_values is None:
            return

        self.current_spectrum.theta_values = list(theta_values)
        self.current_spectrum.num_repeats = num_repeats

        self.main_widget.graph_widget.add_empty_xes_spectrum_to_graph(theta_values, ev_values)

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
            ev_values = []
            theta_start = float(self.widget.theta_start_le.text())
            theta_end = float(self.widget.theta_end_le.text())
            num_steps = int(self.widget.num_steps_lbl.text())
            theta_values = np.linspace(theta_start, theta_end, num_steps)
            for theta_val in theta_values:
                ev_values.append(self.model.theta_to_ev(theta_val))
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
        return theta_values, ev_values

    def start_collection_on_thread(self, theta_values, exp_time, num_repeats):
        logger.info('Using the following Theta Values', theta_values)
        caput_pil(detector_pvs['exp_time'], exp_time, wait=True)
        caput_pil(detector_pvs['acquire_period'], exp_time + 0.002, wait=True)
        num_steps = len(theta_values)
        theta_reversed = False
        self.prepare_roi(theta_values[0])
        for ind in range(num_repeats):
            theta_ind = 0
            for theta in theta_values:
                self.clear_data_before_collecting()
                while self.collection_paused:
                    if self.collection_aborted:
                        break
                    time.sleep(0.1)
                if self.collection_aborted:
                    break
                roi_start = self.model.theta_to_roi(theta)[0]

                caput(motor_pvs['theta'], theta, wait=True)
                caput(detector_pvs['roi_start'], roi_start, wait=True)

                next_file_name = self.get_next_file_name()
                self.widget.update_current_values(theta, self.model.theta_to_ev(theta), next_file_name)
                QtWidgets.QApplication.processEvents()
                single_collection_thread = Thread(target=self.start_single_collection_on_sub_thread, kwargs={
                                       'exp_time': exp_time
                                   })
                single_collection_thread.start()
                while single_collection_thread.isAlive():
                    self.gather_data_while_collecting()
                    QtWidgets.QApplication.processEvents()
                    time.sleep(0.2)
                self.add_data_point(next_file_name, theta, theta_ind, exp_time, theta_reversed, num_steps)
                theta_ind += 1

            if self.collection_aborted:
                break
            theta_values = np.flipud(theta_values)
            theta_reversed = not theta_reversed
        self.collection_aborted = False
        self.collection_paused = False

    def start_single_collection_on_sub_thread(self, exp_time):
        caput(detector_pvs['acquire'], 1, wait=True, timeout=exp_time + 60.0)

    def prepare_roi(self, theta_start):
        caput(detector_pvs['roi_start'], self.model.theta_to_roi(theta_start)[0], wait=True)
        caput(detector_pvs['roi_width'], self.model.calibration['roi_width'], wait=True)
        caput(detector_pvs['roi_left'], self.model.calibration['roi_left'], wait=True)
        caput(detector_pvs['roi_range'], self.model.calibration['roi_range'], wait=True)

    def add_data_point(self, file_name, theta, theta_ind, exp_time, theta_reversed, num_steps):
        if theta_reversed:
            theta_ind = num_steps - theta_ind - 1
        counts = caget(detector_pvs['roi_total_counts'], as_string=False)
        ic1 = round(self.beam_data['IC1']/self.beam_data_count, 3)
        ic2 = round(self.beam_data['IC2']/self.beam_data_count, 3)
        aps_beam = round(self.beam_data['APS']/self.beam_data_count, 3)
        self.current_spectrum.add_data(file_name, theta_ind, round(theta, 3), counts, exp_time, time.asctime(),
                                       ic1, ic2, aps_beam)
        total_counts, total_exp_time = self.current_spectrum.gather_data_for_theta(theta_ind)

        self.main_widget.graph_widget.update_data_point(theta_ind, total_counts/total_exp_time)

    def gather_data_while_collecting(self):
        self.beam_data_count += 1
        for key in self.beam_data:
            try:
                self.beam_data[key] += caget(beam_pvs[key], as_string=False)
            except TypeError:
                pass

    def clear_data_before_collecting(self):
        self.beam_data_count = 0
        for key in self.beam_data:
            self.beam_data[key] = 0

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

    def export_data(self, filename):
        self.current_spectrum.export_data(filename)

    def update_graph_data(self, normalizer):
        normalized_counts = self.current_spectrum.normalize_data(normalizer)
        self.main_widget.graph_widget.update_graph_values(normalized_counts)

    def current_spectrum_changed(self, ind):
        self.current_spectrum = self.xes_spectra[ind]

    def load_settings(self, settings):
        theta_start = settings.value("theta_start", defaultValue=None)
        if theta_start is not None:
            self.widget.theta_start_le.setText(theta_start)
        theta_end = settings.value("theta_end", defaultValue=None)
        if theta_end is not None:
            self.widget.theta_end_le.setText(theta_end)
        theta_step = settings.value("theta_step", defaultValue=None)
        if theta_step is not None:
            self.widget.theta_step_le.setText(theta_step)
        time_per_step = settings.value("time_per_step", defaultValue=None)
        if time_per_step is not None:
            self.widget.time_per_step_le.setText(time_per_step)
        num_repeats = settings.value("num_repeats", defaultValue=None)
        if num_repeats is not None:
            self.widget.num_repeats_sb.setValue(int(num_repeats))
        export_data_directory = settings.value("export_data_directory", defaultValue=None)
        if export_data_directory is not None:
            self.model.current_directories['export_data_directory'] = export_data_directory
        export_image_directory = settings.value("export_image_directory", defaultValue=None)
        if export_image_directory is not None:
            self.model.current_directories['export_image_directory'] = export_image_directory
        self.theta_values_changed()

    def save_settings(self, settings):
        settings.setValue("theta_start", self.widget.theta_start_le.text())
        settings.setValue("theta_end", self.widget.theta_end_le.text())
        settings.setValue("theta_step", self.widget.theta_step_le.text())
        settings.setValue("time_per_step", self.widget.time_per_step_le.text())
        settings.setValue("num_repeats", str(self.widget.num_repeats_sb.value()))
        settings.setValue("export_data_directory", self.model.current_directories['export_data_directory'])
        settings.setValue("export_image_directory", self.model.current_directories['export_image_directory'])
