from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str  # 'admin', 'recruiter', 'candidate'

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# --- Recruiter Schemas ---
class RecruiterBase(BaseModel):
    company_name: str
    designation: Optional[str] = None

class RecruiterCreate(RecruiterBase):
    user: UserCreate

class RecruiterResponse(RecruiterBase):
    recruiter_id: int
    user_id: int
    user: UserResponse
    model_config = ConfigDict(from_attributes=True)

# --- Candidate Schemas ---
class CandidateBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    degree: Optional[str] = None
    cgpa: Optional[float] = None
    skills: Optional[str] = None  # Comma-separated
    experience_years: Optional[int] = 0
    certifications: Optional[str] = None  # Comma-separated
    projects: Optional[str] = None
    github_link: Optional[str] = None
    linkedin_link: Optional[str] = None

class CandidateCreate(CandidateBase):
    email: EmailStr
    password: str

class CandidateUpdate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    location: Optional[str] = None
    degree: Optional[str] = None
    cgpa: Optional[float] = None
    skills: Optional[str] = None
    experience_years: Optional[int] = 0
    certifications: Optional[str] = None
    projects: Optional[str] = None
    github_link: Optional[str] = None
    linkedin_link: Optional[str] = None

class CandidateResponse(CandidateBase):
    candidate_id: int
    user_id: int
    email: str
    resume_path: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Job Schemas ---
class JobBase(BaseModel):
    title: str
    department: str
    description: str
    required_skills: Optional[str] = None  # Comma-separated
    min_experience: Optional[int] = 0
    min_education: Optional[str] = None
    preferred_certifications: Optional[str] = None  # Comma-separated
    
    # Weights for ranking (should sum to 1.0, but we can normalize them)
    weight_resume: Optional[float] = 0.1
    weight_skills: Optional[float] = 0.2
    weight_coding: Optional[float] = 0.2
    weight_technical: Optional[float] = 0.2
    weight_hr: Optional[float] = 0.1
    weight_projects: Optional[float] = 0.1
    weight_certifications: Optional[float] = 0.1

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    job_id: int
    recruiter_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# --- Application Schemas ---
class ApplicationCreate(BaseModel):
    job_id: int

class ApplicationResponse(BaseModel):
    application_id: int
    candidate_id: int
    job_id: int
    status: str
    applied_at: datetime
    job: JobResponse
    model_config = ConfigDict(from_attributes=True)

class ApplicationStatusUpdate(BaseModel):
    status: str  # 'Applied', 'Shortlisted', 'Rejected', 'Selected'

# --- Assessment Schemas ---
class AssessmentCreateOrUpdate(BaseModel):
    coding_score: float = Field(..., ge=0.0, le=100.0)
    aptitude_score: float = Field(..., ge=0.0, le=100.0)
    technical_score: float = Field(..., ge=0.0, le=100.0)
    hr_score: float = Field(..., ge=0.0, le=100.0)
    project_score: float = Field(..., ge=0.0, le=100.0)

class AssessmentResponse(BaseModel):
    assessment_id: int
    candidate_id: int
    job_id: int
    coding_score: float
    aptitude_score: float
    technical_score: float
    hr_score: float
    project_score: float
    model_config = ConfigDict(from_attributes=True)

# --- AI Score Schemas ---
class AIScoreResponse(BaseModel):
    score_id: int
    candidate_id: int
    job_id: int
    skill_match_score: float
    experience_score: float
    education_score: float
    certification_score: float
    project_score: float
    ml_score: float
    final_score: float
    recommendation: str
    rank_position: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

# --- Recruiter Note Schemas ---
class RecruiterNoteCreate(BaseModel):
    note_text: str

class RecruiterNoteResponse(BaseModel):
    note_id: int
    recruiter_id: int
    candidate_id: int
    job_id: int
    note_text: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
