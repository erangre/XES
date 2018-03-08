# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore


class MeasurementWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MeasurementWidget, self).__init__(*args, **kwargs)

        self.all_widgets = []

        self.theta_start_le = self._add_line_edit('66.18')
        self.theta_end_le = self._add_line_edit('66.4')
        self.theta_step_le = self._add_line_edit('0.0183')
        self.num_steps_lbl = QtWidgets.QLabel('12')
        self.ev_start_le = self._add_line_edit('7050')
        self.ev_end_le = self._add_line_edit('7150')
        self.ev_step_le = self._add_line_edit('2')
        self.time_per_step_le = self._add_line_edit('11.5')
        self.total_time_lbl = QtWidgets.QLabel('135.2')
        self.num_repeats_sb = self._add_spin_box()
        self.start_collection_btn = QtWidgets.QPushButton('Start')
        self.abort_collection_btn = QtWidgets.QPushButton('Abort')

        self.equal_unit_widget = QtWidgets.QWidget()
        self.equal_theta_unit_rb = QtWidgets.QRadioButton('Theta (deg)')
        self.equal_ev_unit_rb = QtWidgets.QRadioButton('Energy (eV)')

        self._set_widget_properties()

        self._create_layout()

    def _add_line_edit(self, default_text):
        new_widget = QtWidgets.QLineEdit(default_text)
        self.all_widgets.append(new_widget)
        return new_widget

    def _add_spin_box(self):
        new_widget = QtWidgets.QSpinBox()
        self.all_widgets.append(new_widget)
        return new_widget

    def _set_widget_properties(self):
        self.theta_start_le.setValidator(QtGui.QDoubleValidator())
        self.theta_end_le.setValidator(QtGui.QDoubleValidator())
        self.theta_step_le.setValidator(QtGui.QDoubleValidator())
        self.ev_start_le.setValidator(QtGui.QDoubleValidator())
        self.ev_end_le.setValidator(QtGui.QDoubleValidator())
        self.ev_step_le.setValidator(QtGui.QDoubleValidator())
        self.time_per_step_le.setValidator(QtGui.QDoubleValidator())
        self.num_repeats_sb.setMinimum(1)
        self.num_repeats_sb.setSingleStep(1)
        self.num_repeats_sb.setValue(2)
        self.abort_collection_btn.setVisible(False)
        self.abort_collection_btn.setEnabled(False)
        self.equal_theta_unit_rb.setChecked(True)

    def _create_layout(self):
        self._layout = QtWidgets.QVBoxLayout()

        self._equal_unit_layout = QtWidgets.QHBoxLayout()

        self._equal_unit_layout.addWidget(self.equal_theta_unit_rb)
        self._equal_unit_layout.addWidget(self.equal_ev_unit_rb)
        self.equal_unit_widget.setLayout(self._equal_unit_layout)
