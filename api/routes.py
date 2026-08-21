from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .crud import save_metrics
from .database import get_db
from .schemas import MetricsIn
from .getters import get_agents, get_agent_by_id, get_latest_metrics, get_agent_metrics

router = APIRouter()

@router.post("/metrics")
def receive_metrics(metrics: MetricsIn, db: Session = Depends(get_db)):
    measurement = save_metrics(db, metrics)

    return {
        "status": "ok",
        "measurement_id": measurement.id,
        "agent_id": measurement.agent_id,
    }

@router.get("/health")
def list_health():

    return{
        "status": "ok"
    }

@router.get("/agents")
def list_agents(db: Session = Depends(get_db)):
    agents = get_agents(db)

    if agents is None:
        raise HTTPException(
            status_code=404,
            detail="No measurements found for this agent"
        )
        

    return[
        {
            "id": agent.id,
            "hostname": agent.hostname,
            "ipaddress": agent.ipaddress,
            "os": agent.os,
            "kernel": agent.kernel,
            "last_seen": agent.last_seen,
        }
        for agent in agents
    ]

@router.get("/agents/{agent_id}")
def list_agent_by_id(agent_id: int, db: Session = Depends(get_db)):
    agent = get_agent_by_id(agent_id, db)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {
        "id": agent.id,
        "hostname": agent.hostname,
        "ipaddress": agent.ipaddress,
        "os": agent.os,
        "kernel": agent.kernel,
        "last_seen": agent.last_seen,
    }

@router.get("/agents/{agent_id}/latest")
def list_latest_metrics(agent_id: int, db: Session = Depends(get_db)):
    measurement = get_latest_metrics(agent_id, db)

    if measurement is None:
        raise HTTPException(
            status_code=404,
            detail="No measurements found for this agent"
        )
    
    return {
        "id": measurement.id,
        "agent_id": measurement.agent_id,
        "timestamp": measurement.timestamp,
        "cpu": measurement.cpu,
        "memory": measurement.memory,
        "disk": measurement.disk,
        "network_in": measurement.network_in,
        "network_out": measurement.network_out,
        "network_in_mbps": measurement.network_in_mbps,
        "network_out_mbps": measurement.network_out_mbps,
        "processes": [
            {
                "id": process.id,
                "pid": process.pid,
                "name": process.name,
                "cpu": process.cpu,
                "memory": process.memory,
            }
            for process in measurement.processes
        ],
    }

@router.get("/agents/{agent_id}/measurements")
def list_agent_metrics(
    agent_id: int, 
    minutes: int = 15,
    db: Session = Depends(get_db)):
    
    measurements = get_agent_metrics(agent_id, minutes, db)

    return [
        {
            "id": measurement.id,
            "agent_id": measurement.agent_id,
            "timestamp": measurement.timestamp,
            "cpu": measurement.cpu,
            "memory": measurement.memory,
            "disk": measurement.disk,
            "network_in": measurement.network_in,
            "network_out": measurement.network_out,
            "network_in_mbps": measurement.network_in_mbps,
            "network_out_mbps": measurement.network_out_mbps,
            "processes": [
                {
                    "id": process.id,
                    "pid": process.pid,
                    "name": process.name,
                    "cpu": process.cpu,
                    "memory": process.memory,
                }
                for process in measurement.processes
            ],
        }
        for measurement in measurements
    ]