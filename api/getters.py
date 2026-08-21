from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from .models import Agent, Measurement


def get_agent_by_id(agent_id: int, db: Session) -> Agent:
    return (
        db.query(Agent)
        .filter(Agent.id == agent_id)
        .first()
    )

def get_agents(db: Session) -> list[Agent]:
    return  (
        db.query(Agent)
        .order_by(Agent.hostname)
        .all()
    )


def get_health_status(db: Session) -> list[Agent]:

    return (
        db.query(Agent)
        .order_by(Agent.last_seen)
        .all()
    )

def get_agent_metrics(agent_id: int, minutes: int, db: Session) -> list[Measurement]:

    since = datetime.now() - timedelta(minutes=minutes)

    return (
        db.query(Measurement)
        .filter(Measurement.agent_id == agent_id)
        .filter(Measurement.timestamp >= since)
        .order_by(Measurement.timestamp.desc())
        .all()
    )

    

def get_latest_metrics(agent_id: int, db: Session) -> Measurement | None:
    
    return (
        db.query(Measurement)
        .filter(Measurement.agent_id == agent_id)
        .order_by(Measurement.timestamp.desc())
        .first()
    )
    