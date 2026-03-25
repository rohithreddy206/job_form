import os
from fastapi import UploadFile
from typing import Optional
from app.config.settings import settings

def validate_file(file: UploadFile) -> Optional[str]:
    """Return an error message string if invalid, else None."""
    if not file or not file.filename:
        return "Resume file is required."

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        return f"Invalid file type '.{ext}'. Only PDF, DOC, and DOCX are allowed."

    return None

def get_safe_filename(original_filename: str, timestamp: str) -> str:
    """Generate a safe filename with a timestamp prefix."""
    safe_name = original_filename.replace(" ", "_")
    return f"{timestamp}_{safe_name}"
