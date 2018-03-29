# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import os
import numpy as np
from .ImgWidget import ImgWidget, MaskImgWidget


class RawImageWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RawImageWidget, self).__init__(*args, **kwargs)

        self._layout = QtWidgets.QVBoxLayout()

        self.reintegrate_btn = QtWidgets.QPushButton('Reintegrate')
        self.save_roi_btn = QtWidgets.QPushButton('Save ROI')
        self.load_roi_btn = QtWidgets.QPushButton('Load ROI')

        self._roi_layout = QtWidgets.QHBoxLayout()
        self._roi_layout.addWidget(self.reintegrate_btn)
        self._roi_layout.addWidget(self.save_roi_btn)
        self._roi_layout.addWidget(self.load_roi_btn)

        self._layout.addLayout(self._roi_layout)

        self.prev_raw_image_btn = QtWidgets.QPushButton('Previous')
        self.raw_image_list = QtWidgets.QComboBox()
        self.next_raw_image_btn = QtWidgets.QPushButton('Next')

        self._browsing_layout = QtWidgets.QHBoxLayout()
        self._browsing_layout.addWidget(self.prev_raw_image_btn)
        self._browsing_layout.addWidget(self.raw_image_list)
        self._browsing_layout.addWidget(self.next_raw_image_btn)

        self._layout.addLayout(self._browsing_layout)

        self.img_pg_layout = pg.GraphicsLayoutWidget()
        self.img_view = MaskImgWidget(self.img_pg_layout, orientation='vertical')

        self._layout.addWidget(self.img_pg_layout)

        self.x_pos_pixel_label_lbl = QtWidgets.QLabel('X: ')
        self.x_pos_pixel_lbl = QtWidgets.QLabel('0')
        self.y_pos_pixel_label_lbl = QtWidgets.QLabel('Y: ')
        self.y_pos_pixel_lbl = QtWidgets.QLabel('0')
        self.int_pixel_label_lbl = QtWidgets.QLabel('I: ')
        self.int_pixel_lbl = QtWidgets.QLabel('0')

        self.hover_x_pos_pixel_label_lbl = QtWidgets.QLabel('X: ')
        self.hover_x_pos_pixel_lbl = QtWidgets.QLabel('0')
        self.hover_y_pos_pixel_label_lbl = QtWidgets.QLabel('Y: ')
        self.hover_y_pos_pixel_lbl = QtWidgets.QLabel('0')
        self.hover_int_pixel_label_lbl = QtWidgets.QLabel('I: ')
        self.hover_int_pixel_lbl = QtWidgets.QLabel('0')

        self._mouse_info_layout = QtWidgets.QGridLayout()
        self._mouse_info_layout.addWidget(self.x_pos_pixel_label_lbl, 0, 0, 1, 1)
        self._mouse_info_layout.addWidget(self.x_pos_pixel_lbl, 0, 1, 1, 1)
        self._mouse_info_layout.addWidget(self.y_pos_pixel_label_lbl, 0, 2, 1, 1)
        self._mouse_info_layout.addWidget(self.y_pos_pixel_lbl, 0, 3, 1, 1)
        self._mouse_info_layout.addWidget(self.int_pixel_label_lbl, 0, 4, 1, 1)
        self._mouse_info_layout.addWidget(self.int_pixel_lbl, 0, 5, 1, 1)
        self._mouse_info_layout.addWidget(self.hover_x_pos_pixel_label_lbl, 1, 0, 1, 1)
        self._mouse_info_layout.addWidget(self.hover_x_pos_pixel_lbl, 1, 1, 1, 1)
        self._mouse_info_layout.addWidget(self.hover_y_pos_pixel_label_lbl, 1, 2, 1, 1)
        self._mouse_info_layout.addWidget(self.hover_y_pos_pixel_lbl, 1, 3, 1, 1)
        self._mouse_info_layout.addWidget(self.hover_int_pixel_label_lbl, 1, 4, 1, 1)
        self._mouse_info_layout.addWidget(self.hover_int_pixel_lbl, 1, 5, 1, 1)

        self._layout.addLayout(self._mouse_info_layout)

        self.setLayout(self._layout)

        self.set_widget_properties()

    def set_widget_properties(self):
        pass

    def load_image(self, img_data):
        self.img_view.img_data = img_data
        self.img_view.data_img_item.setImage(img_data.T)

    def update_raw_image_list(self, file_names, ev_values):
        ind = 0
        for file_name, ev_value in zip(file_names, ev_values):
            image_string = os.path.basename(file_name) + '_' + '{:.2f}'.format(ev_value) + '_eV'
            self.raw_image_list.addItem(image_string, ind)
            ind += 1
