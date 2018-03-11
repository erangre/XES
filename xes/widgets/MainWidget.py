# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
from .MeasurementWidget import MeasurementWidget
from .CalibrationWidget import CalibrationWidget
from.GraphWidget import GraphWidget


class MainWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)

        self.collection_tab_btn = QtWidgets.QPushButton('Collection')
        self.calibration_tab_btn = QtWidgets.QPushButton('Calibration')
        self.epics_config_btn = QtWidgets.QPushButton('EPICS Config')
        self._tab_button_group = QtWidgets.QButtonGroup()

        self._tab_button_group.addButton(self.collection_tab_btn)
        self._tab_button_group.addButton(self.calibration_tab_btn)
        self._tab_button_group.addButton(self.epics_config_btn)

        self._layout = QtWidgets.QVBoxLayout()

        self._tab_layout = QtWidgets.QHBoxLayout()

        self._tab_layout.addWidget(self.collection_tab_btn)
        self._tab_layout.addWidget(self.calibration_tab_btn)
        self._tab_layout.addWidget(self.epics_config_btn)

        self.graph_widget = GraphWidget()
        self.measurement_widget = MeasurementWidget()
        self.calibration_widget = CalibrationWidget()

        self._layout.addWidget(self.graph_widget)
        self._layout.addLayout(self._tab_layout)
        self._layout.addWidget(self.measurement_widget)
        self._layout.addWidget(self.calibration_widget)

        self.setLayout(self._layout)
        self.set_widget_properties()
        # TODO: add pics config widgets

        # self._epics_config_layout = QtWidgets.QGridLayout()

    def set_widget_properties(self):
        self.calibration_widget.setVisible(False)
        self.collection_tab_btn.setCheckable(True)
        self.calibration_tab_btn.setCheckable(True)
        self.epics_config_btn.setCheckable(True)
        self.collection_tab_btn.setChecked(True)
        self.calibration_tab_btn.setChecked(False)
        self.epics_config_btn.setChecked(False)
