# -*- coding: utf8 -*-
import os
from sys import platform as _platform

from qtpy import QtWidgets, QtCore

from ..widgets.MainAnalysisWidget import MainAnalysisWidget
from ..widgets.UtilityWidgets import open_files_dialog
from .GraphController import GraphController
from .CalibrationController import CalibrationController
from .RawImageController import RawImageController

from ..model.XESModel import XESModel
from ..model.XESSpectrum import XESSpectrum


class MainAnalysisController(object):
    def __init__(self, use_settings=True):
        self.widget = MainAnalysisWidget()
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
            self.model.open_files(ind=-1, file_names=file_names)
            self.model.add_data_set_to_spectrum(ind=-1)
            self.populate_raw_image_list(file_names)

            self.widget.raw_image_widget.img_view.activate_mask()
            self.model.set_current_image(0)

    def populate_raw_image_list(self, file_names):
        all_theta_values = self.model.current_spectrum.get_data(column='theta')
        ev_values = []
        for theta in all_theta_values:
            ev_values.append(self.model.theta_to_ev(theta))
        self.widget.raw_image_widget.update_raw_image_list(file_names, ev_values)

    def image_changed(self):
        self.widget.raw_image_widget.load_image(self.model.im_data)
        self.widget.raw_image_widget.img_view.set_color([0, 255, 0, 100])
        self.widget.raw_image_widget.img_view.plot_mask(self.model.current_roi_data)

    def load_settings(self):
        self.calibration_controller.load_settings(self.xes_settings)

    def save_settings(self):
        self.calibration_controller.save_settings(self.xes_settings)

    def closeEvent(self, event):
        self.save_settings()
        self.widget.close()
        event.accept()
