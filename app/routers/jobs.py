from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import models, crud, auth

import os

router = APIRouter(prefix="/jobs", tags=["jobs"])

templates_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")
templates = Jinja2Templates(directory=templates_path)

@router.get("")
async def browse_jobs(
    request: Request,
    search: Optional[str] = None,
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional)
):
    query = db.query(models.Job)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Job.title.like(search_term)) | 
            (models.Job.description.like(search_term)) |
            (models.Job.required_skills.like(search_term))
        )
        
    if department:
        query = query.filter(models.Job.department == department)
        
    jobs = query.all()
    
    # Get list of unique departments for filters
    departments = db.query(models.Job.department).distinct().all()
    departments = [d[0] for d in departments if d[0]]
    
    # If logged in as candidate, check which jobs they've applied for
    applied_job_ids = []
    candidate = None
    if current_user and current_user.role == "candidate":
        candidate = crud.get_candidate_by_user_id(db, current_user.id)
        if candidate:
            apps = crud.get_candidate_applications(db, candidate.candidate_id)
            applied_job_ids = [app.job_id for app in apps]
            
    return templates.TemplateResponse(
        request,
        "jobs/browse.html",
        {
            "current_user": current_user,
            "active_tab": "jobs",
            "jobs": jobs,
            "departments": departments,
            "applied_job_ids": applied_job_ids,
            "candidate": candidate,
            "filters": {
                "search": search or "",
                "department": department or ""
            }
        }
    )

@router.get("/{job_id}")
async def job_details(
    job_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(auth.get_current_user_optional)
):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    already_applied = False
    application = None
    candidate = None
    
    if current_user and current_user.role == "candidate":
        candidate = crud.get_candidate_by_user_id(db, current_user.id)
        if candidate:
            already_applied = crud.check_already_applied(db, candidate.candidate_id, job_id)
            if already_applied:
                application = db.query(models.Application).filter(
                    models.Application.candidate_id == candidate.candidate_id,
                    models.Application.job_id == job_id
                ).first()
                
    return templates.TemplateResponse(
        request,
        "jobs/details.html",
        {
            "current_user": current_user,
            "active_tab": "jobs",
            "job": job,
            "already_applied": already_applied,
            "application": application,
            "candidate": candidate
        }
    )

@router.post("/{job_id}/apply")
async def apply_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_candidate)
):
    candidate = crud.get_candidate_by_user_id(db, current_user.id)
    if not candidate:
        candidate = crud.create_candidate_profile(db, current_user.id, current_user.name, current_user.email)
        
    # Check completeness check or warning (optional, let's allow immediate apply but show a warning if skills or education are blank)
    # Check if already applied
    if crud.check_already_applied(db, candidate.candidate_id, job_id):
        return RedirectResponse(url=f"/jobs/{job_id}?error=YouHaveAlreadyAppliedForThisJob", status_code=303)
        
    # Create application
    crud.create_application(db, candidate.candidate_id, job_id)
    
    # Calculate initial AI score immediately upon application
    try:
        crud.calculate_and_save_ai_score(db, candidate.candidate_id, job_id)
    except Exception as e:
        print(f"Error calculating initial AI score: {e}")
        
    return RedirectResponse(url=f"/candidate/dashboard?message=AppliedSuccessfully", status_code=303)
