import time

from .collector import collect_metrics
from .sender import send_metrics

while True:

    data = collect_metrics()

    print(data)

    status = send_metrics(data)

    print(status)

    time.sleep(5)