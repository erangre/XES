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
from ..widgets.UtilityWidgets import save_file_dialog, open_file_dialog


class RawImageController(QtCore.QObject):
    roi_changed = QtCore.Signal()

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
        self.widget.reintegrate_btn.clicked.connect(self.reintegrate_btn_clicked)
        self.widget.save_roi_btn.clicked.connect(self.save_roi_btn_clicked)
        self.widget.load_roi_btn.clicked.connect(self.load_roi_btn_clicked)
        self.widget.bg_roi_size_sb.valueChanged.connect(self.bg_roi_size_changed)

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
            # self.roi_changed.emit()

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

    def reintegrate_btn_clicked(self):
        self.roi_changed.emit()

    def save_roi_btn_clicked(self):
        filename = save_file_dialog(
            self.widget, "Save ROI data", self.model.current_directories['roi_directory'],
            'ROI (*.roi)')

        if filename is not '':
            self.model.current_directories['roi_directory'] = os.path.dirname(filename)
            self.model.save_roi(filename)

    def load_roi_btn_clicked(self):
        filename = open_file_dialog(
            self.widget, "Load ROI data", self.model.current_directories['roi_directory'],
            'ROI (*.roi)')

        if filename is not '':
            self.model.current_directories['roi_directory'] = os.path.dirname(filename)
            self.model.load_roi(filename)
            ind = self.model.current_raw_im_ind
            self.model.set_current_image(ind)

    def bg_roi_size_changed(self):
        self.model.recalc_all_bg_rois(size=self.widget.bg_roi_size_sb.value())
        # self.widget.img_view.plot_mask_b(self.model.current_bg_roi_data)
        ind = self.model.current_raw_im_ind
        self.model.set_current_image(ind)