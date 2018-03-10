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
from ..widgets.UtilityWidgets import save_file_dialog
from threading import Thread

from .epics_config import motor_pvs, detector_pvs, beam_pvs
from.utils import caput_pil, str3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GraphController(QtCore.QObject):
    export_data_signal = QtCore.Signal(str)

    def __init__(self, widget, model):
        """
        :param widget:
        :type widget: MainWidget
        :param model:
        :type model: XESModel
        """
        super(GraphController, self).__init__()
        self.main_widget = widget
        self.model = model
        self.widget = self.main_widget.graph_widget
        self.setup_connections()

    def setup_connections(self):
        self.widget.graph_export_data_btn.clicked.connect(self.graph_export_data_btn_clicked)
        self.widget.graph_export_image_btn.clicked.connect(self.graph_export_image_btn_clicked)

    def graph_export_data_btn_clicked(self):
        filename = save_file_dialog(
            self.widget, "Save XES Spectrum Data", os.getcwd(), 'Data (*.txt)')

        if filename is not '':
            self.export_data_signal.emit(filename)

    def graph_export_image_btn_clicked(self):
        filename = save_file_dialog(
            self.widget, "Save XES Spectrum Image", os.getcwd(), 'PNG (*.png)')

        if filename is not '':
            self.widget.export_graph(filename)
