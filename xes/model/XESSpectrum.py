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

    def add_data(self, file_name, theta, counts, time, ic1, ic2, aps_beam):
        new_data = {
            'file_name': file_name,
            'theta': theta,
            'counts': counts,
            'time': time,
            'IC1': ic1,
            'IC2': ic2,
            'aps_beam': aps_beam,
        }
        self._all_data.append(new_data.copy())

    @property
    def all_data(self):
        return self._all_data
