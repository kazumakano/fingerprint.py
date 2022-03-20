# fingerprint.py
This is Python module to generate RSSI heatmaps and estimate subject's position with them.

## Usage
### main.py
You can run with following command.
You can specify config file with `--conf_file` flag.
`config/default.yaml` will be used if unspecified.
Set `--no_display` flag to run without showing map.
```sh
python main.py [--conf_file PATH_TO_CONF_FILE] [--no_display]
```
