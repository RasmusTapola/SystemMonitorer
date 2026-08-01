from pydantic import BaseModel
from datetime import datetime

class Metrics(BaseModel):
    timestamp: datetime
    cpuUse: float
    memUse: float
    diskUsage: float
    networkTrfIn: int
    networkTrfOut: int