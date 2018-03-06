import os
import math
import numpy as np
from qtpy import QtCore

SI_a = 5.431E-10
Si_h = 4
Si_k = 4
Si_l = 0
h = 4.135667516E-15
c = 299792458

class XESModel(QtCore.QObject):
    # my_signal = QtCore.Signal()

    def __init__(self):
        super(XESModel, self).__init__()

    @staticmethod
    def theta_to_ev(theta):
        lam = 2.0 * SI_a / np.sqrt(Si_h**2 + Si_k**2 + Si_l**2) * np.sin(np.pi*theta/180.0)
        ev = h*c/lam
        return ev

    @staticmethod
    def ev_to_theta(ev):
        sin_theta = h*c/ev/2.0/(SI_a/np.sqrt(Si_h**2 + Si_k**2 + Si_l**2))
        theta = 180.0 * np.arcsin(sin_theta)/np.pi
        return theta
