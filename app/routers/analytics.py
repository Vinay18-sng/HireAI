from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Any
from app.database import get_db
from app import models, auth, crud

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/jobs-applicants")
async def jobs_applicants_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    if not recruiter:
        raise HTTPException(status_code=400, detail="Recruiter not found")
        
    jobs = crud.get_recruiter_jobs(db, recruiter.recruiter_id)
    labels = []
    data = []
    
    for j in jobs:
        count = db.query(models.Application).filter(models.Application.job_id == j.job_id).count()
        labels.append(j.title)
        data.append(count)
        
    return {"labels": labels, "data": data}


@router.get("/status-breakdown")
async def status_breakdown_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    if not recruiter:
        raise HTTPException(status_code=400, detail="Recruiter not found")
        
    jobs = crud.get_recruiter_jobs(db, recruiter.recruiter_id)
    job_ids = [j.job_id for j in jobs]
    
    statuses = ["Applied", "Shortlisted", "Selected", "Rejected"]
    counts = []
    
    if job_ids:
        for status in statuses:
            count = db.query(models.Application).filter(
                models.Application.job_id.in_(job_ids),
                models.Application.status == status
            ).count()
            counts.append(count)
    else:
        counts = [0, 0, 0, 0]
        
    return {"labels": statuses, "data": counts}


@router.get("/score-distribution")
async def score_distribution_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    if not recruiter:
        raise HTTPException(status_code=400, detail="Recruiter not found")
        
    jobs = crud.get_recruiter_jobs(db, recruiter.recruiter_id)
    job_ids = [j.job_id for j in jobs]
    
    ranges = ["90-100", "80-89", "70-79", "60-69", "50-59", "<50"]
    counts = [0, 0, 0, 0, 0, 0]
    
    if job_ids:
        scores = db.query(models.AIScore.final_score).filter(models.AIScore.job_id.in_(job_ids)).all()
        for score_tuple in scores:
            score = score_tuple[0]
            if score >= 90: counts[0] += 1
            elif score >= 80: counts[1] += 1
            elif score >= 70: counts[2] += 1
            elif score >= 60: counts[3] += 1
            elif score >= 50: counts[4] += 1
            else: counts[5] += 1
            
    return {"labels": ranges, "data": counts}


@router.get("/skills-cloud")
async def skills_cloud_data(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_recruiter)
):
    recruiter = crud.get_recruiter_by_user_id(db, current_user.id)
    if not recruiter:
        raise HTTPException(status_code=400, detail="Recruiter not found")
        
    jobs = crud.get_recruiter_jobs(db, recruiter.recruiter_id)
    job_ids = [j.job_id for j in jobs]
    
    skills_map = {}
    
    if job_ids:
        # Fetch candidates who applied to these jobs
        candidates = db.query(models.Candidate.skills).join(models.Application).filter(
            models.Application.job_id.in_(job_ids)
        ).all()
        
        for cand_skills_tuple in candidates:
            skills_str = cand_skills_tuple[0]
            if skills_str:
                for skill in [s.strip().lower() for s in skills_str.split(",") if s.strip()]:
                    # Standardize names
                    if skill in ["js", "javascript"]: skill = "JavaScript"
                    elif skill in ["py", "python"]: skill = "Python"
                    elif skill in ["db", "sql", "mysql"]: skill = "SQL/Database"
                    else: skill = skill.title()
                    
                    skills_map[skill] = skills_map.get(skill, 0) + 1
                    
    # Sort and take top 10
    sorted_skills = sorted(skills_map.items(), key=lambda x: x[1], reverse=True)[:10]
    
    labels = [x[0] for x in sorted_skills]
    data = [x[1] for x in sorted_skills]
    
    return {"labels": labels, "data": data}
