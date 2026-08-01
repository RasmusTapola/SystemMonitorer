from fastapi import APIRouter
from .schemas import Metrics

router = APIRouter()

@router.post("/metrics")
async def receive_metrics(metrics: Metrics):
    print(metrics)

    return {"status": "ok"}