# -*- coding: utf8 -*-
from __future__ import absolute_import

import sys
import os
import time

try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
import traceback
from qtpy import QtWidgets

# resources_path = os.path.join(os.path.dirname(__file__), 'resources')
# calibrants_path = os.path.join(resources_path, 'calibrants')
# icons_path = os.path.join(resources_path, 'icons')
# data_path = os.path.join(resources_path, 'data')
# style_path = os.path.join(resources_path, 'style')


# from .widgets.UtilityWidgets import ErrorMessageBox


def excepthook(exc_type, exc_value, traceback_obj):
    """
    Global function to catch unhandled exceptions. This function will result in an error dialog which displays the
    error information.

    :param exc_type: exception type
    :param exc_value: exception value
    :param traceback_obj: traceback object
    :return:
    """

    separator = '-' * 80
    # log_file = "error.log"
    # notice = \
    #     """An unhandled exception occurred. Please report the bug under:\n """ \
    #     """\t%s\n""" \
    #     """or via email to:\n\t <%s>.\n\n""" \
    #     """A log has been written to "%s".\n\nError information:\n""" % \
    #     ("https://github.com/Dioptas/Dioptas/issues",
    #      "clemens.prescher@gmail.com",
    #      os.path.join(os.path.dirname(__file__), log_file))
    time_string = time.strftime("%Y-%m-%d, %H:%M:%S")
    tb_info_file = StringIO()
    traceback.print_tb(traceback_obj, None, tb_info_file)
    traceback.print_exception(exc_type, exc_value, traceback_obj)
    tb_info_file.seek(0)
    tb_info = tb_info_file.read()
    errmsg = '%s: \n%s' % (str(exc_type), str(exc_value))
    sections = [separator, time_string, separator, errmsg, separator, tb_info]
    msg = '\n'.join(sections)
    print(msg)
    # try:
    #     f = open(log_file, "w")
    #     f.write(msg)
    #     f.write(version_info)
    #     f.close()
    # except IOError:
    #     pass
    # errorbox = ErrorMessageBox()
    # errorbox.setText(str(notice) + str(msg) + str(version_info))
    # errorbox.exec_()


def main():
    app = QtWidgets.QApplication([])
    sys.excepthook = excepthook
    from sys import platform as _platform
    # from .controller.MainController import MainController

    if _platform == "linux" or _platform == "linux2" or _platform == "win32" or _platform == 'cygwin':
        app.setStyle('plastique')

    # controller = MainController()
    # controller.show_window()
    app.exec_()
    del app
