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
        self.widget.img_view.mouse_left_clicked.connect(self.process_mouse_left_clicked)
        self.widget.img_view.mouse_moved.connect(self.process_mouse_moved)

    def process_mouse_left_clicked(self, x, y):
        x = int(x)
        y = int(y)
        im_shape = self.model.im_data.shape
        if x >= 0 and y >= 0 and x < im_shape[1] and y < im_shape[0]:
            self.widget.x_pos_pixel_lbl.setText(str(x))
            self.widget.y_pos_pixel_lbl.setText(str(y))
            self.widget.int_pixel_lbl.setText(str(self.model.im_data.T[x][y]))
            self.model.current_roi_data.T[x][y] = not self.model.current_roi_data.T[x][y]

    def process_mouse_moved(self, x, y):
        x = int(x)
        y = int(y)
        im_shape = self.model.im_data.shape
        if x >= 0 and y >= 0 and x < im_shape[1] and y < im_shape[0]:
            self.widget.hover_x_pos_pixel_lbl.setText(str(x))
            self.widget.hover_y_pos_pixel_lbl.setText(str(y))
            self.widget.hover_int_pixel_lbl.setText(str(self.model.im_data.T[x][y]))
