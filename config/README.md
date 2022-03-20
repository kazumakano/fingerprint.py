# config
This is directory for config files.
Put your config files here.
You can customize following parameters:
| Key                  | Description                                        | Notes                                                                | Type          |
| ---                  | ---                                                | ---                                                                  | ---           |
| begin                | begin datetime of RSSI log                         | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| end                  | end datetime of RSSI log                           | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| log_file             | RSSI log file                                      |                                                                      | `str`         |
| fp_begin             | begin datetime of RSSI log for fingerprinting      | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| fp_end               | end datetime of RSSI log for fingerprinting        | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| fp_log_file          | RSSI log file for fingerprinting                   |                                                                      | `str`         |
| result_dir_name      | name of directory for result files                 | auto generated if unspecified                                        | `str \| None` |
|                      |                                                    |                                                                      |               |
| win_size             | size of sliding window [s]                         |                                                                      | `float`       |
|                      |                                                    |                                                                      |               |
| beacon_dir           | directory for beacon config files                  |                                                                      | `str`         |
| enable_clear_map     | clear map image at each step or not                |                                                                      | `bool`        |
| enable_draw_beacons  | draw beacon positions or not                       |                                                                      | `bool`        |
| enable_save_img      | capture image at last or not                       |                                                                      | `bool`        |
| enable_save_video    | record video or not                                |                                                                      | `bool`        |
| frame_rate           | frame rate of video [fps]                          | synchronized with real speed if 0                                    | `float`       |
| map_conf_file        | map config file                                    |                                                                      | `str`         |
| map_img_file         | map image file                                     |                                                                      | `str`         |
| map_show_range       | range to show map                                  | whole map if unspecified                                             | `list[int]`   |
| win_stride           | stride width of sliding window [s]                 |                                                                      | `float`       |
|                      |                                                    |                                                                      |               |
| truth_log_file       | ground truth position log file                     | disabled if unspecified                                              | `str \| None` |
|                      |                                                    |                                                                      |               |
| el_correction        | correction term for difference in elevation [m]    |                                                                      | `float`       |
| enable_write_conf    | write config file or not                           |                                                                      | `bool`        |
| propag_coef          | propagation coefficient                            | takes 2 in ideal environment                                         | `float`       |
|                      |                                                    |                                                                      |               |
| win_policy           | policy to get representative RSSI value in window  | 1: maximum, 2: latest                                                | `int`         |
|                      |                                                    |                                                                      |               |
| margin_span          | length of span to prepare for next scan [s]        |                                                                      | `float`       |
| scan_span            | length of span to scan [s]                         |                                                                      | `float`       |
| set_points_policy    | policy to set points                               | 1: ground truth trajectory, 2: scan point file                       | `int`         |
| use_beacon_points    | use beacon positions as scan points or not         |                                                                      | `bool`        |
|                      |                                                    |                                                                      |               |
| min_reception_count  | minimum count of packet reception to rely RSSI     |                                                                      | `int`         |
| seg_policy           | policy to get representative RSSI value in segment | 1: median, 2: mode                                                   | `int`         |
