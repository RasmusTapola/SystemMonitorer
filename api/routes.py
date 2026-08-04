from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .crud import save_metrics
from .database import get_db
from .schemas import MetricsIn

router = APIRouter()

@router.post("/metrics")
def receive_metrics(metrics: MetricsIn, db: Session = Depends(get_db)):
    measurement = save_metrics(db, metrics)

    return {
        "status": "ok",
        "measurement_id": measurement.id,
        "agent_id": measurement.agent_id,
    }
