#!/usr/bin/env python3
import os
import time
from PyQt5.QtCore import QSettings
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, CounterMetricFamily

class QBittorrentAllTimeStats(object):
    def __init__(self):
        pass
    def collect(self):
        settings = QSettings('/config/qBittorrent-data.conf', QSettings.IniFormat)

        configData  = settings.value("Stats/AllStats")
        allTimeUp   = configData['AlltimeUL']
        allTimeDown = configData['AlltimeDL']
        ratio       = round(allTimeUp / allTimeDown, 8)

        dl_info_all_time_data_total = CounterMetricFamily('qbittorrent_dl_info_all_time_data_total', 'All Time Total Data Downloaded')
        up_info_all_time_data_total = CounterMetricFamily('qbittorrent_up_info_all_time_data_total', 'All Time Total Data Uploaded')
        info_all_time_share_ratio   = CounterMetricFamily('qbittorrent_info_all_time_share_ratio', 'All Time Share Ratio')

        dl_info_all_time_data_total.add_metric([], int(allTimeDown))
        up_info_all_time_data_total.add_metric([], int(allTimeUp))
        info_all_time_share_ratio.add_metric([], float(ratio))

        yield dl_info_all_time_data_total
        yield up_info_all_time_data_total
        yield info_all_time_share_ratio

if __name__ == "__main__":
    start_http_server(int(os.environ.get('PORT', 9200)))
    REGISTRY.register(QBittorrentAllTimeStats())
    while True:
        # period between collection
        time.sleep(5)
