import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app import models, schemas, auth, utils

logger = logging.getLogger(__name__)

# --- User CRUD ---
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_pwd = auth.get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password_hash=hashed_pwd,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Recruiter CRUD ---
def get_recruiter_by_user_id(db: Session, user_id: int) -> Optional[models.Recruiter]:
    return db.query(models.Recruiter).filter(models.Recruiter.user_id == user_id).first()

def create_recruiter(db: Session, recruiter: schemas.RecruiterCreate, user_id: int) -> models.Recruiter:
    db_recruiter = models.Recruiter(
        user_id=user_id,
        company_name=recruiter.company_name,
        designation=recruiter.designation
    )
    db.add(db_recruiter)
    db.commit()
    db.refresh(db_recruiter)
    return db_recruiter

# --- Candidate CRUD ---
def get_candidate(db: Session, candidate_id: int) -> Optional[models.Candidate]:
    return db.query(models.Candidate).filter(models.Candidate.candidate_id == candidate_id).first()

def get_candidate_by_user_id(db: Session, user_id: int) -> Optional[models.Candidate]:
    return db.query(models.Candidate).filter(models.Candidate.user_id == user_id).first()

def create_candidate_profile(db: Session, user_id: int, name: str, email: str) -> models.Candidate:
    """Helper to initialize candidate profile on user signup."""
    db_cand = models.Candidate(
        user_id=user_id,
        full_name=name,
        email=email,
        experience_years=0,
        cgpa=0.0
    )
    db.add(db_cand)
    db.commit()
    db.refresh(db_cand)
    return db_cand

def update_candidate(db: Session, db_candidate: models.Candidate, profile_update: schemas.CandidateUpdate) -> models.Candidate:
    for var, val in profile_update.model_dump(exclude_unset=True).items():
        setattr(db_candidate, var, val)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

# --- Job CRUD ---
def get_job(db: Session, job_id: int) -> Optional[models.Job]:
    return db.query(models.Job).filter(models.Job.job_id == job_id).first()

def get_all_jobs(db: Session) -> List[models.Job]:
    return db.query(models.Job).order_by(desc(models.Job.created_at)).all()

def get_recruiter_jobs(db: Session, recruiter_id: int) -> List[models.Job]:
    return db.query(models.Job).filter(models.Job.recruiter_id == recruiter_id).order_by(desc(models.Job.created_at)).all()

def create_job(db: Session, job: schemas.JobCreate, recruiter_id: int) -> models.Job:
    db_job = models.Job(
        recruiter_id=recruiter_id,
        **job.model_dump()
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def update_job(db: Session, db_job: models.Job, job_update: schemas.JobCreate) -> models.Job:
    for var, val in job_update.model_dump().items():
        setattr(db_job, var, val)
    db.commit()
    db.refresh(db_job)
    return db_job

def delete_job(db: Session, db_job: models.Job) -> None:
    db.delete(db_job)
    db.commit()

# --- Application CRUD ---
def get_application(db: Session, app_id: int) -> Optional[models.Application]:
    return db.query(models.Application).filter(models.Application.application_id == app_id).first()

def get_applications_for_job(db: Session, job_id: int) -> List[models.Application]:
    return db.query(models.Application).filter(models.Application.job_id == job_id).all()

def get_candidate_applications(db: Session, candidate_id: int) -> List[models.Application]:
    return db.query(models.Application).filter(models.Application.candidate_id == candidate_id).all()

def check_already_applied(db: Session, candidate_id: int, job_id: int) -> bool:
    res = db.query(models.Application).filter(
        models.Application.candidate_id == candidate_id,
        models.Application.job_id == job_id
    ).first()
    return res is not None

def create_application(db: Session, candidate_id: int, job_id: int) -> models.Application:
    db_app = models.Application(
        candidate_id=candidate_id,
        job_id=job_id,
        status="Applied"
    )
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def update_application_status(db: Session, db_app: models.Application, status: str) -> models.Application:
    db_app.status = status
    db.commit()
    db.refresh(db_app)
    return db_app

# --- Assessment CRUD ---
def get_assessment(db: Session, candidate_id: int, job_id: int) -> Optional[models.Assessment]:
    return db.query(models.Assessment).filter(
        models.Assessment.candidate_id == candidate_id,
        models.Assessment.job_id == job_id
    ).first()

def get_or_create_assessment(db: Session, candidate_id: int, job_id: int) -> models.Assessment:
    db_ass = get_assessment(db, candidate_id, job_id)
    if not db_ass:
        db_ass = models.Assessment(
            candidate_id=candidate_id,
            job_id=job_id,
            coding_score=0.0,
            aptitude_score=0.0,
            technical_score=0.0,
            hr_score=0.0,
            project_score=0.0
        )
        db.add(db_ass)
        db.commit()
        db.refresh(db_ass)
    return db_ass

def update_assessment(db: Session, db_ass: models.Assessment, scores: schemas.AssessmentCreateOrUpdate) -> models.Assessment:
    for var, val in scores.model_dump().items():
        setattr(db_ass, var, val)
    db.commit()
    db.refresh(db_ass)
    return db_ass

# --- Recruiter Notes CRUD ---
def get_notes_for_candidate_job(db: Session, candidate_id: int, job_id: int) -> List[models.RecruiterNote]:
    return db.query(models.RecruiterNote).filter(
        models.RecruiterNote.candidate_id == candidate_id,
        models.RecruiterNote.job_id == job_id
    ).order_by(desc(models.RecruiterNote.created_at)).all()

def create_note(db: Session, recruiter_id: int, candidate_id: int, job_id: int, note_text: str) -> models.RecruiterNote:
    db_note = models.RecruiterNote(
        recruiter_id=recruiter_id,
        candidate_id=candidate_id,
        job_id=job_id,
        note_text=note_text
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

# --- AI Scoring and Recalculation ---
def get_ai_score(db: Session, candidate_id: int, job_id: int) -> Optional[models.AIScore]:
    return db.query(models.AIScore).filter(
        models.AIScore.candidate_id == candidate_id,
        models.AIScore.job_id == job_id
    ).first()

def recalculate_job_rankings(db: Session, job_id: int) -> None:
    """Updates rank_position for all candidates applying to a job based on final_score."""
    scores = db.query(models.AIScore).filter(models.AIScore.job_id == job_id).order_by(desc(models.AIScore.final_score)).all()
    for idx, s in enumerate(scores):
        s.rank_position = idx + 1
    db.commit()

def calculate_and_save_ai_score(db: Session, candidate_id: int, job_id: int) -> models.AIScore:
    """Combines Rule-Based (60%) and ML (40%) scores, saves the result, and updates job rankings."""
    candidate = get_candidate(db, candidate_id)
    job = get_job(db, job_id)
    assessment = get_or_create_assessment(db, candidate_id, job_id)
    
    if not candidate or not job:
        raise ValueError("Candidate or Job not found.")
        
    # 1. Rule-based scores
    rule_results = utils.calculate_rule_based_score(candidate, job, assessment)
    rule_score = rule_results["weighted_score"]
    
    # 2. ML suitability score
    # Count certifications
    certs = utils.parse_list(candidate.certifications)
    cert_count = len(certs)
    
    # Pre-calculated project score
    proj_score = rule_results["project_score"]
    
    # Import locally to avoid potential early import issues
    from app.ml_model import predict_suitability
    
    ml_score = predict_suitability(
        role_applied=job.title,
        degree=candidate.degree or "Bachelor",
        cgpa=candidate.cgpa or 7.0,
        skill_match_percent=rule_results["skill_match_score"],
        experience_years=candidate.experience_years or 0,
        coding_score=assessment.coding_score,
        aptitude_score=assessment.aptitude_score,
        technical_score=assessment.technical_score,
        hr_score=assessment.hr_score,
        certification_count=cert_count,
        project_score=proj_score
    )
    
    # 3. Blend: 60% rule-based + 40% ML
    final_score = round((rule_score * 0.60) + (ml_score * 0.40), 2)
    rec = utils.get_final_recommendation(final_score)
    
    # 4. Save to DB
    ai_score = get_ai_score(db, candidate_id, job_id)
    if not ai_score:
        ai_score = models.AIScore(
            candidate_id=candidate_id,
            job_id=job_id
        )
        db.add(ai_score)
        
    ai_score.skill_match_score = rule_results["skill_match_score"]
    ai_score.experience_score = rule_results["experience_score"]
    ai_score.education_score = rule_results["education_score"]
    ai_score.certification_score = rule_results["certification_score"]
    ai_score.project_score = rule_results["project_score"]
    ai_score.ml_score = ml_score
    ai_score.final_score = final_score
    ai_score.recommendation = rec
    
    db.commit()
    db.refresh(ai_score)
    
    # 5. Rerank candidates for this job
    recalculate_job_rankings(db, job_id)
    db.refresh(ai_score)
    
    return ai_score
