# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore


class MeasurementWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(MeasurementWidget, self).__init__(*args, **kwargs)

        self.all_widgets = []

        self.file_dir_lbl = QtWidgets.QLabel('Folder: ')
        self.file_dir_le = self._add_line_edit('/DAC/')
        self.file_name_lbl = QtWidgets.QLabel('File: ')
        self.file_name_le = self._add_line_edit('')
        self.start_number_lbl = QtWidgets.QLabel('#: ')
        self.start_number_le = self._add_line_edit('1')

        self.theta_lbl = QtWidgets.QLabel('Theta (deg): ')
        self.ev_lbl = QtWidgets.QLabel('Energy (eV): ')
        self.start_lbl = QtWidgets.QLabel('Start')
        self.end_lbl = QtWidgets.QLabel('End')
        self.step_lbl = QtWidgets.QLabel('Step')

        self.time_per_step_lbl = QtWidgets.QLabel('Time per step (sec): ')
        self.num_points_label_lbl = QtWidgets.QLabel('# of points: ')
        self.num_repeats_lbl = QtWidgets.QLabel('# of repeats: ')
        self.total_time_label_lbl = QtWidgets.QLabel('Total time (sec): ')

        self.theta_start_le = self._add_line_edit('66.18')
        self.theta_end_le = self._add_line_edit('66.4')
        self.theta_step_le = self._add_line_edit('0.0183')
        self.num_steps_lbl = QtWidgets.QLabel('12')
        self.ev_start_le = self._add_line_edit('7050')
        self.ev_end_le = self._add_line_edit('7150')
        self.ev_step_le = self._add_line_edit('2')
        self.go_to_7058_btn = QtWidgets.QPushButton('Go to 7058')
        self.time_per_step_le = self._add_line_edit('1.5')
        self.total_time_lbl = QtWidgets.QLabel('135.2')
        self.num_repeats_sb = self._add_spin_box()
        self.start_collection_btn = QtWidgets.QPushButton('Start')
        self.abort_collection_btn = QtWidgets.QPushButton('Abort')
        self.pause_collection_btn = QtWidgets.QPushButton('Pause')

        self.equal_unit_widget = QtWidgets.QWidget()
        self.equal_theta_unit_rb = QtWidgets.QRadioButton('Theta (deg)')
        self.equal_ev_unit_rb = QtWidgets.QRadioButton('Energy (eV)')

        self.current_theta_label_lbl = QtWidgets.QLabel('Current Theta (deg): ')
        self.current_theta_lbl = QtWidgets.QLabel('')
        self.current_energy_label_lbl = QtWidgets.QLabel('Current Energy (eV): ')
        self.current_energy_lbl = QtWidgets.QLabel('')
        self.next_file_label_lbl = QtWidgets.QLabel('Next File: ')
        self.next_file_lbl = QtWidgets.QLabel('')

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
        self.num_repeats_sb.setValue(4)
        self.abort_collection_btn.setVisible(False)
        self.abort_collection_btn.setEnabled(False)
        self.equal_theta_unit_rb.setChecked(True)
        self.pause_collection_btn.setVisible(False)
        self.pause_collection_btn.setEnabled(False)
        self.all_widgets.append(self.go_to_7058_btn)

    def _create_layout(self):
        self._measurement_layout = QtWidgets.QGridLayout()

        self._equal_unit_layout = QtWidgets.QHBoxLayout()
        self._equal_unit_layout.addWidget(self.equal_theta_unit_rb)
        self._equal_unit_layout.addWidget(self.equal_ev_unit_rb)
        self.equal_unit_widget.setLayout(self._equal_unit_layout)

        self._measurement_layout.addWidget(self.file_dir_lbl, 1, 0, 1, 1)
        self._measurement_layout.addWidget(self.file_dir_le, 1, 1, 1, 1)
        self._measurement_layout.addWidget(self.file_name_lbl, 1, 2, 1, 1)
        self._measurement_layout.addWidget(self.file_name_le, 1, 3, 1, 1)
        self._measurement_layout.addWidget(self.start_number_lbl, 1, 4, 1, 1)
        self._measurement_layout.addWidget(self.start_number_le, 1, 5, 1, 1)
        self._measurement_layout.addWidget(self.start_lbl, 2, 4, 1, 1)
        self._measurement_layout.addWidget(self.end_lbl, 2, 5, 1, 1)
        self._measurement_layout.addWidget(self.step_lbl, 2, 6, 1, 1)
        self._measurement_layout.addWidget(self.equal_unit_widget, 3, 0, 1, 2)
        self._measurement_layout.addWidget(self.theta_lbl, 3, 3, 1, 1)
        self._measurement_layout.addWidget(self.theta_start_le, 3, 4, 1, 1)
        self._measurement_layout.addWidget(self.theta_end_le, 3, 5, 1, 1)
        self._measurement_layout.addWidget(self.theta_step_le, 3, 6, 1, 1)
        self._measurement_layout.addWidget(self.ev_lbl, 4, 3, 1, 1)
        self._measurement_layout.addWidget(self.ev_start_le, 4, 4, 1, 1)
        self._measurement_layout.addWidget(self.ev_end_le, 4, 5, 1, 1)
        self._measurement_layout.addWidget(self.ev_step_le, 4, 6, 1, 1)
        self._measurement_layout.addWidget(self.go_to_7058_btn, 4, 7, 1, 1)
        self._measurement_layout.addWidget(self.time_per_step_lbl, 5, 0, 1, 1)
        self._measurement_layout.addWidget(self.time_per_step_le, 5, 1, 1, 1)
        self._measurement_layout.addWidget(self.num_repeats_lbl, 5, 2, 1, 1)
        self._measurement_layout.addWidget(self.num_repeats_sb, 5, 3, 1, 1)
        self._measurement_layout.addWidget(self.num_points_label_lbl, 5, 4, 1, 1)
        self._measurement_layout.addWidget(self.num_steps_lbl, 5, 5, 1, 1)
        self._measurement_layout.addWidget(self.total_time_label_lbl, 5, 6, 1, 1)
        self._measurement_layout.addWidget(self.total_time_lbl, 5, 7, 1, 1)
        self._measurement_layout.addWidget(self.start_collection_btn, 6, 0, 1, 1)
        self._measurement_layout.addWidget(self.abort_collection_btn, 6, 0, 1, 1)
        self._measurement_layout.addWidget(self.pause_collection_btn, 6, 1, 1, 1)
        self._measurement_layout.addWidget(self.current_theta_label_lbl, 7, 2, 1, 1)
        self._measurement_layout.addWidget(self.current_theta_lbl, 7, 3, 1, 1)
        self._measurement_layout.addWidget(self.current_energy_label_lbl, 7, 4, 1, 1)
        self._measurement_layout.addWidget(self.current_energy_lbl, 7, 5, 1, 1)
        self._measurement_layout.addWidget(self.next_file_label_lbl, 7, 6, 1, 1)
        self._measurement_layout.addWidget(self.next_file_lbl, 7, 7, 1, 1)

        self.setLayout(self._measurement_layout)

    def update_current_values(self, current_theta, current_energy, next_file_name):
        self.current_theta_lbl.setText("{0:.3f}".format(current_theta))
        self.current_energy_lbl.setText("{0:.3f}".format(current_energy))
        self.next_file_lbl.setText(next_file_name)
