import os.path as path
from datetime import datetime, timedelta
from typing import Any
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
from particle_filter.script.log import Log
from script.fingerprint import Fingerprint
from script.window import Window


def _set_main_params(conf: dict[str, Any]) -> None:
    global BEGIN, END, LOG_FILE, FP_BEGIN, FP_END, FP_LOG_FILE, RESULT_DIR_NAME

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    LOG_FILE = str(conf["log_file"])
    FP_BEGIN = datetime.strptime(conf["fp_begin"], "%Y-%m-%d %H:%M:%S")
    FP_END = datetime.strptime(conf["fp_end"], "%Y-%m-%d %H:%M:%S")
    FP_LOG_FILE = str(conf["fp_log_file"])
    RESULT_DIR_NAME = None if conf["result_dir_name"] is None else str(conf["result_dir_name"])

def fingerprinting(conf: dict[str, Any], enable_show: bool = True) -> None:
    log = Log(BEGIN, END, path.join(pf_param.ROOT_DIR, "log/observed/", LOG_FILE))
    fp_log = Log(FP_BEGIN + timedelta(seconds=pf_param.WIN_SIZE), FP_END, path.join(pf_param.ROOT_DIR, "log/observed/", FP_LOG_FILE))
    result_dir = pf_util.make_result_dir(RESULT_DIR_NAME)
    fp = Fingerprint(FP_BEGIN, FP_END, fp_log, result_dir)

    if pf_param.ENABLE_DRAW_BEACONS:
        fp.draw_beacons(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        fp.init_recorder()

    t = BEGIN
    while t <= END:
        print(f"main.py: {t.time()}")

        estim_pos = fp.estim_pos(Window(t, fp_log.mac_list, log).rssi_list)
        
        if not np.isnan(estim_pos[0]):    # if not lost
            fp.draw_pos(estim_pos)
        if pf_param.ENABLE_SAVE_VIDEO:
            fp.record()
        if enable_show:
            fp.show()

        t += timedelta(seconds=pf_param.WIN_STRIDE)
    
    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        fp.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        fp.save_video()
    if pf_param.ENABLE_WRITE_CONF:
        pf_util.write_conf(conf, result_dir)
    if enable_show:
        fp.show(0)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")
    parser.add_argument("--no_display", action="store_true", help="run without display")
    args = parser.parse_args()

    conf = set_params(args.conf_file)
    _set_main_params(conf)

    fingerprinting(conf, not args.no_display)
