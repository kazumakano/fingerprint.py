import math
import numpy as np
import particle_filter.script.parameter as pf_param


# calculate RSSI backward by distance-RSSI relation
def calc_rssi_by_dist(dist: float) -> float:
    return -10 * pf_param.PROPAG_COEF * math.log10(dist + pf_param.EL_CORRECTION) - 68
