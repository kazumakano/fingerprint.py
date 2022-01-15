import os.path as path
import warnings
from datetime import datetime, timedelta
from typing import Any
import cv2
import numpy as np
import particle_filter.script.parameter as pf_param
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from particle_filter.script.log import Log
from particle_filter.script.map import Map
from scipy.interpolate import griddata
from . import parameter as param
from . import utility as util
from .segment import get_seg_rssi_list


class Fingerprint(Map):
    def __init__(self, begin: datetime, end: datetime, log: Log) -> None:
        global RSSI_AT_BEACON

        if begin > end:
            raise Exception("log.py: log range is wrong")

        if param.USE_BEACON_POINTS:
            RSSI_AT_BEACON = np.float16(util.calc_rssi_by_dist(0))    # RSSI at points directly under beacon

        super().__init__(log.mac_list)

        scan_span = timedelta(seconds=param.SCAN_SPAN)
        entire_span = scan_span + timedelta(seconds=param.MARGIN_SPAN)
        point_num = (end - begin) // entire_span    # number of points to scan
        print(f"fingerprint.py: the number of scan points is {point_num}")

        self._set_points(point_num)
        self._set_rssis(begin, entire_span, log, point_num, scan_span)
        self._create_fingerprint(log)

    def _set_points(self, point_num: int) -> None:
        if param.SET_POINTS_POLICY == 1:      # load from ground truth trajectory
            pass    # not implemented yet
        elif param.SET_POINTS_POLICY == 2:    # load from scan point file
            self.point_poses = np.loadtxt(path.join(param.ROOT_DIR, "map/point.csv"), dtype=np.float16, delimiter=",")

        if len(self.point_poses) != point_num:
            raise Exception(f"fingerprint.py: the number of scan points is expected to be {point_num} but {len(self.point_poses)} points were loaded")

        print("fingerprint.py: scan points has been loaded")

    def _set_rssis(self, begin: datetime, entire_span: timedelta, log: Log, point_num: int, scan_span: timedelta) -> None:
        self.rssi_lists = np.empty((point_num, len(log.mac_list)), dtype=np.float16)

        t = begin
        for i in range(point_num):
            self.rssi_lists[i] = get_seg_rssi_list(t, log, scan_span)
            t += entire_span
        
        print(f"fingerprint.py: RSSI has been loaded")

    def _create_heatmap(self, beacon_index: int) -> np.ndarray:
        valid_point_poses = np.empty((0, 2), dtype=np.float16)    # positions of points where RSSI is valid
        valid_rssi = np.empty(0, dtype=np.float16)
        if param.USE_BEACON_POINTS:
            valid_point_poses = np.vstack((valid_point_poses, self.beacon_pos_list[beacon_index]))
            valid_rssi = np.hstack((valid_rssi, RSSI_AT_BEACON))
        for i, p in enumerate(self.point_poses):
            if not np.isneginf(self.rssi_lists[i, beacon_index]):    # if RSSI of specified beacon at the point is valid
                valid_point_poses = np.vstack((valid_point_poses, p))
                valid_rssi = np.hstack((valid_rssi, self.rssi_lists[i, beacon_index]))
        try:
            return griddata(valid_point_poses, valid_rssi, tuple(np.array(np.meshgrid(range(self.img.shape[0]), range(self.img.shape[1])), dtype=np.uint16)), method="cubic")
        except:
            print(f"fingerprint.py: heatmap of given MAC address was not successfully created probably because of its fewness of valid points {valid_point_poses}")
            warnings.simplefilter("ignore", category=UserWarning)

            return np.full(self.img.shape[:2], np.nan, dtype=np.float64)

    def _create_fingerprint(self, log: Log) -> None:
        self.grid_list = np.empty((len(log.mac_list), self.img.shape[0], self.img.shape[1]), dtype=np.float64)
        for i in range(len(log.mac_list)):
            self.grid_list[i] = self._create_heatmap(i)

    def draw_points(self, is_never_cleared: bool = False) -> None:
        for p in self.point_poses:
            self._draw_pos((128, 128, 128), is_never_cleared, p)

    def draw_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_pos((0, 0, 255), False, pos)

    def estim_pos(self, rssi_list: np.ndarray) -> np.ndarray:
        lh_grid = np.zeros(self.img.shape[:2], dtype=np.float64)
        for i, r in enumerate(rssi_list):
            lh_grid += util.get_likelihood_grid(self.grid_list[i], r)
        max_lh: np.float64 = lh_grid.max()

        return np.full(2, np.nan, dtype=np.float16) if max_lh == 0 else np.argwhere(lh_grid == max_lh).mean(axis=0).astype(np.float16)[::-1]

    def show_with_heatmap(self, mac: str, mac_list: np.ndarray, enable_lim: bool = False, xlim: Any = None, ylim: Any = None) -> None:
        if mac not in mac_list:
            raise Warning("fingerprint.py: given MAC address was not found in log")

        ax = plt.subplots(figsize=(16, 16))[1]
        cax: plt.Axes = make_axes_locatable(ax).append_axes("right", 0.2, pad=0.1)    # create axis for colorbar
        print("cax", type(cax))
        for i, m in enumerate(mac_list):
            if m == mac:
                img = cv2.circle(self.img.copy(), self.beacon_pos_list[i].astype(int), 3, (0, 0, 255), 6)
                if enable_lim:
                    if xlim is None:
                        xlim = param.XLIM
                    if ylim is None:
                        ylim = param.YLIM
                    ax.imshow(cv2.cvtColor(img[ylim[0]:ylim[1], xlim[0]:xlim[1]], cv2.COLOR_BGR2RGB))    # limit size and convert color space
                    aximg: plt.AxesImage = ax.imshow(self.grid_list[i, ylim[0]:ylim[1], xlim[0]:xlim[1]], cmap="jet", alpha=0.5)
                    print("aximg", type(aximg))
                    plt.colorbar(mappable=aximg, cax=cax)
                else:
                    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                    aximg: plt.AxesImage = ax.imshow(self.grid_list[i], cmap="jet", alpha=0.5)
                    plt.colorbar(mappable=aximg, cax=cax)
                break
