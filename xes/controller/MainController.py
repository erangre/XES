# -*- coding: utf8 -*-
import os
from sys import platform as _platform

from qtpy import QtWidgets, QtCore

from ..widgets.MainWidget import MainWidget
from .MeasurementController import MeasurementController
from .GraphController import GraphController
from .CalibrationController import CalibrationController
from ..model.XESModel import XESModel


class MainController(object):
    def __init__(self, use_settings=True):
        self.widget = MainWidget()
        self.model = XESModel()
        self.measurement_controller = MeasurementController(widget=self.widget, model=self.model)
        self.graph_controller = GraphController(widget=self.widget, model=self.model)
        self.calibration_controller = CalibrationController(widget=self.widget, model=self.model)
        self.setup_connections()
        if use_settings:
            self.xes_settings = QtCore.QSettings("XES", "XES_Settings")
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
        self.graph_controller.export_data_signal.connect(self.measurement_controller.export_data)
        self.graph_controller.normalization_changed_signal.connect(self.measurement_controller.update_graph_data)
        self.graph_controller.current_spectrum_changed_signal.connect(
            self.measurement_controller.current_spectrum_changed)
        self.widget.closeEvent = self.closeEvent
        self.widget.collection_tab_btn.clicked.connect(self.switch_tabs)
        self.widget.calibration_tab_btn.clicked.connect(self.switch_tabs)
        self.widget.epics_config_btn.clicked.connect(self.switch_tabs)

    def switch_tabs(self):
        if self.widget.collection_tab_btn.isChecked():
            self.widget.measurement_widget.setVisible(True)
            self.widget.calibration_widget.setVisible(False)
            # self.widget.epics_config_widget.setVisible(False)
        elif self.widget.calibration_tab_btn.isChecked():
            self.widget.measurement_widget.setVisible(False)
            self.widget.calibration_widget.setVisible(True)
            # self.widget.epics_config_widget.setVisible(False)
        elif self.widget.calibration_tab_btn.isChecked():
            self.widget.measurement_widget.setVisible(False)
            self.widget.calibration_widget.setVisible(False)
            # self.widget.epics_config_widget.setVisible(True)

    def load_settings(self):
        self.measurement_controller.load_settings(self.xes_settings)
        # self.calibration_controller.load_settings(self.xes_settings)
        # self.epics_controller.load_settings(self.xes_settings)

    def save_settings(self):
        self.measurement_controller.save_settings(self.xes_settings)
        # self.calibration_controller.save_settings(self.xes_settings)
        # self.epics_controller.save_settings(self.xes_settings)

    def closeEvent(self, event):
        self.save_settings()
        self.widget.close()
        event.accept()
