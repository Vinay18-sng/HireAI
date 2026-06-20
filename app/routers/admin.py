from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app import models, crud, auth

router = APIRouter(prefix="/admin", tags=["admin"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    # Aggregated system metrics
    total_recruiters = db.query(models.Recruiter).count()
    total_candidates = db.query(models.Candidate).count()
    total_jobs = db.query(models.Job).count()
    total_applications = db.query(models.Application).count()
    
    total_shortlisted = db.query(models.Application).filter(models.Application.status == "Shortlisted").count()
    total_selected = db.query(models.Application).filter(models.Application.status == "Selected").count()
    
    # Active recruiters list
    active_recruiters = db.query(models.Recruiter).join(models.User).limit(10).all()
    
    # Recent system logs/events (e.g. recent job postings)
    recent_jobs = db.query(models.Job).order_by(models.Job.created_at.desc()).limit(5).all()
    
    return templates.TemplateResponse(
        request,
        "admin/dashboard.html",
        {
            "current_user": current_user,
            "active_tab": "dashboard",
            "stats": {
                "recruiters": total_recruiters,
                "candidates": total_candidates,
                "jobs": total_jobs,
                "applications": total_applications,
                "shortlisted": total_shortlisted,
                "selected": total_selected
            },
            "active_recruiters": active_recruiters,
            "recent_jobs": recent_jobs
        }
    )

@router.get("/recruiters")
async def list_recruiters(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    recruiters = db.query(models.Recruiter).all()
    return templates.TemplateResponse(
        request,
        "admin/recruiters.html",
        {
            "current_user": current_user,
            "active_tab": "recruiters",
            "recruiters": recruiters
        }
    )

@router.get("/candidates")
async def list_candidates(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_admin)
):
    candidates = db.query(models.Candidate).all()
    return templates.TemplateResponse(
        request,
        "admin/candidates.html",
        {
            "current_user": current_user,
            "active_tab": "candidates",
            "candidates": candidates
        }
    )
