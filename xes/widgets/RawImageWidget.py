# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from .ImgWidget import ImgWidget


class RawImageWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RawImageWidget, self).__init__(*args, **kwargs)

        self._layout = QtWidgets.QVBoxLayout()

        self.img_pg_layout = pg.GraphicsLayoutWidget()
        self.img_view = ImgWidget(self.img_pg_layout, orientation='vertical')

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
