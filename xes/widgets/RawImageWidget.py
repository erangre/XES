# -*- coding: utf8 -*-

from qtpy import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np


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
        self.modify_mouse_behavior()

    def set_widget_properties(self):
        self.bottom_axis.setLabel('pixel')
        self.left_axis.setLabel('pixel')

    def modify_mouse_behavior(self):
        self.img_view_box.mouseClickEvent = self.myMouseClickEvent

    def myMouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton or \
                (ev.button() == QtCore.Qt.LeftButton and
                 ev.modifiers() & QtCore.Qt.ControlModifier):
            view_range = np.array(self.img_view_box.viewRange()) * 2
            if self.img_data is not None:
                if (view_range[0][1] - view_range[0][0]) > self.img_data.shape[1] and \
                                (view_range[1][1] - view_range[1][0]) > self.img_data.shape[0]:
                    self.auto_range()
                else:
                    self.img_view_box.scaleBy(2)

        elif ev.button() == QtCore.Qt.LeftButton:
            pos = self.img_view_box.mapFromScene(ev.pos())
            pos = self.img_scatter_plot_item.mapFromScene(2 * ev.pos() - pos)
            self.mouse_left_clicked.emit(pos.x(), pos.y())

    def auto_range(self):
        self.img_view_box.autoRange()
        # self._max_range = True

    def load_image(self, img_data):
        self.img_data = img_data
        self.data_img_item.setImage(img_data.T)

