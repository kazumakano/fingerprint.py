import math
import numpy as np
import particle_filter.script.parameter as pf_param


# calculate RSSI backward by distance-RSSI relation
def calc_rssi_by_dist(dist: float) -> float:
    return -10 * pf_param.PROPAG_COEF * math.log10(dist + pf_param.EL_CORRECTION) - 68

def get_likelihood_grid(heatmap: np.ndarray, rssi: np.float16) -> np.ndarray:
    if np.isneginf(rssi):
        return np.zeros(heatmap.shape, dtype=np.float64)
    else:
        return np.where(np.isnan(heatmap), 0, 1 / np.abs(heatmap - rssi))
