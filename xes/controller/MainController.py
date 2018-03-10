# -*- coding: utf8 -*-
import os
from sys import platform as _platform

from qtpy import QtWidgets, QtCore

from ..widgets.MainWidget import MainWidget
from .MeasurementController import MeasurementController
from .GraphController import GraphController
from ..model.XESModel import XESModel


class MainController(object):
    def __init__(self, use_settings=True):
        self.widget = MainWidget()
        self.model = XESModel()
        self.measurement_controller = MeasurementController(widget=self.widget, model=self.model)
        self.graph_controller = GraphController(widget=self.widget, model=self.model)
        self.setup_connections()

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
