motor_pvs = {
    'theta': '13IDD:m40.VAL',
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
    'set_TIFF_base_dir': TIFF_prefix + 'FilePath',
    'set_TIFF_base_name': TIFF_prefix + 'FileName',
    'set_TIFF_next_number': TIFF_prefix + 'FileNumber',
    'TIFF_base_dir': TIFF_prefix + 'FilePath_RBV',
    'TIFF_base_name': TIFF_prefix + 'FileName_RBV',
    'TIFF_next_number': TIFF_prefix + 'FileNumber_RBV',
    'roi_left': ROI_prefix + 'MinY',
    'roi_range': ROI_prefix + 'SizeY',
    'roi_start': ROI_prefix + 'MinX',
    'roi_width': ROI_prefix + 'SizeX',
    'roi_total_counts': '13IDC-PIL:Stats1:Total_RBV',
    'comments': '13IDC-PIL:AcquireSequence.STRA',
    'detector_shutter_control': '13IDC-PIL:cam1:ShutterMode',
}

detector_values = {
    'status_message_ok': 'OK',
    'detector_shutter_control_epics_pv': '1',
    'detector_shutter_control_none': '0',
}

beam_pvs = {
    'IC1': '13IDA:mono_pid1.CVAL',
    'IC2': '13IDD:userTran1.P',
    'APS': 'S:SRcurrentAI.VAL',
}

general_pvs = {
    'table_shutter': '13IDD:Unidig1Bo11',
    'table_shutter_status': '13IDD:Unidig1Bi11'
}

general_values = {
    'table_shutter_open': '0',
    'table_shutter_close': '1',
    'table_shutter_status_open': 0,
    'table_shutter_status_closed': 1,

}