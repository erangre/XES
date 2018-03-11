# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore


class CalibrationWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(CalibrationWidget, self).__init__(*args, **kwargs)
        self.slope_lbl = QtWidgets.QLabel('Slope: ')
        self.slope_le = QtWidgets.QLineEdit('')
        self.theta_zero_lbl = QtWidgets.QLabel('Theta 0: ')
        self.theta_zero_le = QtWidgets.QLineEdit('')
        self.roi_start_lbl = QtWidgets.QLabel('Roi Start: ')
        self.roi_start_sb = QtWidgets.QSpinBox()
        self.roi_width_lbl = QtWidgets.QLabel('Roi Width: ')
        self.roi_width_sb = QtWidgets.QSpinBox()
        self.roi_left_lbl = QtWidgets.QLabel('Roi Left: ')
        self.roi_left_sb = QtWidgets.QSpinBox()
        self.roi_range_lbl = QtWidgets.QLabel('Roi Range: ')
        self.roi_range_sb = QtWidgets.QSpinBox()

        self._layout = QtWidgets.QGridLayout()
        self._layout.addWidget(self.slope_lbl, 0, 0, 1, 1)
        self._layout.addWidget(self.slope_le, 0, 1, 1, 1)
        self._layout.addWidget(self.theta_zero_lbl, 0, 2, 1, 1)
        self._layout.addWidget(self.theta_zero_le, 0, 3, 1, 1)
        self._layout.addWidget(self.roi_start_lbl, 1, 0, 1, 1)
        self._layout.addWidget(self.roi_start_sb, 1, 1, 1, 1)
        self._layout.addWidget(self.roi_width_lbl, 1, 2, 1, 1)
        self._layout.addWidget(self.roi_width_sb, 1, 3, 1, 1)
        self._layout.addWidget(self.roi_left_lbl, 2, 0, 1, 1)
        self._layout.addWidget(self.roi_left_sb, 2, 1, 1, 1)
        self._layout.addWidget(self.roi_range_lbl, 2, 2, 1, 1)
        self._layout.addWidget(self.roi_range_sb, 2, 3, 1, 1)

        self.setLayout(self._layout)

        self.set_widget_properties()

    def set_widget_properties(self):
        self.theta_zero_le.setValidator(QtGui.QDoubleValidator())
        self.slope_le.setValidator(QtGui.QDoubleValidator())
