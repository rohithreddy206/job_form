import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.config.settings import settings
from app.utils.file_helpers import get_safe_filename

class CandidateService:
    @staticmethod
    async def save_resume(file_bytes: bytes, original_filename: str) -> str:
        """Save the resume to disk and return the file path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = get_safe_filename(original_filename, timestamp)
        file_path = os.path.join(settings.UPLOAD_DIR, filename)

        with open(file_path, "wb") as f:
            f.write(file_bytes)
        
        return file_path

    @staticmethod
    def create_candidate(db: Session, candidate_data: dict, resume_path: str) -> bool:
        """Insert a new candidate into the database using SQLAlchemy."""
        try:
            db_candidate = Candidate(
                first_name=candidate_data.get('first_name'),
                last_name=candidate_data.get('last_name'),
                phone_number=candidate_data.get('phone_number'),
                email=candidate_data.get('email'),
                current_location=candidate_data.get('current_location'),
                current_company=candidate_data.get('current_company'),
                total_experience=candidate_data.get('total_experience', 0),
                relevant_experience=candidate_data.get('relevant_experience', 0),
                education=candidate_data.get('education'),
                current_ctc=candidate_data.get('current_ctc', 0.0),
                expected_ctc=candidate_data.get('expected_ctc', 0.0),
                notice_period=candidate_data.get('notice_period'),
                reason_for_job_change=candidate_data.get('reason_for_job_change'),
                comments=candidate_data.get('comments'),
                resume_path=resume_path
            )
            db.add(db_candidate)
            db.commit()
            db.refresh(db_candidate)
            print(f"[DB] Candidate '{db_candidate.first_name} {db_candidate.last_name}' saved successfully.")
            return True
        except Exception as e:
            print(f"[DB ERROR] {e}")
            db.rollback()
            return False
