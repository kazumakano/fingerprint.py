import os.path as path
from datetime import datetime, timedelta
import numpy as np
import particle_filter.script.parameter as pf_param
from particle_filter.script.log import Log
from script.fingerprint import Fingerprint
from script.window import Window


def _set_main_params(conf: dict) -> None:
    global BEGIN, END, LOG_FILE, FP_BEGIN, FP_END, FP_LOG_FILE

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    LOG_FILE = str(conf["log_file"])
    FP_BEGIN = datetime.strptime(conf["fp_begin"], "%Y-%m-%d %H:%M:%S")
    FP_END = datetime.strptime(conf["fp_end"], "%Y-%m-%d %H:%M:%S")
    FP_LOG_FILE = str(conf["log_file"])

def fingerprint() -> None:
    log = Log(BEGIN, END, path.join(pf_param.ROOT_DIR, "log/observed/", LOG_FILE))
    fp_log = Log(FP_BEGIN + timedelta(seconds=pf_param.WIN_SIZE), FP_END, path.join(pf_param.ROOT_DIR, "log/observed/", FP_LOG_FILE))
    fp = Fingerprint(FP_BEGIN, FP_END, fp_log)

    if pf_param.ENABLE_DRAW_BEACONS:
        fp.draw_beacons(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        fp.init_recorder()

    t = BEGIN
    while t <= END:
        print(f"main.py: {t.time()}")
        win = Window(t, fp_log.mac_list, log)

        estim_pos = fp.estim_pos(win.rssi_list)
        
        if not np.isnan(estim_pos[0]):    # if not lost
            fp.draw_pos(estim_pos)
            fp.show()
        if pf_param.ENABLE_SAVE_VIDEO:
            fp.record()

        t += timedelta(seconds=pf_param.WIN_STRIDE)
    
    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        fp.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        fp.save_video()
    fp.show(0)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")

    _set_main_params(set_params(parser.parse_args().conf_file))

    fingerprint()
