import psutil
import time


def systemMonitorer():
    cpuUsage = psutil.cpu_percent(interval=1)
    print(f"Cpu usage is {cpuUsage}")

    memUsage = psutil.virtual_memory()
    print(f"Memory Usage is {memUsage}")

    diskUsage = psutil.disk_usage("/")
    print(f"Disk usage is {diskUsage}")

    networkTrf = psutil.net_io_counters()
    print(f"Received Network Traffic is {networkTrf.bytes_recv} and sent is {networkTrf.bytes_sent}")

systemMonitorer()