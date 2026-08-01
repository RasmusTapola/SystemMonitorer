import psutil
import time
import logging
import json
import datetime
from subprocess import call
from prettytable import PrettyTable


def systemMonitorer():
    while True:
        cpuUsage = psutil.cpu_percent(interval=1)
        logging.info(f"Cpu usage is {cpuUsage}")

        memUsage = psutil.virtual_memory()
        logging.info(f"Memory Usage is {memUsage}")

        diskUsage = psutil.disk_usage("/")
        logging.info(f"Disk usage is {diskUsage}")

        networkTrf = psutil.net_io_counters()
        logging.info(f"Received Network Traffic is {networkTrf.bytes_recv} and sent is {networkTrf.bytes_sent}")

        ts = datetime.datetime.now()

        process_table = PrettyTable(['PID', 'PNAME', 'STATUS',
                                 'CPU', 'NUM THREADS', 'MEMORY(MB)'])

        proc = []

        for pid in psutil.pids()[-200:]:
            try:
                p = psutil.Process(pid)
                p.cpu_percent()
                proc.append(p)
            except:
                pass

        top = {}
        for p in proc:
            top[p] = p.cpu_percent() / psutil.cpu_count()

        toplist = sorted(top.items(), key=lambda x: x[1])
        top10 = toplist[-10:]
        top10.reverse()

        for p, cpu_percent in top10:

            try:
                # oneshot to improve info retrieve efficiency
                with p.oneshot():
                    
                    process_table.add_row([
                        str(p.pid),
                        p.name(),
                        p.status(),
                        f'{cpu_percent:.2f}' + "%",
                        p.num_threads(),
                        f'{p.memory_info().rss / 1e6:.3f}'
                    ])

            except Exception as e:
                pass
        print(process_table)

        data = {
            "timestamp" : str(ts),
            "cpuUse" : cpuUsage,
            "memUse" : memUsage.percent,
            "diskUsage" : diskUsage.percent,
            "networkTrfIn" : networkTrf.bytes_recv,
            "networkTrfOut" : networkTrf.bytes_sent
        }

        json_data = json.dumps(data, indent=2)

        print(json_data)

systemMonitorer()