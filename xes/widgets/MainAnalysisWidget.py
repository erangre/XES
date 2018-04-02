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


class ManualFileInfoDialog(QtWidgets.QDialog):
    """
    Dialog for inputting the file info manually
    """

    def __init__(self, parent):
        super(ManualFileInfoDialog, self).__init__()

        self._parent = parent
        self._create_widgets()
        self._layout_widgets()
        self._style_widgets()

        self._connect_widgets()
        self.approved = False

    def _create_widgets(self):
        self.selected_files = QtWidgets.QListWidget()
        self.read_list_btn = QtWidgets.QPushButton('Show Files')
        self.move_up_btn = QtWidgets.QPushButton(u'\u2191')
        self.move_down_btn = QtWidgets.QPushButton(u'\u2193')
        # self.add_empty_btn = QtWidgets.QPushButton('Empty')
        self.delete_btn = QtWidgets.QPushButton('Delete')

        self.start_energy_lbl = QtWidgets.QLabel("Start Energy (eV)")
        self.end_energy_lbl = QtWidgets.QLabel("End Energy (eV)")
        self.energy_step_lbl = QtWidgets.QLabel("Energy Step (eV)")
        self.num_step_lbl = QtWidgets.QLabel("0 Steps")
        self.num_repeats_lbl = QtWidgets.QLabel("0 repeats")
        self.num_expected_files_lbl = QtWidgets.QLabel("0 Expected Files")
        self.total_files_lbl = QtWidgets.QLabel("0 Files")

        self.start_energy_le = QtWidgets.QLineEdit()
        self.end_energy_le = QtWidgets.QLineEdit()
        self.energy_step_le = QtWidgets.QLineEdit()

        self.ok_btn = QtWidgets.QPushButton("Done")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

    def _layout_widgets(self):
        self._grid_layout = QtWidgets.QGridLayout()
        self._hbox_layout = QtWidgets.QHBoxLayout()
        self._vbox_list_layout = QtWidgets.QVBoxLayout()
        self._vbox_list_controls_layout = QtWidgets.QVBoxLayout()

        self._grid_layout.addWidget(self.start_energy_lbl, 0, 0)
        self._grid_layout.addWidget(self.start_energy_le, 0, 1)
        self._grid_layout.addWidget(self.end_energy_lbl, 1, 0)
        self._grid_layout.addWidget(self.end_energy_le, 1, 1)
        self._grid_layout.addWidget(self.energy_step_lbl, 2, 0)
        self._grid_layout.addWidget(self.energy_step_le, 2, 1)
        self._grid_layout.addWidget(self.num_step_lbl, 3, 0)
        self._grid_layout.addWidget(self.num_repeats_lbl, 3, 1)
        self._grid_layout.addWidget(self.num_expected_files_lbl, 4, 0)
        self._grid_layout.addWidget(self.ok_btn, 4, 0)
        self._grid_layout.addWidget(self.cancel_btn, 4, 1)

        self._hbox_layout.addLayout(self._grid_layout)

        self._vbox_list_layout.addWidget(self.selected_files)
        self._vbox_list_layout.addWidget(self.total_files_lbl)
        self._hbox_layout.addLayout(self._vbox_list_layout)

        self._vbox_list_controls_layout.addWidget(self.read_list_btn)
        self._vbox_list_controls_layout.addWidget(self.move_up_btn)
        # self._vbox_list_controls_layout.addWidget(self.add_empty_btn)
        self._vbox_list_controls_layout.addWidget(self.delete_btn)
        self._vbox_list_controls_layout.addWidget(self.move_down_btn)

        self._hbox_layout.addLayout(self._vbox_list_controls_layout)
        self.setLayout(self._hbox_layout)

    def _style_widgets(self):
        """
        Makes everything pretty and set double/int validators for the line edits.
        """

        self.selected_map_files.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.start_energy_le.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.start_energy_le.setMaximumWidth(40)
        self.end_energy_le.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.end_energy_le.setMaximumWidth(40)
        self.energy_step_le.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.energy_step_le.setMaximumWidth(40)

        self.start_energy_le.setValidator(QtGui.QDoubleValidator())
        self.end_energy_le.setValidator(QtGui.QDoubleValidator())
        self.energy_step_le.setValidator(QtGui.QDoubleValidator())

        self.ok_btn.setEnabled(False)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #
        # file = open(os.path.join(style_path, "stylesheet.qss"))
        # stylesheet = file.read()
        # self.setStyleSheet(stylesheet)
        # file.close()

    def _connect_widgets(self):
        """
        Connecting actions to slots.
        """
        self.ok_btn.clicked.connect(self.accept_manual_file_info)
        self.cancel_btn.clicked.connect(self.reject_manual_file_info)

    def accept_manual_file_info(self):
        self.approved = True
        self.accept()

    def reject_manual_file_info(self):
        self.approved = False
        self.reject()

    @property
    def start_energy(self):
        return float(str(self.start_energy_le.text()))

    @property
    def end_energy(self):
        return float(str(self.end_energy_le.text()))

    @property
    def energy_step(self):
        return float(str(self.energy_step_le.text()))

    def exec_(self):
        """
        Overwriting the dialog exec_ function to center the widget in the parent window before execution.
        """
        parent_center = self._parent.window().mapToGlobal(self._parent.window().rect().center())
        self.move(parent_center.x() - 101, parent_center.y() - 48)
        super(ManualFileInfoDialog, self).exec_()
