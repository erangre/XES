# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
import pyqtgraph as pg


class RawImageWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(RawImageWidget, self).__init__(*args, **kwargs)

        self._layout = QtWidgets.QVBoxLayout()

        self.setLayout(self._layout)

        self.pg_layout = pg.GraphicsLayoutWidget()

        self.img_data = None
        self.img_view_box = self.pg_layout.addViewBox(1, 1)
        self.data_img_item = pg.ImageItem()
        self.img_view_box.addItem(self.data_img_item)

        self.left_axis = pg.AxisItem('left')
        self.bottom_axis = pg.AxisItem('bottom')

        self._layout.addWidget(self.pg_layout)

        self.set_widget_properties()

    def set_widget_properties(self):
        self.bottom_axis.setLabel('pixel')
        self.left_axis.setLabel('pixel')

    def load_image(self, img_data):
        self.img_data = img_data
        self.data_img_item.setImage(img_data.T)
