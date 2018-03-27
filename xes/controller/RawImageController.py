# -*- coding: utf8 -*-
import os
from sys import platform as _platform
import logging
import time
import numpy as np
from epics import caput, caget

from qtpy import QtWidgets, QtCore

from ..widgets.MainAnalysisWidget import MainAnalysisWidget
from ..widgets.RawImageWidget import RawImageWidget
from ..model.XESModel import XESModel
from ..model.XESSpectrum import XESSpectrum
from ..widgets.UtilityWidgets import save_file_dialog


class RawImageController(QtCore.QObject):
    def __init__(self, widget, model):
        """
        :param widget:
        :type widget: MainAnalysisWidget
        :param model:
        :type model: XESModel
        """
        super(RawImageController, self).__init__()
        self.main_widget = widget
        self.model = model
        self.widget = self.main_widget.raw_image_widget
        self.setup_connections()

    def setup_connections(self):
        self.widget.data_img_item.mou
