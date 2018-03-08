# -*- coding: utf8 -*-
import os
from sys import platform as _platform

from qtpy import QtWidgets, QtCore

from ..widgets.MainWidget import MainWidget


class MainController(object):
    def __init__(self, use_settings=True):
        self.widget = MainWidget()

    def show_window(self):
        """
        Displays the main window on the screen and makes it active.
        """
        self.widget.show()

        if _platform == "darwin":
            self.widget.setWindowState(self.widget.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
            self.widget.activateWindow()
            self.widget.raise_()
