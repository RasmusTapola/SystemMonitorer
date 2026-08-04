import psutil
from datetime import datetime
import logging
import socket
import platform
import time

networkInMbps = None
networkOutMbps = None
previous_time = None

def collect_metrics():
    global networkOutMbps
    global networkInMbps
    global previous_time

    cpuUsage = psutil.cpu_percent(interval=1)
    logging.info(f"Cpu usage is {cpuUsage}")

    memUsage = psutil.virtual_memory()
    logging.info(f"Memory Usage is {memUsage}")

    diskUsage = psutil.disk_usage("/")
    logging.info(f"Disk usage is {diskUsage}")

    networkTrf = psutil.net_io_counters()
    logging.info(f"Received Network Traffic is {networkTrf.bytes_recv} and sent is {networkTrf.bytes_sent}")

    ts = datetime.now().isoformat()

    mbps_in = 0.0
    mbps_out = 0.0

    if networkInMbps is not None and networkOutMbps is not None:
        time_elapsed = time.monotonic() - previous_time

        bytes_delta_in = networkTrf.bytes_recv - networkInMbps
        bytes_delta_out = networkTrf.bytes_sent - networkOutMbps

        mbps_in = (bytes_delta_in / time_elapsed * 8) / 1_000_000
        mbps_out = (bytes_delta_out / time_elapsed * 8) / 1_000_000

    networkInMbps = networkTrf.bytes_recv
    networkOutMbps = networkTrf.bytes_sent
    previous_time = time.monotonic()

    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)

    os_name = platform.system()
    kernel = platform.release()

    top_procs = collect_top_processes()

    return {
            "hostname": hostname,
            "ipaddress": ipaddress,
            "os": os_name,
            "kernel": kernel,
    
            "timestamp": ts,
            "cpuUse": cpuUsage,
            "memUse": memUsage.percent,
            "diskUsage": diskUsage.percent,
            "networkTrfIn": networkTrf.bytes_recv,
            "networkTrfOut": networkTrf.bytes_sent,
            "networkInMbps": mbps_in,
            "networkOutMbps": mbps_out,

            "processes": top_procs
        }


def collect_top_processes(limit=5):

    proc = []
    
    for process in psutil.process_iter(["pid", "name"]):
        try:
            process.cpu_percent(None)
            proc.append(process)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    time.sleep(0.2)

    measured = []

    for process in proc:
        try:
            cpu = process.cpu_percent(None)
            memory = process.memory_info().rss / (1024 * 1024)

            measured.append({
                "pid": process.pid,
                "name": process.name(),
                "cpu": cpu,
                "memory": memory
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    measured.sort(
        key=lambda process: process["cpu"],
        reverse=True
    )

    return measured[:limit]
