import os
import shutil
from fastapi import APIRouter, Depends, Form, File, UploadFile, Request, HTTPException
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, crud, auth

router = APIRouter(prefix="/candidate", tags=["candidate"])

templates = Jinja2Templates(directory="app/templates")
UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "uploads"))

@router.get("/dashboard")
async def candidate_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_candidate)
):
    candidate = crud.get_candidate_by_user_id(db, current_user.id)
    if not candidate:
        # Auto-create if not exists for some reason
        candidate = crud.create_candidate_profile(db, current_user.id, current_user.name, current_user.email)
        
    applications = crud.get_candidate_applications(db, candidate.candidate_id)
    
    # Calculate profile completion %
    completeness = 0
    if candidate.phone: completeness += 10
    if candidate.location: completeness += 10
    if candidate.degree: completeness += 15
    if candidate.cgpa: completeness += 15
    if candidate.skills: completeness += 20
    if candidate.experience_years: completeness += 10
    if candidate.resume_path: completeness += 20
    
    # Aggregate statistics
    applied_count = len(applications)
    shortlisted_count = sum(1 for app in applications if app.status == "Shortlisted")
    selected_count = sum(1 for app in applications if app.status == "Selected")
    rejected_count = sum(1 for app in applications if app.status == "Rejected")
    
    return templates.TemplateResponse(
        request,
        "candidate/dashboard.html",
        {
            "current_user": current_user,
            "active_tab": "dashboard",
            "candidate": candidate,
            "applications": applications,
            "stats": {
                "applied": applied_count,
                "shortlisted": shortlisted_count,
                "selected": selected_count,
                "rejected": rejected_count,
                "completeness": completeness
            }
        }
    )

@router.get("/profile")
async def candidate_profile(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_candidate)
):
    candidate = crud.get_candidate_by_user_id(db, current_user.id)
    return templates.TemplateResponse(
        request,
        "candidate/profile.html",
        {
            "current_user": current_user,
            "active_tab": "profile",
            "candidate": candidate
        }
    )

@router.post("/profile/edit")
async def edit_candidate_profile(
    phone: str = Form(None),
    location: str = Form(None),
    degree: str = Form(None),
    cgpa: float = Form(None),
    skills: str = Form(None),
    experience_years: int = Form(0),
    certifications: str = Form(None),
    projects: str = Form(None),
    github_link: str = Form(None),
    linkedin_link: str = Form(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_candidate)
):
    candidate = crud.get_candidate_by_user_id(db, current_user.id)
    if not candidate:
        candidate = crud.create_candidate_profile(db, current_user.id, current_user.name, current_user.email)
        
    profile_update = schemas.CandidateUpdate(
        full_name=current_user.name,
        phone=phone,
        location=location,
        degree=degree,
        cgpa=cgpa,
        skills=skills,
        experience_years=experience_years,
        certifications=certifications,
        projects=projects,
        github_link=github_link,
        linkedin_link=linkedin_link
    )
    crud.update_candidate(db, candidate, profile_update)
    
    # Recalculate AI scores for all applications this candidate has submitted
    for app in candidate.applications:
        try:
            crud.calculate_and_save_ai_score(db, candidate.candidate_id, app.job_id)
        except Exception as e:
            pass
            
    return RedirectResponse(url="/candidate/profile?message=ProfileUpdatedSuccessfully", status_code=303)

@router.post("/profile/resume")
async def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_candidate)
):
    candidate = crud.get_candidate_by_user_id(db, current_user.id)
    if not candidate:
        candidate = crud.create_candidate_profile(db, current_user.id, current_user.name, current_user.email)
        
    # Verify file extension
    ext = os.path.splitext(resume.filename)[1].lower()
    if ext not in [".pdf", ".docx", ".doc"]:
        return RedirectResponse(url="/candidate/profile?error=UnsupportedFileTypeUsePDForWord", status_code=303)
        
    # Save the file
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"resume_{candidate.candidate_id}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)
        
    candidate.resume_path = f"/candidate/resume/download/{filename}"
    db.commit()
    
    # Recalculate AI scores since a new resume is uploaded
    for app in candidate.applications:
        try:
            crud.calculate_and_save_ai_score(db, candidate.candidate_id, app.job_id)
        except Exception as e:
            pass
            
    return RedirectResponse(url="/candidate/profile?message=ResumeUploadedSuccessfully", status_code=303)

@router.get("/resume/download/{filename}")
async def download_resume_file(
    filename: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Ensure file is only accessed by recruiters, admins, or the candidate owner
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
        
    # Verify permission
    # Candidate owner check
    if current_user.role == "candidate":
        candidate = crud.get_candidate_by_user_id(db, current_user.id)
        # Check if the filename belongs to this candidate
        expected_prefix = f"resume_{candidate.candidate_id}"
        if not filename.startswith(expected_prefix):
            raise HTTPException(status_code=403, detail="Access denied")
            
    return FileResponse(filepath, filename=filename)
