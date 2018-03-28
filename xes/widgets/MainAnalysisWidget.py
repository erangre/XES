# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
# from .RawDataWidget import RawDataWidget
from .CalibrationWidget import CalibrationWidget
from .GraphWidget import GraphWidget
from .RawImageWidget import RawImageWidget


class MainAnalysisWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MainAnalysisWidget, self).__init__(*args, **kwargs)

        self.load_raw_data_files_btn = QtWidgets.QPushButton('Load Files')
        self.num_files_label_lbl = QtWidgets.QLabel('Number of files: ')
        self.num_files_lbl = QtWidgets.QLabel('0')

        self.raw_data_tab_btn = QtWidgets.QPushButton('Raw Data')
        self.calibration_tab_btn = QtWidgets.QPushButton('Calibration')
        self._tab_button_group = QtWidgets.QButtonGroup()

        self._tab_button_group.addButton(self.raw_data_tab_btn)
        self._tab_button_group.addButton(self.calibration_tab_btn)

        self._layout = QtWidgets.QVBoxLayout()

        self._files_layout = QtWidgets.QHBoxLayout()

        self._files_layout.addWidget(self.load_raw_data_files_btn)
        self._files_layout.addWidget(self.num_files_label_lbl)
        self._files_layout.addWidget(self.num_files_lbl)

        self._tab_layout = QtWidgets.QHBoxLayout()

        self._tab_layout.addWidget(self.raw_data_tab_btn)
        self._tab_layout.addWidget(self.calibration_tab_btn)

        self.graph_widget = GraphWidget()
        self.raw_image_widget = RawImageWidget()
        self.calibration_widget = CalibrationWidget()

        self._layout.addLayout(self._files_layout)
        self._layout.addWidget(self.graph_widget)
        self._layout.addLayout(self._tab_layout)
        self._layout.addWidget(self.raw_image_widget)
        self._layout.addWidget(self.calibration_widget)

        self.setLayout(self._layout)
        self.set_widget_properties()

    def set_widget_properties(self):
        self.calibration_widget.setVisible(False)
        self.raw_data_tab_btn.setCheckable(True)
        self.calibration_tab_btn.setCheckable(True)
        self.raw_data_tab_btn.setChecked(True)
        self.calibration_tab_btn.setChecked(False)
