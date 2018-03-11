# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.exporters

import numpy as np


class GraphWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(GraphWidget, self).__init__(*args, **kwargs)

        self.graph_units_lbl = QtWidgets.QLabel('Graph Units: ')
        self.graph_units_list = QtWidgets.QComboBox()
        self.graph_units_list.addItem('Energy (eV)')
        self.graph_units_list.addItem('Theta (deg)')

        self.graph_normalize_lbl = QtWidgets.QLabel('Normalization')
        self.graph_normalize_list = QtWidgets.QComboBox()
        self.graph_normalize_list.addItem('Raw')
        self.graph_normalize_list.addItem('IC1')
        self.graph_normalize_list.addItem('IC2')
        self.graph_normalize_list.addItem('APS')

        self.graph_export_image_btn = QtWidgets.QPushButton('Export Image')
        self.graph_export_data_btn = QtWidgets.QPushButton('Export Data')
        self.current_spectrum_sb = QtWidgets.QSpinBox()
        self.spectra_count_lbl = QtWidgets.QLabel('of 0')

        self._graph_control_layout = QtWidgets.QGridLayout()
        self._graph_control_layout.addWidget(self.graph_units_lbl, 1, 1, 1, 1)
        self._graph_control_layout.addWidget(self.graph_units_list, 1, 2, 1, 1)
        self._graph_control_layout.addWidget(self.graph_normalize_lbl, 1, 3, 1, 1)
        self._graph_control_layout.addWidget(self.graph_normalize_list, 1, 4, 1, 1)
        self._graph_control_layout.addWidget(self.graph_export_image_btn, 2, 1, 1, 1)
        self._graph_control_layout.addWidget(self.graph_export_data_btn, 2, 2, 1, 1)
        self._graph_control_layout.addWidget(self.current_spectrum_sb, 3, 2, 1, 1)
        self._graph_control_layout.addWidget(self.spectra_count_lbl, 3, 3, 1, 1)

        self.xes_graph = pg.GraphicsLayoutWidget()

        self._graph_layout = QtWidgets.QHBoxLayout()
        self._graph_layout.addWidget(self.xes_graph)
        self._graph_layout.addLayout(self._graph_control_layout)
        self.setLayout(self._graph_layout)

        xes_plot_labels = {'left': 'CPS', 'bottom': 'Energy (eV)'}
        self.xes_spectrum_plot = self.xes_graph.addPlot(labels=xes_plot_labels)

        self.current_spectrum = 0

        self.xes_spectra = []
        self.xes_theta_values = []
        self.xes_ev_values = []
        self.xes_count_values = []

        # self.normalizer = 'RAW'

        self._set_widget_properties()

        # TODO: make energy choice work
        # TODO: Modify exports to work for spectrum choice.
        # TODO: Check if normalization works for older spectra.

    def _set_widget_properties(self):
        self.current_spectrum_sb.setValue(0)
        self.current_spectrum_sb.setMinimum(0)
        self.current_spectrum_sb.setMaximum(0)

    def add_empty_xes_spectrum_to_graph(self, theta_values, ev_values):
        if len(self.xes_spectra) > 0:
            self.xes_spectrum_plot.removeItem(self.xes_spectra[self.current_spectrum])
        main_pen = pg.mkPen({'color': (255, 255, 0), 'width': 2.0})

        self.xes_theta_values.append(theta_values)
        self.xes_ev_values.append(ev_values)
        self.xes_count_values.append(np.zeros(len(theta_values)))

        self.xes_spectra.append(self.xes_spectrum_plot.plot(self.xes_ev_values[-1], self.xes_count_values[-1],
                                                            pen=main_pen, name="Current Data"))

        self.current_xes_data_plot = self.xes_spectra[-1]
        self.update_current_graph_index(len(self.xes_spectra))

    def update_current_graph_index(self, num_spectra):
        self.current_spectrum = num_spectra - 1
        self.spectra_count_lbl.setText('of ' + str(num_spectra))
        self.current_spectrum_sb.setMaximum(num_spectra)
        self.current_spectrum_sb.setMinimum(1)
        self.current_spectrum_sb.setValue(num_spectra)

    def update_data_point(self, theta_ind, new_counts):
        self.xes_count_values[-1][theta_ind] = new_counts
        self.update_graph_plot(-1)

    def update_graph_values(self, xes_count_values):
        ind = self.current_spectrum_sb.value() - 1
        self.xes_count_values[ind] = xes_count_values
        self.update_graph_plot(ind)

    def update_graph_plot(self, ind):
        units = self.graph_units_list.currentIndex()
        if units == 0:
            self.xes_spectra[ind].setData(self.xes_ev_values[ind], self.xes_count_values[ind])
        elif units == 1:
            self.xes_spectra[ind].setData(self.xes_theta_values[ind], self.xes_count_values[ind])
        QtWidgets.QApplication.processEvents()

    # def add_xes_spectrum_to_graph(self):
        # xes_plot_labels = {'left': 'CPS', 'bottom': 'Energy (eV)', 'top': 'Theta (deg)'}
        # self.xes_spectrum_plot = self.xes_graph.addPlot(labels=xes_plot_labels)
        # main_pen = pg.mkPen({'color': (255, 255, 0), 'width': 2.0})
        #
        # self.xes_data_plot = self.xes_spectrum_plot.plot(self.x_vector, self.counts_vector, pen=main_pen,
        #                                                  name="Current Data")

    def export_graph(self, filename):
        self.exporter = pg.exporters.ImageExporter(self.xes_graph.scene())
        # temp_working_dir = caget(epc['temperature_directory'], as_string=True)
        # file_name = 'ramp_' + str(self.file_number['First'] + 1) + '_' + str(self.file_number['Last']) + '.png'
        self.exporter.export(filename)

    # def change_graph_units(self, unit):
    #     if unit == 0:
    #         self.current_xes_data_plot.setData(self.xes_ev_values[-1], self.xes_count_values[-1])
    #     elif unit == 1:
    #         self.current_xes_data_plot.setData(self.xes_theta_values[-1], self.xes_count_values[-1])
    #     else:
    #         return
    #     QtWidgets.QApplication.processEvents()
