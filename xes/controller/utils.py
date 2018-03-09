try:
    from epics import caput, caget
except ImportError:
    exit(2)

from .epics_config import detector_pvs, detector_values
import time


def caput_pil(pv, value, wait=True):
    t0 = time.time()
    caput(pv, value, wait=wait)

    while time.time() - t0 < 20.0:
        time.sleep(0.02)
        if detector_values['status_message_ok'] in caget(detector_pvs['status_message'], as_string=True):
            return True
    return False
