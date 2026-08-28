import os
import requests

url = os.getenv("API_URL", "http://127.0.0.1:8000/metrics")


def send_metrics(data):

    try:
        response = requests.post(url, json=data, timeout=5)

        if response.status_code != 200:
            print(response.text)

        return response.status_code
    except requests.RequestException as error:
        print(f"failed to send metrics: {error}")
        return None