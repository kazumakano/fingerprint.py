import math
import numpy as np
import particle_filter.script.parameter as pf_param
from scipy.stats import norm


# calculate RSSI backward by distance-RSSI relation
def calc_rssi_by_dist(dist: float) -> float:
    return -5 * pf_param.PROPAG_COEF * math.log10(dist ** 2 + pf_param.EL_CORRECTION ** 2) - 80

def get_likelihood_grid(heatmap: np.ndarray, rssi: np.float32) -> np.ndarray:
    return np.zeros(heatmap.shape, dtype=np.float64) if np.isneginf(rssi) else np.where(np.isnan(heatmap), 0, norm.pdf(rssi, loc=heatmap))
