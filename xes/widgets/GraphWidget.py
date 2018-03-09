# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class GraphWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(GraphWidget, self).__init__(*args, **kwargs)

        self.xes_graph = pg.GraphicsLayoutWidget()

        self._graph_layout = QtWidgets.QHBoxLayout()
        self._graph_layout.addWidget(self.xes_graph)
        self.setLayout(self._graph_layout)
        xes_plot_labels = {'left': 'CPS', 'bottom': 'Energy (eV)'}
        self.xes_spectrum_plot = self.xes_graph.addPlot(labels=xes_plot_labels)
        self.xes_spectra = []
        self.xes_theta_values = []
        self.xes_ev_values = []
        self.xes_count_values = []

    def add_empty_xes_spectrum_to_graph(self, theta_values, ev_values):
        main_pen = pg.mkPen({'color': (255, 255, 0), 'width': 2.0})

        self.xes_theta_values.append(theta_values)
        self.xes_ev_values.append(ev_values)
        self.xes_count_values.append(np.zeros(len(theta_values)))

        self.xes_spectra.append(self.xes_spectrum_plot.plot(self.xes_ev_values[-1], self.xes_count_values[-1],
                                                            pen=main_pen, name="Current Data"))

        self.current_xes_data_plot = self.xes_spectra[-1]

    def update_data_point(self, theta_ind, new_counts, theta_reversed):
        if theta_reversed:
            self.xes_count_values[-1][-theta_ind-1] = new_counts
        else:
            self.xes_count_values[-1][theta_ind] = new_counts
        self.current_xes_data_plot.setData(self.xes_ev_values[-1], self.xes_count_values[-1])
        QtWidgets.QApplication.processEvents()

    # def add_xes_spectrum_to_graph(self):
        # xes_plot_labels = {'left': 'CPS', 'bottom': 'Energy (eV)', 'top': 'Theta (deg)'}
        # self.xes_spectrum_plot = self.xes_graph.addPlot(labels=xes_plot_labels)
        # main_pen = pg.mkPen({'color': (255, 255, 0), 'width': 2.0})
        #
        # self.xes_data_plot = self.xes_spectrum_plot.plot(self.x_vector, self.counts_vector, pen=main_pen,
        #                                                  name="Current Data")

    # def export_graph(self):
    #     self.exporter = pg.exporters.ImageExporter(self.ramp_graph.scene())
    #     temp_working_dir = caget(epc['temperature_directory'], as_string=True)
    #     file_name = 'ramp_' + str(self.file_number['First'] + 1) + '_' + str(self.file_number['Last']) + '.png'
    #     self.exporter.export(temp_working_dir + '\\' + file_name)

