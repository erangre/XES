import os
import math
import numpy as np
from qtpy import QtCore
from .calib import detector_calibration

Si_a = 5.431E-10
Si_h = 4
Si_k = 4
Si_l = 0
h = 4.135667516E-15
c = 299792458


class XESModel(QtCore.QObject):
    # my_signal = QtCore.Signal()

    def __init__(self):
        super(XESModel, self).__init__()

    def theta_to_ev(self, theta):
        d_hkl = self.d_hkl(Si_a, Si_h, Si_k, Si_l)
        lam = 2.0 * d_hkl * np.sin(np.pi*theta/180.0)
        ev = h*c/lam
        return ev

    def ev_to_theta(self, ev):
        d_hkl = self.d_hkl(Si_a, Si_h, Si_k, Si_l)
        sin_theta = h*c/ev/2.0/d_hkl
        theta = 180.0 * np.arcsin(sin_theta)/np.pi
        return theta

    def theta_step_to_ev_step(self, E, theta, d_theta):
        d_ev = abs(E / np.tan(theta*np.pi/180.0) * d_theta*np.pi/180.0)
        return d_ev

    def ev_step_to_theta_step(self, E, theta, d_ev):
        d_theta_rad = d_ev/E*np.tan(theta*np.pi/180.0)
        d_theta = d_theta_rad*180.0/np.pi
        return d_theta

    def theta_to_roi(self, theta, calib=detector_calibration):
        roi_start = calib['roi_start'] + calib['slope'] * (theta - calib['theta_0'])
        roi_end = roi_start + calib['roi_width']
        return roi_start, roi_end

    @staticmethod
    def d_hkl(a, hh, kk, ll):
        d = a / np.sqrt(hh**2 + kk**2 + ll**2)
        return d

