from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from app.database import get_db
from app import models, schemas, crud, auth, utils

router = APIRouter(prefix="/recruiter", tags=["recruiter"])

templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
async def recruiter_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    if not recruiter:
        raise HTTPException(status_code=400, detail="Recruiter profile not found")
        
    jobs = crud.get_recruiter_jobs(db, recruiter.recruiter_id)
    job_ids = [j.job_id for j in jobs]
    
    # 1. Total Stats
    total_jobs = len(jobs)
    
    total_applicants = 0
    shortlisted = 0
    rejected = 0
    selected = 0
    
    if job_ids:
        total_applicants = db.query(models.Application).filter(models.Application.job_id.in_(job_ids)).count()
        shortlisted = db.query(models.Application).filter(models.Application.job_id.in_(job_ids), models.Application.status == "Shortlisted").count()
        rejected = db.query(models.Application).filter(models.Application.job_id.in_(job_ids), models.Application.status == "Rejected").count()
        selected = db.query(models.Application).filter(models.Application.job_id.in_(job_ids), models.Application.status == "Selected").count()
        
    # 2. Average AI Score
    avg_score = 0.0
    if job_ids:
        avg_score_res = db.query(func.avg(models.AIScore.final_score)).filter(models.AIScore.job_id.in_(job_ids)).scalar()
        if avg_score_res:
            avg_score = round(float(avg_score_res), 2)
            
    # 3. Top 5 Candidates by AI score
    top_candidates = []
    if job_ids:
        top_scores = db.query(models.AIScore).filter(models.AIScore.job_id.in_(job_ids)).order_by(desc(models.AIScore.final_score)).limit(5).all()
        for ts in top_scores:
            app = db.query(models.Application).filter(models.Application.candidate_id == ts.candidate_id, models.Application.job_id == ts.job_id).first()
            if app:
                top_candidates.append({
                    "candidate": ts.candidate,
                    "job": ts.job,
                    "final_score": ts.final_score,
                    "recommendation": ts.recommendation,
                    "status": app.status
                })
                
    # 4. Recent Applications
    recent_apps = []
    if job_ids:
        db_recent_apps = db.query(models.Application).filter(models.Application.job_id.in_(job_ids)).order_by(desc(models.Application.applied_at)).limit(5).all()
        for ra in db_recent_apps:
            score_rec = crud.get_ai_score(db, ra.candidate_id, ra.job_id)
            recent_apps.append({
                "application": ra,
                "candidate": ra.candidate,
                "job": ra.job,
                "ai_score": score_rec.final_score if score_rec else None
            })
            
    return templates.TemplateResponse(
        request,
        "recruiter/dashboard.html",
        {
            "current_user": current_user,
            "active_tab": "dashboard",
            "recruiter": recruiter,
            "stats": {
                "total_jobs": total_jobs,
                "total_applicants": total_applicants,
                "shortlisted": shortlisted,
                "rejected": rejected,
                "selected": selected,
                "avg_score": avg_score
            },
            "top_candidates": top_candidates,
            "recent_applications": recent_apps
        }
    )

# --- Jobs Management ---

@router.get("/jobs")
async def list_jobs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    jobs = crud.get_recruiter_jobs(db, recruiter.recruiter_id)
    
    # Calculate applicant counts for each job
    jobs_with_count = []
    for j in jobs:
        count = db.query(models.Application).filter(models.Application.job_id == j.job_id).count()
        jobs_with_count.append((j, count))
        
    return templates.TemplateResponse(
        request,
        "recruiter/jobs_list.html",
        {
            "current_user": current_user,
            "active_tab": "jobs",
            "jobs_with_count": jobs_with_count
        }
    )

@router.get("/jobs/new")
async def new_job_form(
    request: Request,
    current_user: models.User = Depends(auth.require_recruiter)
):
    return templates.TemplateResponse(
        request,
        "recruiter/job_form.html",
        {
            "current_user": current_user,
            "active_tab": "post_job",
            "job": None
        }
    )

@router.post("/jobs/new")
async def create_job(
    title: str = Form(...),
    department: str = Form(...),
    description: str = Form(...),
    required_skills: str = Form(None),
    min_experience: int = Form(0),
    min_education: str = Form(None),
    preferred_certifications: str = Form(None),
    weight_resume: float = Form(0.1),
    weight_skills: float = Form(0.2),
    weight_coding: float = Form(0.2),
    weight_technical: float = Form(0.2),
    weight_hr: float = Form(0.1),
    weight_projects: float = Form(0.1),
    weight_certifications: float = Form(0.1),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    job_in = schemas.JobCreate(
        title=title,
        department=department,
        description=description,
        required_skills=required_skills,
        min_experience=min_experience,
        min_education=min_education,
        preferred_certifications=preferred_certifications,
        weight_resume=weight_resume,
        weight_skills=weight_skills,
        weight_coding=weight_coding,
        weight_technical=weight_technical,
        weight_hr=weight_hr,
        weight_projects=weight_projects,
        weight_certifications=weight_certifications
    )
    crud.create_job(db, job_in, recruiter.recruiter_id)
    return RedirectResponse(url="/recruiter/jobs?message=JobPostedSuccessfully", status_code=303)

@router.get("/jobs/edit/{job_id}")
async def edit_job_form(
    job_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    job = crud.get_job(db, job_id)
    if not job or job.recruiter_id != recruiter.recruiter_id:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return templates.TemplateResponse(
        request,
        "recruiter/job_form.html",
        {
            "current_user": current_user,
            "active_tab": "jobs",
            "job": job
        }
    )

@router.post("/jobs/edit/{job_id}")
async def update_job(
    job_id: int,
    title: str = Form(...),
    department: str = Form(...),
    description: str = Form(...),
    required_skills: str = Form(None),
    min_experience: int = Form(0),
    min_education: str = Form(None),
    preferred_certifications: str = Form(None),
    weight_resume: float = Form(0.1),
    weight_skills: float = Form(0.2),
    weight_coding: float = Form(0.2),
    weight_technical: float = Form(0.2),
    weight_hr: float = Form(0.1),
    weight_projects: float = Form(0.1),
    weight_certifications: float = Form(0.1),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    db_job = crud.get_job(db, job_id)
    if not db_job or db_job.recruiter_id != recruiter.recruiter_id:
        raise HTTPException(status_code=404, detail="Job not found")
        
    job_update = schemas.JobCreate(
        title=title,
        department=department,
        description=description,
        required_skills=required_skills,
        min_experience=min_experience,
        min_education=min_education,
        preferred_certifications=preferred_certifications,
        weight_resume=weight_resume,
        weight_skills=weight_skills,
        weight_coding=weight_coding,
        weight_technical=weight_technical,
        weight_hr=weight_hr,
        weight_projects=weight_projects,
        weight_certifications=weight_certifications
    )
    crud.update_job(db, db_job, job_update)
    
    # Recalculate AI scores for all applications since weights/requirements changed
    apps = crud.get_applications_for_job(db, job_id)
    for app in apps:
        try:
            crud.calculate_and_save_ai_score(db, app.candidate_id, job_id)
        except Exception:
            pass
            
    return RedirectResponse(url="/recruiter/jobs?message=JobUpdatedSuccessfully", status_code=303)

@router.post("/jobs/delete/{job_id}")
async def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    db_job = crud.get_job(db, job_id)
    if not db_job or db_job.recruiter_id != recruiter.recruiter_id:
        raise HTTPException(status_code=404, detail="Job not found")
        
    crud.delete_job(db, db_job)
    return RedirectResponse(url="/recruiter/jobs?message=JobDeletedSuccessfully", status_code=303)

# --- Applicant Management ---

@router.get("/jobs/{job_id}/applicants")
async def list_applicants(
    job_id: int,
    request: Request,
    status_filter: Optional[str] = None,
    score_filter: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    job = crud.get_job(db, job_id)
    if not job or job.recruiter_id != recruiter.recruiter_id:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Get all applications
    query = db.query(models.Application).filter(models.Application.job_id == job_id)
    
    # Filter by Status
    if status_filter:
        query = query.filter(models.Application.status == status_filter)
        
    # Search by Name or Skill
    if search:
        search_term = f"%{search}%"
        query = query.join(models.Candidate).filter(
            (models.Candidate.full_name.like(search_term)) | 
            (models.Candidate.skills.like(search_term))
        )
        
    applications = query.all()
    
    # Process applications with their AI scores
    applicants_data = []
    for app in applications:
        ai_score = crud.get_ai_score(db, app.candidate_id, job_id)
        
        # Recalculate if missing
        if not ai_score:
            try:
                ai_score = crud.calculate_and_save_ai_score(db, app.candidate_id, job_id)
            except Exception:
                pass
                
        # Score Filter
        if score_filter and ai_score:
            val = ai_score.final_score
            if score_filter == "75+" and val < 75: continue
            elif score_filter == "50-74" and (val < 50 or val >= 75): continue
            elif score_filter == "sub50" and val >= 50: continue
            
        applicants_data.append({
            "application": app,
            "candidate": app.candidate,
            "ai_score": ai_score
        })
        
    # Sort applicants data by final AI score descending
    applicants_data.sort(key=lambda x: x["ai_score"].final_score if x["ai_score"] else -1, reverse=True)
    
    return templates.TemplateResponse(
        request,
        "recruiter/applicants_list.html",
        {
            "current_user": current_user,
            "active_tab": "jobs",
            "job": job,
            "applicants": applicants_data,
            "filters": {
                "status": status_filter or "",
                "score": score_filter or "",
                "search": search or ""
            }
        }
    )

@router.get("/candidate/{candidate_id}/job/{job_id}")
async def candidate_details(
    candidate_id: int,
    job_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    job = crud.get_job(db, job_id)
    if not job or job.recruiter_id != recruiter.recruiter_id:
        raise HTTPException(status_code=404, detail="Job not found")
        
    candidate = crud.get_candidate(db, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    application = db.query(models.Application).filter(
        models.Application.candidate_id == candidate_id,
        models.Application.job_id == job_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    assessment = crud.get_or_create_assessment(db, candidate_id, job_id)
    ai_score = crud.get_ai_score(db, candidate_id, job_id)
    if not ai_score:
        ai_score = crud.calculate_and_save_ai_score(db, candidate_id, job_id)
        
    notes = crud.get_notes_for_candidate_job(db, candidate_id, job_id)
    
    return templates.TemplateResponse(
        request,
        "recruiter/candidate_details.html",
        {
            "current_user": current_user,
            "active_tab": "jobs",
            "job": job,
            "candidate": candidate,
            "application": application,
            "assessment": assessment,
            "ai_score": ai_score,
            "notes": notes
        }
    )

@router.post("/candidate/{candidate_id}/job/{job_id}/scores")
async def update_candidate_scores(
    candidate_id: int,
    job_id: int,
    coding_score: float = Form(...),
    aptitude_score: float = Form(...),
    technical_score: float = Form(...),
    hr_score: float = Form(...),
    project_score: float = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    assessment = crud.get_or_create_assessment(db, candidate_id, job_id)
    score_update = schemas.AssessmentCreateOrUpdate(
        coding_score=coding_score,
        aptitude_score=aptitude_score,
        technical_score=technical_score,
        hr_score=hr_score,
        project_score=project_score
    )
    crud.update_assessment(db, assessment, score_update)
    
    # Recalculate AI score
    crud.calculate_and_save_ai_score(db, candidate_id, job_id)
    
    return RedirectResponse(
        url=f"/recruiter/candidate/{candidate_id}/job/{job_id}?message=AssessmentScoresUpdatedSuccessfully",
        status_code=303
    )

@router.post("/candidate/{candidate_id}/job/{job_id}/status")
async def update_application_status(
    candidate_id: int,
    job_id: int,
    status: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    app = db.query(models.Application).filter(
        models.Application.candidate_id == candidate_id,
        models.Application.job_id == job_id
    ).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    crud.update_application_status(db, app, status)
    return RedirectResponse(
        url=f"/recruiter/candidate/{candidate_id}/job/{job_id}?message=ApplicationStatusUpdatedTo{status}",
        status_code=303
    )

@router.post("/candidate/{candidate_id}/job/{job_id}/note")
async def add_recruiter_note(
    candidate_id: int,
    job_id: int,
    note_text: str = Form(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    crud.create_note(db, recruiter.recruiter_id, candidate_id, job_id, note_text)
    return RedirectResponse(
        url=f"/recruiter/candidate/{candidate_id}/job/{job_id}?message=NoteAddedSuccessfully",
        status_code=303
    )

# --- Printable Candidate Report ---

@router.get("/candidate/{candidate_id}/job/{job_id}/report")
async def candidate_report(
    candidate_id: int,
    job_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    candidate = crud.get_candidate(db, candidate_id)
    job = crud.get_job(db, job_id)
    if not candidate or not job:
        raise HTTPException(status_code=404, detail="Data not found")
        
    application = db.query(models.Application).filter(
        models.Application.candidate_id == candidate_id,
        models.Application.job_id == job_id
    ).first()
    
    assessment = crud.get_assessment(db, candidate_id, job_id)
    ai_score = crud.get_ai_score(db, candidate_id, job_id)
    notes = crud.get_notes_for_candidate_job(db, candidate_id, job_id)
    
    return templates.TemplateResponse(
        request,
        "recruiter/candidate_report.html",
        {
            "current_user": current_user,
            "candidate": candidate,
            "job": job,
            "application": application,
            "assessment": assessment,
            "ai_score": ai_score,
            "notes": notes
        }
    )

# --- Side-by-Side Comparison ---

@router.get("/jobs/{job_id}/compare")
async def compare_candidates(
    job_id: int,
    request: Request,
    candidate_ids: str = "", # Comma-separated ids
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    job = crud.get_job(db, job_id)
    if not job or job.recruiter_id != recruiter.recruiter_id:
        raise HTTPException(status_code=404, detail="Job not found")
        
    ids = [int(x.strip()) for x in candidate_ids.split(",") if x.strip().isdigit()]
    
    comparison_data = []
    for cid in ids:
        cand = crud.get_candidate(db, cid)
        if cand:
            ass = crud.get_assessment(db, cid, job_id)
            score = crud.get_ai_score(db, cid, job_id)
            if not score:
                try:
                    score = crud.calculate_and_save_ai_score(db, cid, job_id)
                except Exception:
                    pass
            comparison_data.append({
                "candidate": cand,
                "assessment": ass,
                "ai_score": score
            })
            
    return templates.TemplateResponse(
        request,
        "recruiter/compare.html",
        {
            "current_user": current_user,
            "active_tab": "jobs",
            "job": job,
            "candidates": comparison_data
        }
    )
