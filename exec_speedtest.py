#!/usr/bin/python

import speedtest
import time

from prometheus_client import start_http_server, Summary, Gauge

# If you want to test against a specific server
# 2020/02/23 command result
#$speedtest-cli --list | grep Japan
#
# 6087) Allied Telesis Capital Corporation (Fussa-shi, Japan)
# 6405) Allied Telesis Capital Corporation (Misawa, Japan)
# 6581) haza (Haebaru, Japan)
# 6766) JAIST(ino-lab) (Nomi, Japan)
# 7139) SoftEther Corporation (Tsukuba, Japan)
# 8407) Allied Telesis Capital Corporation (Sagamihara, Japan)
#14623) IPA CyberLab (Bunkyo, Japan)
#15047) OPEN Project (via 20G SINET) (Tokyo, Japan)
#18516) GIAM PING VIETPN.COM (Tokyo, Japan)
#18709) extride inc (Hitoyoshi, Japan)
#20976) GLBB Japan (Tokyo, Japan)
#21118) GLBB Japan (Naha, Japan)
#21569) i3D.net (Tokyo, Japan)
#24333) Rakuten Mobile , Inc (Tokyo, Japan)
#24774) Local24 Inc., (Kyoto, Japan)
#28910) fdcservers.net (Tokyo, Japan)
#30230) Lequios (Naha City, Japan)
servers = [14623]

test_interval = 600 # initiate speed test every 600 seconds

speedtest_upload = Gauge('speedtest_upload_speed', 'upload bandwidth in (bit/s)')
speedtest_download = Gauge('speedtest_download_speed', 'download bandwidth in (bit/s)')
speedtest_upload_bytes= Gauge('speedtest_upload_bytes', 'upload usage capacity (bytes)')
speedtest_download_bytes = Gauge('speedtest_download_bytes', 'download usage capacity (bytes)')
speedtest_ping = Gauge('speedtest_ping', 'icmp latency (ms)')

def process_request(t):

    stester = speedtest.Speedtest()
    stester.get_servers(servers)
    stester.get_best_server()

    stester.upload()
    stester.download()

    results_dict = stester.results.dict()

    speedtest_upload.set(results_dict["upload"])
    speedtest_download.set(results_dict["download"])
    speedtest_upload_bytes.set(results_dict["bytes_sent"])
    speedtest_download_bytes.set(results_dict["bytes_received"])
    speedtest_ping.set(results_dict["ping"])

    print("upload: %s" % (results_dict["upload"]))
    print("download: %s" % (results_dict["download"]))
    print("upload_bytes: %s" % (results_dict["bytes_sent"]))
    print("download_bytes: %s" % (results_dict["bytes_received"]))
    print("ping: %s" % (results_dict["ping"]))

    time.sleep(t)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(9104) 
    # Generate some requests.
    while True:
        try:
            process_request(test_interval)
        except TypeError:
            print("TypeError returned from speedtest server")
        except socket.timeout:
            print("socket.timeout returned from speedtest server")
