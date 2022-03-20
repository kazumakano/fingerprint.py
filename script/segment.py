from datetime import datetime, timedelta
from statistics import multimode
import numpy as np
from particle_filter.script.log import Log
from . import parameter as param


def get_seg_rssi_list(current: datetime, log: Log, scan_span: timedelta) -> np.ndarray:
    rssi_list = np.full(len(log.mac_list), -np.inf, dtype=np.float32)    # list of typical RSSI in this segment
    all_rssi = np.empty(len(log.mac_list), dtype=np.ndarray)
    for i in range(len(log.mac_list)):
        all_rssi[i] = np.empty(0, dtype=np.int8)

    ts, mac, rssi = log.slice(current + scan_span, scan_span)    # get segment of (current, current + scan_span)

    for i in range(len(ts)):
        for j, m in enumerate(log.mac_list):
            if m == mac[i]:
                all_rssi[j] = np.hstack((all_rssi[j], rssi[i]))
                break

    if param.SEG_POLICY == 1:      # use median of RSSI
        for i, l in enumerate(all_rssi):
            if len(l) > param.MIN_COUNT:    # ignore unreliable data
                rssi_list[i] = np.float32(np.median(l))
    elif param.SEG_POLICY == 2:    # use mode of RSSI
        for i, l in enumerate(all_rssi):
            if len(l) > param.MIN_COUNT:
                rssi_list[i] = np.float32(np.median(multimode(l)))

    return rssi_list
