import os
import math
import numpy as np
from qtpy import QtCore
from .calib import detector_calibration


class XESSpectrum(QtCore.QObject):
    # my_signal = QtCore.Signal()

    def __init__(self):
        super(XESSpectrum, self).__init__()
        self._all_data = []
        self._max_ic1 = 0
        self._max_ic2 = 0
        self._max_aps_beam = 0

    def add_data(self, file_name, theta_ind, theta, counts, exp_time, time, ic1, ic2, aps_beam):
        new_data = {
            'file_name': file_name,
            'theta_ind': theta_ind,
            'theta': theta,
            'counts': counts,
            'exp_time': exp_time,
            'time': time,
            'IC1': ic1,
            'IC2': ic2,
            'aps_beam': aps_beam,
        }
        if ic1 > self._max_ic1:
            self._max_ic1 = ic1
        if ic2 > self._max_ic2:
            self._max_ic2 = ic2
        if aps_beam > self._max_aps_beam:
            self._max_aps_beam = aps_beam
        self._all_data.append(new_data.copy())
        print(new_data)

    # TODO: Fix this part. It doesn't work when rounding theta. Use index instead.
    def gather_data_for_theta(self, theta_ind):
        counts = 0
        exp_time = 0
        for data_point in self._all_data:
            if data_point['theta_ind'] == theta_ind:
                counts += data_point['counts']
                exp_time += data_point['exp_time']
        return counts, exp_time

    @property
    def all_data(self):
        return self._all_data
