import subprocess

api = subprocess.Popen([
    "uvicorn", 
    "api.main:app", 
    "--reload"
])

agent = subprocess.Popen([
    "python", 
    "agent/main.py"
])

api.wait()
agent.wait()