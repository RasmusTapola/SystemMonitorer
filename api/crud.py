from sqlalchemy.orm import Session

from .models import Agent, Measurement
from .schemas import MetricsIn


def save_metrics(db: Session, metrics: MetricsIn) -> Measurement:
    agent = (
        db.query(Agent)
        .filter(Agent.hostname == metrics.hostname)
        .first()
    )

    if agent is None:
        agent = Agent(
            hostname=metrics.hostname,
            ipaddress=metrics.ipaddress,
            os=metrics.os,
            kernel=metrics.kernel,
            last_seen=metrics.timestamp,
        )
        db.add(agent)
        db.flush()
    else:
        agent.ipaddress = metrics.ipaddress
        agent.os = metrics.os
        agent.kernel = metrics.kernel
        agent.last_seen = metrics.timestamp

    measurement = Measurement(
        agent_id=agent.id,
        timestamp=metrics.timestamp,
        cpu=metrics.cpuUse,
        memory=metrics.memUse,
        disk=metrics.diskUsage,
        network_in=metrics.networkTrfIn,
        network_out=metrics.networkTrfOut,
    )

    try:
        db.add(measurement)
        db.commit()
        db.refresh(measurement)
    except Exception:
        db.rollback()
        raise

    return measurement
