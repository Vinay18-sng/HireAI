from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)  # 'admin', 'recruiter', 'candidate'
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    # One-to-One / One-to-Many relationships
    recruiter = relationship("Recruiter", back_populates="user", uselist=False, cascade="all, delete-orphan")
    candidate = relationship("Candidate", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Recruiter(Base):
    __tablename__ = "recruiters"

    recruiter_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_name = Column(String(255), nullable=False)
    designation = Column(String(255))

    # Relationships
    user = relationship("User", back_populates="recruiter")
    jobs = relationship("Job", back_populates="recruiter", cascade="all, delete-orphan")
    notes = relationship("RecruiterNote", back_populates="recruiter", cascade="all, delete-orphan")


class Candidate(Base):
    __tablename__ = "candidates"

    candidate_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50))
    location = Column(String(255))
    degree = Column(String(255))
    cgpa = Column(Float)
    skills = Column(Text)  # Comma-separated or clean list
    experience_years = Column(Integer, default=0)
    certifications = Column(Text)  # Comma-separated or clean list
    projects = Column(Text)  # Text summary or descriptions
    resume_path = Column(String(500))
    github_link = Column(String(255))
    linkedin_link = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="candidate")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="candidate", cascade="all, delete-orphan")
    ai_scores = relationship("AIScore", back_populates="candidate", cascade="all, delete-orphan")
    notes = relationship("RecruiterNote", back_populates="candidate", cascade="all, delete-orphan")


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("recruiters.recruiter_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    department = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text)  # Comma-separated
    min_experience = Column(Integer, default=0)
    min_education = Column(String(255))
    preferred_certifications = Column(Text)  # Comma-separated
    
    # Matching weights (sum up to 1.0)
    weight_resume = Column(Float, default=0.1)
    weight_skills = Column(Float, default=0.2)
    weight_coding = Column(Float, default=0.2)
    weight_technical = Column(Float, default=0.2)
    weight_hr = Column(Float, default=0.1)
    weight_projects = Column(Float, default=0.1)
    weight_certifications = Column(Float, default=0.1)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    # Relationships
    recruiter = relationship("Recruiter", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="job", cascade="all, delete-orphan")
    ai_scores = relationship("AIScore", back_populates="job", cascade="all, delete-orphan")
    notes = relationship("RecruiterNote", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False)
    status = Column(String(100), default="Applied")  # 'Applied', 'Shortlisted', 'Rejected', 'Selected'
    applied_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    # Relationships
    candidate = relationship("Candidate", back_populates="applications")
    job = relationship("Job", back_populates="applications")


class Assessment(Base):
    __tablename__ = "assessments"

    assessment_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False)
    coding_score = Column(Float, default=0.0)
    aptitude_score = Column(Float, default=0.0)
    technical_score = Column(Float, default=0.0)
    hr_score = Column(Float, default=0.0)
    project_score = Column(Float, default=0.0)

    # Relationships
    candidate = relationship("Candidate", back_populates="assessments")
    job = relationship("Job", back_populates="assessments")


class AIScore(Base):
    __tablename__ = "ai_scores"

    score_id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False)
    skill_match_score = Column(Float, default=0.0)
    experience_score = Column(Float, default=0.0)
    education_score = Column(Float, default=0.0)
    certification_score = Column(Float, default=0.0)
    project_score = Column(Float, default=0.0)
    ml_score = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    recommendation = Column(String(100))  # 'Recommended', 'Consider', 'Not Recommended'
    rank_position = Column(Integer)

    # Relationships
    candidate = relationship("Candidate", back_populates="ai_scores")
    job = relationship("Job", back_populates="ai_scores")


class RecruiterNote(Base):
    __tablename__ = "recruiter_notes"

    note_id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("recruiters.recruiter_id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.job_id", ondelete="CASCADE"), nullable=False)
    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, server_default=func.now())

    # Relationships
    recruiter = relationship("Recruiter", back_populates="notes")
    candidate = relationship("Candidate", back_populates="notes")
    job = relationship("Job", back_populates="notes")
