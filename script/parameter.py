import os.path as path
from typing import Union
import numpy as np
from particle_filter.script.parameter import set_params as set_pf_params


def _set_fingerprint_params(conf: dict) -> None:
    global USE_BEACON_POINT, SCAN_SPAN, MARGIN_SPAN, SET_POINTS_POLICY, XLIM, YLIM

    USE_BEACON_POINT = conf["use_beacon_point"]         # use beacon as scan point or not
    SCAN_SPAN = int(conf["scan_span"])                  # length of span to scan [s]
    MARGIN_SPAN = int(conf["margin_span"])              # length of span to prepare [s]
    SET_POINTS_POLICY = conf["set_points_policy"]       # 1: ground truth of trajectory, 2: scan point file
    XLIM = conf["xlim"]                                 # default width limitation for map image
    YLIM = conf["ylim"]                                 # default height limitation for map image

def _set_segment_params(conf: dict) -> None:
    global SEG_POLICY, MIN_COUNT

    SEG_POLICY = np.int8(conf["seg_policy"])            # 1: median, 2: mode
    MIN_COUNT = int(conf["min_reception_count"])        # minimum count of signal reception to rely RSSI

def set_params(conf_file: Union[str, None] = None) -> dict:
    global ROOT_DIR

    ROOT_DIR = path.dirname(__file__) + "/../"       # project root directory

    if conf_file is None:
        conf_file = ROOT_DIR + "config/default.yaml"    # load default file if not specified
    else:
        conf_file = conf_file

    conf = set_pf_params(conf_file)
    _set_fingerprint_params(conf)
    _set_segment_params(conf)

    return conf
