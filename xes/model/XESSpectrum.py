import os
import math
import numpy as np
from qtpy import QtCore
from .calib import detector_calibration
from collections import OrderedDict


class XESSpectrum(QtCore.QObject):
    # my_signal = QtCore.Signal()

    def __init__(self):
        super(XESSpectrum, self).__init__()
        self._all_data = []
        self._max_ic1 = 0
        self._max_ic2 = 0
        self._max_aps_beam = 0
        self.theta_values = []
        self.num_repeats = 0

    def add_data(self, file_name, theta_ind, theta, counts, exp_time, time, ic1, ic2, aps_beam):
        new_data = OrderedDict()
        new_data['file_name'] = file_name
        new_data['theta_ind'] = theta_ind
        new_data['theta'] = theta
        new_data['counts'] = counts
        new_data['exp_time'] = exp_time
        new_data['time'] = time
        new_data['IC1'] = ic1
        new_data['IC2'] = ic2
        new_data['aps_beam'] = aps_beam

        if ic1 > self._max_ic1:
            self._max_ic1 = ic1
        if ic2 > self._max_ic2:
            self._max_ic2 = ic2
        if aps_beam > self._max_aps_beam:
            self._max_aps_beam = aps_beam
        self._all_data.append(new_data.copy())
        print(new_data)

    def gather_data_for_theta(self, theta_ind):
        counts = 0
        exp_time = 0
        for data_point in self._all_data:
            if data_point['theta_ind'] == theta_ind:
                counts += data_point['counts']
                exp_time += data_point['exp_time']
        return counts, exp_time

    def export_data(self, filename):
        file_handle = open(filename, 'w')
        num_points = len(self.all_data)
        header1 = '# Theta from: ' + str(min(self.theta_values)) + ' to ' + str(max(self.theta_values)) + \
                  ', repeating ' + str(num_points) + ' times\n'

        file_handle.write(header1)
        header2 = ''
        for key in self.all_data[0]:
            header2 = header2 + key + '\t'
        header2 = header2 + '\n'
        file_handle.write(header2)
        for data_point in self.all_data:
            line = ''
            for key in data_point:
                line = line + str(data_point[key]) + '\t'
            file_handle.write(line+'\n')

    @property
    def all_data(self):
        return self._all_data
