motor_pvs = {
    'theta': '13IDC-PIL:scan1.P1SP',
    'phi': '13IDC-PIL:scan1.P1EP',
}

detector_prefix = '13IDC-PIL:cam1:'
TIFF_prefix = '13IDC-PIL:TIFF1:'
ROI_prefix = '13IDC-PIL:ROI1:'
detector_pvs = {
    'exp_time': detector_prefix + 'AcquireTime',
    'acquire_period': detector_prefix + 'AcquirePeriod',
    'acquire': detector_prefix + 'Acquire',
    'status_message': detector_prefix + 'StatusMessage_RBV',
    'TIFF_base_name': TIFF_prefix + 'FileName_RBV',
    'TIFF_next_number': TIFF_prefix + 'FileNumber_RBV',
    'roi_left': ROI_prefix + 'MinY',
    'roi_size_hor': ROI_prefix + 'SizeY',
    'roi_start': ROI_prefix + 'MinX',
    'roi_size_ver': ROI_prefix + 'SizeX',
    'roi_total_counts': '13IDC-PIL:Stats1:Total_RBV',
}

detector_values = {
    'status_message_ok': 'OK',
}

beam_pvs = {
    'IC1': '13IDA:mono_pid1.CVAL',
    'IC2': '13IDD:userTran1.P',
    'aps_beam': 'S:SRcurrentAI.VAL',
}
