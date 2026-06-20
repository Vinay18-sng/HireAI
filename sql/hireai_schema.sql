-- HireAI MySQL Schema Definitions

CREATE DATABASE IF NOT EXISTS hireai;
USE hireai;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'admin', 'recruiter', 'candidate'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Recruiters Table
CREATE TABLE IF NOT EXISTS recruiters (
    recruiter_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    designation VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Candidates Table
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    location VARCHAR(255),
    degree VARCHAR(255),
    cgpa FLOAT,
    skills TEXT,
    experience_years INT DEFAULT 0,
    certifications TEXT,
    projects TEXT,
    resume_path VARCHAR(500),
    github_link VARCHAR(255),
    linkedin_link VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    recruiter_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    department VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    required_skills TEXT,
    min_experience INT DEFAULT 0,
    min_education VARCHAR(255),
    preferred_certifications TEXT,
    weight_resume FLOAT DEFAULT 0.1,
    weight_skills FLOAT DEFAULT 0.2,
    weight_coding FLOAT DEFAULT 0.2,
    weight_technical FLOAT DEFAULT 0.2,
    weight_hr FLOAT DEFAULT 0.1,
    weight_projects FLOAT DEFAULT 0.1,
    weight_certifications FLOAT DEFAULT 0.1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recruiter_id) REFERENCES recruiters(recruiter_id) ON DELETE CASCADE
);

-- 5. Applications Table
CREATE TABLE IF NOT EXISTS applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    status VARCHAR(100) DEFAULT 'Applied', -- 'Applied', 'Shortlisted', 'Rejected', 'Selected'
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

-- 6. Assessments Table
CREATE TABLE IF NOT EXISTS assessments (
    assessment_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    coding_score FLOAT DEFAULT 0.0,
    aptitude_score FLOAT DEFAULT 0.0,
    technical_score FLOAT DEFAULT 0.0,
    hr_score FLOAT DEFAULT 0.0,
    project_score FLOAT DEFAULT 0.0,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

-- 7. AI Scores Table
CREATE TABLE IF NOT EXISTS ai_scores (
    score_id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    skill_match_score FLOAT DEFAULT 0.0,
    experience_score FLOAT DEFAULT 0.0,
    education_score FLOAT DEFAULT 0.0,
    certification_score FLOAT DEFAULT 0.0,
    project_score FLOAT DEFAULT 0.0,
    ml_score FLOAT DEFAULT 0.0,
    final_score FLOAT DEFAULT 0.0,
    recommendation VARCHAR(100), -- 'Recommended', 'Consider', 'Not Recommended'
    rank_position INT,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

-- 8. Recruiter Notes Table
CREATE TABLE IF NOT EXISTS recruiter_notes (
    note_id INT AUTO_INCREMENT PRIMARY KEY,
    recruiter_id INT NOT NULL,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    note_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recruiter_id) REFERENCES recruiters(recruiter_id) ON DELETE CASCADE,
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);
