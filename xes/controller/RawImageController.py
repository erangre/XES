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
        self.widget.prev_raw_image_btn.clicked.connect(self.prev_raw_image_btn_clicked)
        self.widget.next_raw_image_btn.clicked.connect(self.next_raw_image_btn_clicked)
        self.widget.raw_image_list.currentIndexChanged.connect(self.raw_image_list_item_changed)

    def process_mouse_left_clicked(self, x, y):
        if self.model.im_data is None:
            return
        x = int(x)
        y = int(y)
        im_shape = self.model.im_data.shape
        if x >= 0 and y >= 0 and x < im_shape[1] and y < im_shape[0]:
            self.widget.x_pos_pixel_lbl.setText(str(x))
            self.widget.y_pos_pixel_lbl.setText(str(y))
            self.widget.int_pixel_lbl.setText(str(self.model.im_data.T[x][y]))
            self.model.current_roi_data.T[x][y] = not self.model.current_roi_data.T[x][y]
            self.model.recalc_all_rois()
            self.widget.img_view.plot_mask(self.model.current_roi_data)

    def process_mouse_moved(self, x, y):
        if self.model.im_data is None:
            return
        x = int(x)
        y = int(y)
        im_shape = self.model.im_data.shape
        if x >= 0 and y >= 0 and x < im_shape[1] and y < im_shape[0]:
            self.widget.hover_x_pos_pixel_lbl.setText(str(x))
            self.widget.hover_y_pos_pixel_lbl.setText(str(y))
            self.widget.hover_int_pixel_lbl.setText(str(self.model.im_data.T[x][y]))

    def prev_raw_image_btn_clicked(self):
        ind = self.model.current_raw_im_ind
        if ind is None or ind == 0:
            return
        self.model.set_current_image(ind - 1)
        self.widget.raw_image_list.setCurrentIndex(ind - 1)

    def next_raw_image_btn_clicked(self):
        ind = self.model.current_raw_im_ind
        if ind is None or ind >= self.model.current_spectrum.num_data_points - 1:
            return
        self.model.set_current_image(ind + 1)
        self.widget.raw_image_list.setCurrentIndex(ind + 1)

    def raw_image_list_item_changed(self, ind):
        self.model.set_current_image(ind)
