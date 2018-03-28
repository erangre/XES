# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from .ImgWidget import ImgWidget


class RawImageWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RawImageWidget, self).__init__(*args, **kwargs)

        self.x_pos_pixel_label_lbl = QtWidgets.QLabel('X: ')
        self.x_pos_pixel_lbl = QtWidgets.QLabel('0')
        self.y_pos_pixel_label_lbl = QtWidgets.QLabel('Y: ')
        self.y_pos_pixel_lbl = QtWidgets.QLabel('0')

        self._layout = QtWidgets.QVBoxLayout()

        self.setLayout(self._layout)

        self.img_pg_layout = pg.GraphicsLayoutWidget()
        self.img_view = ImgWidget(self.img_pg_layout, orientation='horizontal')

        self._layout.addWidget(self.img_pg_layout)

        self.set_widget_properties()

    def set_widget_properties(self):
        pass

    def load_image(self, img_data):
        self.img_view.img_data = img_data
        self.img_view.data_img_item.setImage(img_data.T)
