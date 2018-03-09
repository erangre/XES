# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
from .MeasurementWidget import MeasurementWidget
from.GraphWidget import GraphWidget


class MainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self.collection_tab_btn = QtWidgets.QPushButton('Collection')
        self.calibration_tab_btn = QtWidgets.QPushButton('Calibration')
        self.epics_config_btn = QtWidgets.QPushButton('EPICS Config')

        self._layout = QtWidgets.QVBoxLayout()

        self._tab_layout = QtWidgets.QHBoxLayout()

        self._tab_layout.addWidget(self.collection_tab_btn)
        self._tab_layout.addWidget(self.calibration_tab_btn)
        self._tab_layout.addWidget(self.epics_config_btn)

        self.graph_widget = GraphWidget()
        self.measurement_widget = MeasurementWidget()

        self._layout.addWidget(self.graph_widget)
        self._layout.addLayout(self._tab_layout)
        self._layout.addWidget(self.measurement_widget)

        self.setLayout(self._layout)
        # TODO: add calibration and epics config widgets

        # self._calibration_layout = QtWidgets.QGridLayout()
        # self._epics_config_layout = QtWidgets.QGridLayout()
