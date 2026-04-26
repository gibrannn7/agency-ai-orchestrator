import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Numeric, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LeadStatus(Base):
    __tablename__ = "lead_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_email = Column(String, nullable=False)
    subject = Column(Text, nullable=True)
    classification = Column(String, nullable=False)  # 'LEAD', 'SPAM', 'SUPPORT', 'IGNORE'
    budget_estimation = Column(Numeric(15, 2), nullable=True)
    is_processed = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class SystemLogs(Base):
    __tablename__ = "system_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String, nullable=False, index=True)
    log_level = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class ProjectSyncStatus(Base):
    __tablename__ = "project_sync_status"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clickup_task_id = Column(String, nullable=True)
    folder_id = Column(String, nullable=True)
    client_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
