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
    normalization_changed_signal = QtCore.Signal(str)

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
        self.widget.graph_normalize_list.currentIndexChanged.connect(self.graph_normalize_list_index_changed)
        self.widget.current_spectrum_sb.valueChanged.connect(self.current_spectrum_index_changed)

    def graph_export_data_btn_clicked(self):
        filename = save_file_dialog(
            self.widget, "Save XES Spectrum Data", self.model.current_directories['export_data_directory'],
            'Data (*.txt)')

        if filename is not '':
            self.model.current_directories['export_data_directory'] = os.path.dirname(filename)

            self.export_data_signal.emit(filename)

    def graph_export_image_btn_clicked(self):
        filename = save_file_dialog(
            self.widget, "Save XES Spectrum Image", self.model.current_directories['export_image_directory'],
            'PNG (*.png)')

        if filename is not '':
            self.model.current_directories['export_image_directory'] = os.path.dirname(filename)
            self.widget.export_graph(filename)

    def graph_normalize_list_index_changed(self, ind):
        # self.widget.normalizer = self.widget.graph_normalize_list.itemText(ind)
        self.normalization_changed_signal.emit(self.widget.graph_normalize_list.itemText(ind))

    def current_spectrum_index_changed(self, value):
        old_spectrum_index = self.widget.current_spectrum
        self.widget.current_spectrum = value - 1
        self.widget.xes_spectrum_plot.removeItem(self.widget.xes_spectra[old_spectrum_index])
        self.widget.xes_spectrum_plot.addItem(self.widget.xes_spectra[value - 1])
