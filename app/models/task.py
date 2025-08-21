import enum
import uuid
from sqlalchemy import Column, Integer, String, Enum as SqlEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from app.db.base import Base


class TaskStatus(enum.Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    uuid = Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(
        SqlEnum(TaskStatus), default=TaskStatus.CREATED, nullable=False
    )


__all__ = ["Task", "TaskStatus"]
