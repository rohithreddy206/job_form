from sqlalchemy import Column, Integer, String, Float, Text, DateTime, func
from app.database.connection import Base

class Candidate(Base):
    __tablename__ = "candidates"

    sr_no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone_number = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    current_location = Column(String(100), nullable=True)
    current_company = Column(String(100), nullable=True)
    total_experience = Column(Integer, default=0)
    relevant_experience = Column(Integer, default=0)
    education = Column(String(50), nullable=True)
    current_ctc = Column(Float, default=0.0)
    expected_ctc = Column(Float, default=0.0)
    notice_period = Column(String(50), nullable=True)
    reason_for_job_change = Column(Text, nullable=True)
    comments = Column(Text, nullable=True)
    resume_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
