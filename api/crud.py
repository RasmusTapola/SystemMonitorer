from sqlalchemy.orm import Session

from .models import Agent, Measurement, Process
from .schemas import MetricsIn


def save_metrics(db: Session, metrics: MetricsIn) -> Measurement:
    agent = (
        db.query(Agent)
        .filter(Agent.agent_name == metrics.agentName)
        .first()
    )

    if agent is None:
        agent = Agent(
            agent_name=metrics.agentName,
            hostname=metrics.hostname,
            ipaddress=metrics.ipaddress,
            os=metrics.os,
            kernel=metrics.kernel,
            last_seen=metrics.timestamp,
        )
        db.add(agent)
        db.flush()
    else:
        agent.agent_name = metrics.agentName
        agent.ipaddress = metrics.ipaddress
        agent.os = metrics.os
        agent.kernel = metrics.kernel
        agent.last_seen = metrics.timestamp

    processes = [
        Process(
            pid=process.pid,
            name=process.name,
            cpu=process.cpu,
            memory=process.memory,
        )
        for process in metrics.processes
    ]

    measurement = Measurement(
        agent_id=agent.id,
        timestamp=metrics.timestamp,
        cpu=metrics.cpuUse,
        memory=metrics.memUse,
        disk=metrics.diskUsage,
        network_in=metrics.networkTrfIn,
        network_out=metrics.networkTrfOut,
        network_in_mbps=metrics.networkInMbps,
        network_out_mbps=metrics.networkOutMbps,
        processes=processes,
    )

    try:
        db.add(measurement)
        db.commit()
        db.refresh(measurement)
    except Exception:
        db.rollback()
        raise

    return measurement
