import subprocess
import sys

api = subprocess.Popen([
    sys.executable,
    "-m",
    "uvicorn", 
    "api.main:app", 
    "--reload"
])
'''
agent = subprocess.Popen([
    sys.executable, 
    "-m",
    "agent.main"
])
'''
api.wait()
#agent.wait()