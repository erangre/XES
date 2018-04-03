# -*- coding: utf8 -*-
import os
from sys import platform as _platform

from qtpy import QtWidgets, QtCore

from ..widgets.MainAnalysisWidget import MainAnalysisWidget, ManualFileInfoDialog
from ..widgets.UtilityWidgets import open_files_dialog
from .GraphController import GraphController
from .CalibrationController import CalibrationController
from .RawImageController import RawImageController

from ..model.XESModel import XESModel
from ..model.XESSpectrum import XESSpectrum


class MainAnalysisController(object):
    def __init__(self, use_settings=True):
        self.widget = MainAnalysisWidget()
        self.manual_file_info_dialog = ManualFileInfoDialog(self.widget)
        self.model = XESModel()
        self.graph_controller = GraphController(widget=self.widget, model=self.model)
        self.calibration_controller = CalibrationController(widget=self.widget, model=self.model)
        self.raw_image_controller = RawImageController(widget=self.widget, model=self.model)
        self.setup_connections()

        self.current_spectrum = None

        if use_settings:
            self.xes_settings = QtCore.QSettings("XES", "XES_Analysis_Settings")
            self.load_settings()

    def show_window(self):
        """
        Displays the main window on the screen and makes it active.
        """
        self.widget.show()

        if _platform == "darwin":
            self.widget.setWindowState(self.widget.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.widget.activateWindow()
            self.widget.raise_()

    def setup_connections(self):
        self.widget.closeEvent = self.closeEvent
        self.widget.load_raw_data_files_btn.clicked.connect(self.load_raw_data_files_clicked)
        self.widget.raw_data_tab_btn.clicked.connect(self.switch_tabs)
        self.widget.calibration_tab_btn.clicked.connect(self.switch_tabs)
        self.model.image_changed.connect(self.image_changed)
        self.raw_image_controller.roi_changed.connect(self.update_graph_data)
        self.graph_controller.export_data_signal.connect(self.export_data)
        self.manual_file_info_dialog.read_list_btn.clicked.connect(self.manual_read_list_btn_clicked)
        self.manual_file_info_dialog.start_energy_le.editingFinished.connect(self.manual_file_info_num_points_changed)
        self.manual_file_info_dialog.end_energy_le.editingFinished.connect(self.manual_file_info_num_points_changed)
        self.manual_file_info_dialog.energy_step_le.editingFinished.connect(self.manual_file_info_num_points_changed)
        self.manual_file_info_dialog.num_repeats_le.editingFinished.connect(self.manual_file_info_num_points_changed)
        self.model.manual_file_info_mode.connect(self.manual_file_info_mode_enabled)

    def switch_tabs(self):
        if self.widget.raw_data_tab_btn.isChecked():
            self.widget.raw_image_widget.setVisible(True)
            self.widget.calibration_widget.setVisible(False)
        elif self.widget.calibration_tab_btn.isChecked():
            self.widget.raw_image_widget.setVisible(False)
            self.widget.calibration_widget.setVisible(True)

    def load_raw_data_files_clicked(self):
        self.load_files()

    def load_files(self, *args, **kwargs):
        filename = kwargs.get('filename', None)
        if filename is None:
            file_names = open_files_dialog(self.widget, "Load raw image data files",
                                           self.model.current_directories['raw_image_directory'])
        else:
            file_names = [filename]

        if file_names is not None and len(file_names) is not 0:
            self.widget.num_files_lbl.setText(str(len(file_names)))
            self.model.xes_spectra.append(XESSpectrum())
            self.current_spectrum = self.model.xes_spectra[-1]
            theta_values, ev_values = self.model.open_files(ind=-1, file_names=file_names)
            self.model.prepare_all_rois()
            self.model.add_data_set_to_spectrum(ind=-1,
                                                use_bg_roi=self.widget.raw_image_widget.use_bg_roi_cb.isChecked())
            self.populate_raw_image_list(file_names)
            self.widget.graph_widget.add_empty_xes_spectrum_to_graph(theta_values, ev_values)

            self.widget.raw_image_widget.img_view.activate_mask()
            self.widget.raw_image_widget.img_view.activate_mask_b()
            self.model.set_current_image(0)
            self.update_graph_data()

    def populate_raw_image_list(self, file_names):
        all_theta_values = self.model.current_spectrum.get_data(column='theta')
        ev_values = []
        for theta in all_theta_values:
            ev_values.append(self.model.theta_to_ev(theta))
        self.widget.raw_image_widget.update_raw_image_list(file_names, ev_values)

    def update_graph_data(self, normalizer='Raw'):
        self.model.recalc_all_counts(use_bg_roi=self.widget.raw_image_widget.use_bg_roi_cb.isChecked())
        normalized_counts = self.current_spectrum.normalize_data(normalizer)
        self.widget.graph_widget.update_graph_values(normalized_counts)

    def image_changed(self):
        self.widget.raw_image_widget.load_image(self.model.im_data)
        self.widget.raw_image_widget.img_view.set_color([0, 255, 0, 100])
        self.widget.raw_image_widget.img_view.set_color_b([255, 0, 0, 100])

        self.widget.raw_image_widget.img_view.plot_mask(self.model.current_roi_data)
        self.widget.raw_image_widget.img_view.plot_mask_b(self.model.current_bg_roi_data)

    def export_data(self, filename):
        self.model.xes_spectra[self.model.current_spectrum_ind].export_data(filename)

    def manual_file_info_mode_enabled(self, file_names):
        self.manual_file_info_dialog.file_names = file_names
        self.manual_file_info_dialog.exec_()
        if self.manual_file_info_dialog.approved:
            manual_settings = {}
            manual_settings['start_energy'] = self.manual_file_info_dialog.start_energy
            manual_settings['end_energy'] = self.manual_file_info_dialog.end_energy
            manual_settings['num_steps'] = (self.manual_file_info_dialog.end_energy -
                                            self.manual_file_info_dialog.start_energy)/(
                self.manual_file_info_dialog.energy_step)
            manual_settings['num_repeats'] = self.manual_file_info_dialog.num_repeats
            manual_settings['exp_time'] = self.manual_file_info_dialog.exp_time
            self.model.manual_get_all_files_info(file_names, manual_settings)

    def manual_read_list_btn_clicked(self):
        self.manual_file_info_dialog.selected_files.clear()
        for item in self.manual_file_info_dialog.file_names:
            self.manual_file_info_dialog.selected_files.addItem(QtWidgets.QListWidgetItem(item))
        self.manual_file_info_dialog.total_files_lbl.setText(
            str(self.manual_file_info_dialog.selected_files.count()) + ' files')
        self.manual_file_info_check_num_points()

    def manual_file_info_num_points_changed(self):
        try:
            start_energy = float(self.manual_file_info_dialog.start_energy_le.text())
            end_energy = float(self.manual_file_info_dialog.end_energy_le.text())
            energy_step = float(self.manual_file_info_dialog.energy_step_le.text())
            num_repeats = int(self.manual_file_info_dialog.num_repeats_le.text())
            num_steps = int((end_energy - start_energy) / energy_step) + 1
            num_defined = num_steps * num_repeats

            self.manual_file_info_dialog.num_step_lbl.setText(str(num_steps))
            self.manual_file_info_dialog.num_expected_files_lbl.setText(str(num_defined))
        except ValueError:
            self.manual_file_info_dialog.num_expected_files_lbl.setText('0 Expected Files')
        self.manual_file_info_check_num_points()

    def manual_file_info_check_num_points(self):
        try:
            start_energy = float(self.manual_file_info_dialog.start_energy_le.text())
            end_energy = float(self.manual_file_info_dialog.end_energy_le.text())
            energy_step = float(self.manual_file_info_dialog.energy_step_le.text())
            num_repeats = int(self.manual_file_info_dialog.num_repeats_le.text())
            num_defined = (int((end_energy - start_energy)/energy_step) + 1) * num_repeats

            num_in_list = self.manual_file_info_dialog.selected_files.count()

        except ValueError:
            self.manual_file_info_dialog.ok_btn.setEnabled(False)
            return

        self.manual_file_info_dialog.ok_btn.setEnabled(num_defined == num_in_list)

    def load_settings(self):
        self.calibration_controller.load_settings(self.xes_settings)

    def save_settings(self):
        self.calibration_controller.save_settings(self.xes_settings)

    def closeEvent(self, event):
        self.save_settings()
        self.widget.close()
        event.accept()
