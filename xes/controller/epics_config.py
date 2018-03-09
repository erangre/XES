motor_pvs = {
    'theta': '13IDC-PIL:AcquireSequence.STR1',
    'phi': '13IDC-PIL:AcquireSequence.STR2',
}

detector_prefix = '13IDC-PIL:cam1:'
TIFF_prefix = '13IDC-PIL:TIFF1:'
detector_pvs = {
    'exp_time': detector_prefix + 'AcquireTime',
    'acquire_period': detector_prefix + 'AcquirePeriod',
    'acquire': detector_prefix + 'Acquire',
    'status_message': detector_prefix + 'StatusMessage_RBV',
    'TIFF_base_name': TIFF_prefix + 'FileName_RBV',
    'TIFF_next_number': TIFF_prefix + 'FileNumber_RBV',
}

detector_values = {
    'status_message_ok': 'OK',
}
