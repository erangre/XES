# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore


class MeasurementWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MeasurementWidget, self).__init__(*args, **kwargs)

        self.theta_start_le = QtWidgets.QLineEdit('66.18')
        self.theta_end_le = QtWidgets.QLineEdit('66.4')
        self.theta_step_le = QtWidgets.QLineEdit('0.0183')
        self.num_steps_lbl = QtWidgets.QLabel('12')
        self.ev_start_le = QtWidgets.QLineEdit('7050')
        self.ev_end_le = QtWidgets.QLineEdit('7150')
        self.ev_step_le = QtWidgets.QLineEdit('2')

        self.set_widget_properties()

    def set_widget_properties(self):
        self.theta_start_le.setValidator(QtGui.QDoubleValidator())
        self.theta_end_le.setValidator(QtGui.QDoubleValidator())
        self.theta_step_le.setValidator(QtGui.QDoubleValidator())
