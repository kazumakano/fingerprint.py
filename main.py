import argparse
import datetime
from datetime import datetime, timedelta
import numpy as np
import particle_filter.script.parameter as pf_param
from particle_filter.script.log import Log
from script.fingerprint import Fingerprint
from script.parameter import set_params
from script.window import Window


def _set_main_params(conf: dict) -> None:
    global BEGIN, END, FP_LOG_BEGIN, FP_LOG_END

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    FP_LOG_BEGIN = datetime.strptime(conf["fp_log_begin"], "%Y-%m-%d %H:%M:%S")
    FP_LOG_END = datetime.strptime(conf["fp_log_end"], "%Y-%m-%d %H:%M:%S")

def fingerprint() -> None:
    log = Log(BEGIN, END)
    fp_log = Log(FP_LOG_BEGIN + timedelta(seconds=pf_param.WIN_SIZE), FP_LOG_END)
    fp = Fingerprint(fp_log, FP_LOG_BEGIN, FP_LOG_END)

    if pf_param.ENABLE_DRAW_BEACONS:
        fp.draw_beacons(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        fp.init_recorder()

    t = BEGIN
    while t <= END:
        print(f"main.py: {t.time()}")
        win = Window(log, fp_log.mac_list, t)

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify your config file", metavar="PATH_TO_CONFIG_FILE")

    conf = set_params(parser.parse_args().config)
    _set_main_params(conf)

    fingerprint()
