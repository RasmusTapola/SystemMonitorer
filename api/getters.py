from sqlalchemy.orm import Session

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

def get_agent_metrics(agent_id: int, db: Session) -> list[Measurement]:

    return (
        db.query(Measurement)
        .filter(Measurement.agent_id == agent_id)
        .order_by(Measurement.timestamp.desc())
        .all()
    )

    

def get_latest_metrics(agent_id: int, db: Session) -> list[Measurement]:
    
    return (
        db.query(Measurement)
        .filter(Measurement.agent_id == agent_id)
        .order_by(Measurement.timestamp.desc())
        .first()
    )
    