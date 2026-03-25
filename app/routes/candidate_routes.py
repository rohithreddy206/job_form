from fastapi import APIRouter, Request, Form, UploadFile, File, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os
from app.config.settings import settings
from app.utils.file_helpers import validate_file
from app.services.candidate_service import CandidateService
from app.database.connection import get_db

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(settings.BASE_DIR, "templates"))

@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    """Render the candidate application form."""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/submit")
async def submit_form(
    request: Request,
    db: Session = Depends(get_db),
    first_name: str = Form(None),
    last_name: str = Form(None),
    phone_number: str = Form(...),
    email: str = Form(...),
    current_location: str = Form(""),
    current_company: str = Form(""),
    total_experience: int = Form(0),
    relevant_experience: int = Form(0),
    education: str = Form(""),
    current_ctc: float = Form(0.0),
    expected_ctc: float = Form(0.0),
    notice_period: str = Form(""),
    reason_for_job_change: str = Form(""),
    comments: str = Form(""),
    resume: UploadFile = File(...),
):
    """Handle form submission: validate, save file, insert into DB."""
    
    # ── Validate required fields ──────────────────────────────────
    errors = []
    if not phone_number.strip():
        errors.append("Phone number is required.")
    if not email.strip() or "@" not in email:
        errors.append("A valid email address is required.")

    # ── Validate resume ───────────────────────────────────────────
    file_error = validate_file(resume)
    if file_error:
        errors.append(file_error)

    if errors:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "errors": errors},
            status_code=422,
        )

    # ── Read & size-check file ────────────────────────────────────
    file_bytes = await resume.read()
    if len(file_bytes) > settings.MAX_FILE_SIZE_BYTES:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "errors": ["Resume file must be under 5 MB."]},
            status_code=422,
        )

    # ── Save file to disk ─────────────────────────────────────────
    resume_path = await CandidateService.save_resume(file_bytes, resume.filename)

    # ── Insert using SQLAlchemy ───────────────────────────────────
    candidate_data = {
        "first_name": first_name.strip() if first_name else "",
        "last_name": last_name.strip() if last_name else "",
        "phone_number": phone_number.strip(),
        "email": email.strip(),
        "current_location": current_location.strip(),
        "current_company": current_company.strip(),
        "total_experience": total_experience,
        "relevant_experience": relevant_experience,
        "education": education.strip(),
        "current_ctc": current_ctc,
        "expected_ctc": expected_ctc,
        "notice_period": notice_period.strip(),
        "reason_for_job_change": reason_for_job_change.strip(),
        "comments": comments.strip()
    }
    
    success = CandidateService.create_candidate(db, candidate_data, resume_path)
    
    if not success:
        print("[WARNING] Could not save to DB.")

    # ── Render success page ───────────────────────────────────────
    return templates.TemplateResponse(
        "success.html",
        {"request": request, "full_name": f"{first_name} {last_name}".strip() or email},
    )
