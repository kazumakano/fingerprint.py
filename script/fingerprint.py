import warnings
from datetime import datetime, timedelta
from typing import Any
import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.image import AxesImage
from matplotlib.pyplot import Axes
from mpl_toolkits.axes_grid1 import make_axes_locatable
from particle_filter.script.log import Log
from particle_filter.script.map import Map
from scipy.interpolate import griddata
from . import parameter as param
from . import utility as util
from .segment import get_seg_rssi_list


class Fingerprint(Map):
    def __init__(self, log: Log, begin: datetime, end: datetime) -> None:
        global RSSI_AT_BEACON

        if param.USE_BEACON_POINT:
            RSSI_AT_BEACON = util.calc_rssi_by_dist(0)    # RSSI at point directly under beacon

        super().__init__(log)

        scan_span = timedelta(seconds=param.SCAN_SPAN)
        entire_span = scan_span + timedelta(seconds=param.MARGIN_SPAN)
        point_num = (end - begin) // entire_span    # the number of points to scan
        print(f"fingerprint.py: the number of scan points is {point_num}")

        self._set_points(point_num)
        self._set_rssi(log, point_num, begin, scan_span, entire_span)

    def _set_points(self, point_num: int) -> None:
        if param.SET_POINTS_POLICY == 1:      # load from grand truth of trajectory
            pass
        elif param.SET_POINTS_POLICY == 2:    # load from scan point file
            self.point_poses: np.ndarray = np.loadtxt(param.ROOT_DIR + "map/point.csv", dtype=np.float16, delimiter=",")

        if len(self.point_poses) != point_num:
            raise Exception(f"fingerprint.py: the number of scan points is expected to be {point_num} but {len(self.point_poses)} points were loaded")

        print("fingerprint.py: scan points has been loaded")

    def _set_rssi(self, log: Log, point_num: int, begin: datetime, scan_span: timedelta, entire_span: timedelta) -> None:
        self.rssi_lists = np.empty((point_num, len(log.mac_list)), dtype=np.float16)

        t = begin
        for i in range(point_num):
            self.rssi_lists[i] = get_seg_rssi_list(log, t, scan_span)
            t += entire_span
        
        print(f"fingerprint.py: RSSI has been loaded")

    def draw_points(self) -> None:
        for p in self.point_poses:
            cv2.circle(self.img, p.astype(int), 3, (128, 128, 128), 6)

    def _create_heatmap(self, beacon_index: int) -> np.ndarray:
        valid_point_poses = np.empty((0, 2), dtype=np.float16)    # positions of points where RSSI is valid
        valid_rssi = np.empty(0, dtype=np.float16)
        if param.USE_BEACON_POINT:
            valid_point_poses = np.vstack((valid_point_poses, self.beacon_pos_list[beacon_index]))
            valid_rssi = np.hstack((valid_rssi, np.float16(RSSI_AT_BEACON)))
        for i, p in enumerate(self.point_poses):
            if not np.isneginf(self.rssi_lists[i, beacon_index]):    # if RSSI of specified beacon at the point is valid
                valid_point_poses = np.vstack((valid_point_poses, p))
                valid_rssi = np.hstack((valid_rssi, self.rssi_lists[i, beacon_index]))
        try:
            return griddata(valid_point_poses, valid_rssi, tuple(np.meshgrid(range(self.img.shape[0]), range(self.img.shape[1]))), method="cubic")
        except:
            print("fingerprint.py: heatmap of given beacon was not successfully created probably because of its fewness of valid points")
            print(f"fingerprint.py: valid point positions are {valid_point_poses}")
            warnings.simplefilter("ignore", category=UserWarning)

            return np.full((self.img.shape[0], self.img.shape[1]), np.nan)

    def show_with_heatmap(self, log: Log, mac: str, enable_lim: bool = False, xlim: Any = None, ylim: Any = None) -> None:
        if mac not in log.mac_list:
            raise Warning("fingerprint.py: given MAC address was not found in log")

        ax = plt.subplots(figsize=(16, 16))[1]
        cax: Axes = make_axes_locatable(ax).append_axes("right", 0.2, pad=0.1)    # create axis for colorbar
        for i, m in enumerate(log.mac_list):
            if m == mac:
                self.draw_any_pos(self.beacon_pos_list[i], (0, 0, 255))
                if enable_lim:
                    if xlim is None:
                        xlim = param.XLIM
                    if ylim is None:
                        ylim = param.YLIM
                    ax.imshow(cv2.cvtColor(self.img[ylim[0]:ylim[1], xlim[0]:xlim[1]], cv2.COLOR_BGR2RGB))    # limit size and convert color space
                    aximg: AxesImage = ax.imshow(self._create_heatmap(i)[ylim[0]:ylim[1], xlim[0]:xlim[1]], cmap="jet", alpha=0.5)
                    plt.colorbar(mappable=aximg, cax=cax)
                else:
                    ax.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
                    aximg: AxesImage = ax.imshow(self._create_heatmap(i), cmap="jet", alpha=0.5)
                    plt.colorbar(mappable=aximg, cax=cax)
                break
