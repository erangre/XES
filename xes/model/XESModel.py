import os
import math
import numpy as np
from qtpy import QtCore
from .calib import detector_calibration
from PIL import Image
from collections import OrderedDict
from .XESSpectrum import XESSpectrum

Si_a = 5.431E-10
Si_h = 4
Si_k = 4
Si_l = 0
h = 4.135667516E-15
c = 299792458


class XESModel(QtCore.QObject):
    image_changed = QtCore.Signal()

    def __init__(self):
        super(XESModel, self).__init__()
        self.current_directories = {
            'raw_image_directory': os.getcwd(),
            'export_image_directory': os.getcwd(),
            'export_data_directory': os.getcwd(),
            'roi_directory': os.getcwd(),
        }
        self.calibration = detector_calibration.copy()
        self.xes_spectra = []  # type: list[XESSpectrum]
        self.rois = []
        self.current_spectrum = None
        self.current_spectrum_ind = None
        self.im_data = None
        self.current_raw_im_ind = None
        self.current_roi_data = None
        self.base_rois = []

    def theta_to_ev(self, theta):
        d_hkl = self.d_hkl(Si_a, Si_h, Si_k, Si_l)
        lam = 2.0 * d_hkl * np.sin(np.pi*theta/180.0)
        ev = h*c/lam
        return ev

    def ev_to_theta(self, ev):
        d_hkl = self.d_hkl(Si_a, Si_h, Si_k, Si_l)
        sin_theta = h*c/ev/2.0/d_hkl
        theta = 180.0 * np.arcsin(sin_theta)/np.pi
        return theta

    def theta_step_to_ev_step(self, E, theta, d_theta):
        d_ev = abs(E / np.tan(theta*np.pi/180.0) * d_theta*np.pi/180.0)
        return d_ev

    def ev_step_to_theta_step(self, E, theta, d_ev):
        d_theta_rad = d_ev/E*np.tan(theta*np.pi/180.0)
        d_theta = d_theta_rad*180.0/np.pi
        return d_theta

    def theta_to_roi(self, theta, calib=None):
        if calib is None:
            calib = self.calibration
        roi_start = calib['roi_start'] + calib['slope'] * (theta - calib['theta_zero'])
        roi_end = roi_start + calib['roi_width']
        return roi_start, roi_end

    def open_files(self, ind, file_names):
        theta_min = 90.0
        theta_max = 0.0
        theta_values = []
        ev_values = []
        self.rois.append(OrderedDict())
        self.base_rois.append(None)
        for raw_image_file in file_names:
            filename = str(raw_image_file)
            img_file = open(filename, 'rb')
            im = Image.open(img_file)
            # self.xes_spectra[ind].raw_images.append(np.array(im)[::-1])
            self.xes_spectra[ind].raw_images_info.append(self._get_file_info(im))
            self.xes_spectra[ind].raw_images_info[-1]['File Name'] = filename
            theta = float(self.xes_spectra[ind].raw_images_info[-1]['XES angle'])
            if theta < theta_min:
                theta_min = theta
            if theta > theta_max:
                theta_max = theta

            if theta not in theta_values:
                theta_values.append(theta)
                ev_values.append(self.theta_to_ev(theta))
                if self.base_rois[-1] is None:
                    im_shape = np.array(im)[::-1].shape
                    self.prepare_basic_roi(im_shape)
                self.rois[-1][theta] = self.prepare_roi_for_theta(theta)

            im.close()
            img_file.close()

        self.xes_spectra[ind].theta_values = list(theta_values)
        return theta_values, ev_values

    def prepare_basic_roi(self, im_shape):
        self.base_rois[-1] = np.zeros(shape=im_shape, dtype=bool)
        for col in range(int(self.calibration['roi_width'])):
            self.base_rois[-1][:, col] = True

    def prepare_roi_for_theta(self, theta):
        # roi_array = np.zeros(shape=im_shape, dtype=bool)
        roi_start, roi_end = self.theta_to_roi(theta)
        # for roi_column in range(int(roi_start), int(roi_end)):
        #     roi_array[:, roi_column] = True
        roi_array = np.roll(self.base_rois[-1], int(roi_start), axis=1)
        return roi_array

    def recalc_all_rois(self):
        ind = self.current_raw_im_ind
        s_ind = self.current_spectrum_ind
        theta = self.current_spectrum.all_data[ind]['theta']
        roi_start, roi_end = self.theta_to_roi(theta)
        self.base_rois[s_ind] = np.roll(self.current_roi_data, -int(roi_start), axis=1)
        for theta in self.current_spectrum.theta_values:
            self.rois[s_ind][theta] = self.prepare_roi_for_theta(theta)

    def _get_file_info(self, image):
        result = {}
        tags = image.tag

        useful_tags = ['XES angle:', 'Ion chamber2:', 'ID RingCurrent:', 'Date:', 'Exposure time(s):']

        try:
            tag_values = tags.itervalues()
        except AttributeError:
            tag_values = tags.values()

        for value in tag_values:
            for key in useful_tags:
                if key in str(value):
                    k, v = str(value[0]).split(':', 1)
                    result[str(k)] = v
        return result

    def add_data_set_to_spectrum(self, ind):
        self.current_spectrum = self.xes_spectra[ind]  # type: XESSpectrum
        self.current_spectrum_ind = ind
        for image_info in self.current_spectrum.raw_images_info:
            file_name = image_info['File Name']
            theta = float(image_info['XES angle'])
            theta_ind = self.current_spectrum.theta_values.index(theta)
            counts = self.calc_counts_for_file_name(file_name, theta)
            exp_time = float(image_info['Exposure time(s)'])
            c_time = image_info['Date']
            ic1 = 1
            ic2 = float(image_info['Ion chamber2'])
            aps_beam = float(image_info['ID RingCurrent'])

            self.current_spectrum.add_data(file_name, theta_ind, theta, counts, exp_time, c_time, ic1, ic2, aps_beam,
                                           live_data=False)

    def sum_rect_roi(self, im_data, roi_start, roi_width, roi_left, roi_range):
        roi_data = im_data[roi_left:(roi_left + roi_range+1), roi_start:(roi_start+roi_width+1)]
        return roi_data.sum()

    def recalc_all_counts(self):
        for data_point in self.current_spectrum.all_data:
            file_name = data_point['file_name']
            theta = float(data_point['theta'])
            data_point['counts'] = self.calc_counts_for_file_name(file_name, theta)

    def calc_counts_for_file_name(self, file_name, theta):
        s_ind = self.current_spectrum_ind

        file_name = str(file_name)
        img_file = open(file_name, 'rb')
        im = Image.open(img_file)
        img_data = np.array(im)[::-1]
        roi_data = self.rois[s_ind][theta]
        counts = np.sum(img_data[roi_data])
        im.close()
        img_file.close()
        return counts

    def sum_general_roi(self, im_data, roi):
        return im_data[roi].sum()

    def set_current_image(self, ind):
        self.current_raw_im_ind = ind
        file_name = self.current_spectrum.all_data[ind]['file_name']
        img_file = open(file_name, 'rb')
        im = Image.open(img_file)
        self.im_data = np.array(im)[::-1]

        theta = self.current_spectrum.all_data[ind]['theta']
        self.current_roi_data = self.rois[self.current_spectrum_ind][theta]

        im.close()
        img_file.close()
        self.image_changed.emit()

    def save_roi(self, file_name):
        ind = self.current_raw_im_ind
        s_ind = self.current_spectrum_ind
        theta = self.current_spectrum.all_data[ind]['theta']
        roi_start, roi_end = self.theta_to_roi(theta)
        base_roi = np.roll(self.current_roi_data, -int(roi_start), axis=1)
        np.save(file_name, base_roi)

    def load_roi(self, file_name):
        s_ind = self.current_spectrum_ind
        self.base_rois[s_ind] = np.load(file_name)
        for theta in self.current_spectrum.theta_values:
            self.rois[s_ind][theta] = self.prepare_roi_for_theta(theta)
        self.image_changed.emit()

    @staticmethod
    def d_hkl(a, hh, kk, ll):
        d = a / np.sqrt(hh**2 + kk**2 + ll**2)
        return d

