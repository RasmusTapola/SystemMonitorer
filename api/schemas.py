from pydantic import BaseModel
from datetime import datetime

class ProcessIn(BaseModel):
    name: str
    pid: int
    cpu: float
    memory: float

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
    networkInMbps: float
    networkOutMbps: float
    processes: list[ProcessIn]

class AgentsIn(BaseModel):
    hostname: str
    ipaddress: str
    os: str
    kernel: str


