import os.path as path
from typing import Union
import numpy as np
from particle_filter.script.parameter import set_params as set_pf_params


def _set_fingerprint_params(conf: dict) -> None:
    global MARGIN_SPAN, SCAN_SPAN, SET_POINTS_POLICY, USE_BEACON_POINTS, XLIM, YLIM

    MARGIN_SPAN = float(conf["margin_span"])
    SCAN_SPAN = float(conf["scan_span"])
    SET_POINTS_POLICY = np.int8(conf["set_points_policy"])
    USE_BEACON_POINTS = bool(conf["use_beacon_points"])
    XLIM = np.array(conf["xlim"], dtype=np.int16)
    YLIM = np.array(conf["ylim"], dtype=np.int16)

def _set_segment_params(conf: dict) -> None:
    global MIN_COUNT, SEG_POLICY

    MIN_COUNT = np.uint8(conf["min_reception_count"])
    SEG_POLICY = np.int8(conf["seg_policy"])

def set_params(conf_file: Union[str, None] = None) -> dict:
    global ROOT_DIR

    ROOT_DIR = path.join(path.dirname(__file__), "../")

    if conf_file is None:
        conf_file = path.join(ROOT_DIR, "config/default.yaml")

    conf = set_pf_params(conf_file)
    _set_fingerprint_params(conf)
    _set_segment_params(conf)

    return conf
