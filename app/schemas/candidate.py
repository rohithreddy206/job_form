from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CandidateBase(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    phone_number: str
    email: EmailStr
    current_location: Optional[str] = ""
    current_company: Optional[str] = ""
    total_experience: Optional[int] = 0
    relevant_experience: Optional[int] = 0
    education: Optional[str] = ""
    current_ctc: Optional[float] = 0.0
    expected_ctc: Optional[float] = 0.0
    notice_period: Optional[str] = ""
    reason_for_job_change: Optional[str] = ""
    comments: Optional[str] = ""

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(CandidateBase):
    pass

class CandidateResponse(CandidateBase):
    sr_no: int
    resume_path: str
    created_at: str

    class Config:
        from_attributes = True
