# Usage

This image is similar to [esanchezm/prometheus-qbittorrent-exporter](https://github.com/esanchezm/prometheus-qbittorrent-exporter) except this decodes the data from qBittorrent's config file and exports the all time data. The previously mentioned exporter only exports the current session data as these stats are not available via the API.

This "all time data" is the total data downloaded, total data uploaded, and the share ratio.

Once this is setup, expect the following metrics to be available:

```text
qbittorrent_dl_info_all_time_data_total
qbittorrent_up_info_all_time_data_total
qbittorrent_info_all_time_share_ratio_total
```

I would (and do) use this in conjunction with [esanchezm/prometheus-qbittorrent-exporter](https://github.com/esanchezm/prometheus-qbittorrent-exporter). Import the dashboard.json file into Grafana and you'll have a nice dashboard. I've switched out the "current session" data for the "all time" data on my dashboard.

![](./dashboard.png)

## Docker Run

```bash
docker run \
  -v /path/to/qbittorrent/config:/app \
  -p 9200:9200 \
  adamhebden/prom-qbittorrent-alltime-stats:alpine-latest
```

### Change the PORT

The default port is 9200, but you can change it by setting the PORT environment variable. Don't forget to expose the port.

```bash
docker run \
  -v /path/to/qbittorrent/config:/config \
  -e PORT=9177 \
  -p 9177:9177 \
  adamhebden/prom-qbittorrent-alltime-stats:alpine-latest
```

## Docker Compose
```yaml
  # QBittorrent All Time Exporter
  qbittorrent-alltime-exporter:
    image: adamhebden/prom-qbittorrent-alltime-stats:alpine-latest
    container_name: qbittorrent-alltime-exporter
    security_opt:
      - no-new-privileges:true
    restart: unless-stopped
    volumes:
      - /path/to/qbittorrent/config:/config
```

For the volume, all that matters is qBittorrent-data.conf is in the root of the volume.

## Images
https://hub.docker.com/r/adamhebden/prom-qbittorrent-alltime-stats/tags

 - arm64v8: `adamhebden/prom-qbittorrent-alltime-stats:alpine-latest`
    - or: `adamhebden/prom-qbittorrent-alltime-stats:alpine-v1.0.0`
 - amd64: `adamhebden/prom-qbittorrent-alltime-stats:latest`
    - or: `adamhebden/prom-qbittorrent-alltime-stats:v1.0.0`

## Prometheus Setup

```yaml
  - job_name: 'qbittorrent-alltime-exporter'
    static_configs:
      - targets: ['qbittorrent-alltime-exporter:9200']
```

## Example Metrics

```text
# HELP qbittorrent_dl_info_all_time_data_total All Time Total Data Downloaded
# TYPE qbittorrent_dl_info_all_time_data_total counter
qbittorrent_dl_info_all_time_data_total 8.06438490048e+011
# HELP qbittorrent_up_info_all_time_data_total All Time Total Data Uploaded
# TYPE qbittorrent_up_info_all_time_data_total counter
qbittorrent_up_info_all_time_data_total 1.276814893325e+012
# HELP qbittorrent_info_all_time_share_ratio_total All Time Share Ratio
# TYPE qbittorrent_info_all_time_share_ratio_total counter
qbittorrent_info_all_time_share_ratio_total 1.58327623
```
