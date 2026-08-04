from pydantic import BaseModel
from datetime import datetime

class MetricsIn(BaseModel):
    hostname: str
    ipaddress: str
    os: str
    kernel: str
    timestamp: datetime
    cpuUse: float
    memUse: float
    diskUsage: float
    networkTrfIn: int
    networkTrfOut: int

class AgentsIn(BaseModel):
    hostname: str
    ipaddress: str
    os: str
    kernel: str

class ProcessIn(BaseModel):
    id: int
    name: str
    pid: int
    cpu: float
    memory: float
