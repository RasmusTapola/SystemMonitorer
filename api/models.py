from sqlalchemy import ForeignKey, Float, DateTime, String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .database import Base

class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(primary_key=True)

    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    agent_name: Mapped[str] = mapped_column(String(100))

    hostname: Mapped[str] = mapped_column(String(100))

    ipaddress: Mapped[str] = mapped_column(String(50))

    os: Mapped[str] = mapped_column(String(100))

    kernel: Mapped[str] = mapped_column(String(100))

    measurements: Mapped[list["Measurement"]] = relationship(
        back_populates="agent",
        cascade="all, delete-orphan"
    )

class Measurement(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)

    agent_id: Mapped[int] = mapped_column(
        ForeignKey("agents.id")
    )

    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    cpu: Mapped[float]

    memory: Mapped[float]

    disk: Mapped[float]

    network_in: Mapped[int] = mapped_column(BigInteger)

    network_out: Mapped[int] = mapped_column(BigInteger)

    network_in_mbps: Mapped[float]

    network_out_mbps: Mapped[float]

    agent: Mapped["Agent"] = relationship(
        back_populates="measurements"
    )

    processes: Mapped[list["Process"]] = relationship(
        back_populates="measurement",
        cascade="all, delete-orphan"
    )

class Process(Base):
    __tablename__= "processes"

    id: Mapped[int] = mapped_column(primary_key=True)

    pid: Mapped[int] = mapped_column(Integer)

    name: Mapped[str] = mapped_column(String(255))

    measurement_id: Mapped[int] = mapped_column(
        ForeignKey("measurements.id")
    )

    cpu: Mapped[float]

    memory: Mapped[float]

    measurement: Mapped["Measurement"] = relationship(
        back_populates="processes"
    )
