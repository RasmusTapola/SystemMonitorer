import requests

url = "http://127.0.0.1:8000/metrics"

def send_metrics(data):

    response = requests.post(url, json=data)

    return response.status_code