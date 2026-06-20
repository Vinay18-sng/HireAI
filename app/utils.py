import re
from typing import List, Dict, Any
from app import models

# Education levels hierarchy for matching
EDUCATION_LEVELS = {
    "none": 0,
    "high school": 1,
    "diploma": 2,
    "bachelor": 3,
    "b.tech": 3,
    "b.e.": 3,
    "bs": 3,
    "b.sc": 3,
    "master": 4,
    "m.tech": 4,
    "ms": 4,
    "m.sc": 4,
    "mba": 4,
    "phd": 5,
    "doctorate": 5
}

def parse_list(text: str) -> List[str]:
    """Helper to parse comma-separated or newline-separated strings into a clean lowercase list of items."""
    if not text:
        return []
    # Split by comma or semicolon or newline
    items = re.split(r'[,;\n]', text)
    return [item.strip().lower() for item in items if item.strip()]

def calculate_skill_match(candidate_skills_str: str, job_skills_str: str) -> float:
    """Calculates the percentage of required job skills possessed by the candidate."""
    cand_skills = parse_list(candidate_skills_str)
    job_skills = parse_list(job_skills_str)
    
    if not job_skills:
        return 100.0  # No required skills means perfect fit by default
        
    matched = 0
    for js in job_skills:
        # Check for substring match, e.g. "python" matches in "python development" or vice versa
        if any(js in cs or cs in js for cs in cand_skills):
            matched += 1
            
    return round((matched / len(job_skills)) * 100.0, 2)

def get_education_rank(education_str: str) -> int:
    if not education_str:
        return 0
    edu_lower = education_str.lower()
    for key, val in EDUCATION_LEVELS.items():
        if key in edu_lower:
            return val
    return 2  # Default to Bachelor level if unknown but present

def calculate_education_match(candidate_edu: str, job_min_edu: str) -> float:
    """Calculates education match. 100% if candidate education rank >= job required rank."""
    if not job_min_edu:
        return 100.0
    
    cand_rank = get_education_rank(candidate_edu)
    job_rank = get_education_rank(job_min_edu)
    
    if cand_rank >= job_rank:
        return 100.0
    elif cand_rank == 0:
        return 0.0
    else:
        # Partial match if candidate has some education but less than required
        return round((cand_rank / job_rank) * 100.0, 2)

def calculate_experience_match(cand_exp: int, job_min_exp: int) -> float:
    """Calculates experience match. 100% if candidate exp >= job min exp."""
    if not job_min_exp or job_min_exp <= 0:
        return 100.0
    if cand_exp >= job_min_exp:
        return 100.0
    return round((cand_exp / job_min_exp) * 100.0, 2)

def calculate_certification_score(cand_certs_str: str, job_certs_str: str) -> float:
    """Calculates score based on presence of preferred certifications."""
    pref_certs = parse_list(job_certs_str)
    if not pref_certs:
        return 100.0  # No preferred certifications required
        
    cand_certs = parse_list(cand_certs_str)
    matched = 0
    for pc in pref_certs:
        if any(pc in cc or cc in pc for cc in cand_certs):
            matched += 1
            
    return round((matched / len(pref_certs)) * 100.0, 2)

def calculate_project_score(projects_str: str) -> float:
    """Calculates a baseline project score from candidate's project text."""
    if not projects_str or len(projects_str.strip()) < 5:
        return 0.0
    # Simple heuristic: number of words or bullet points
    # Let's count characters or sentences
    words = len(projects_str.split())
    if words > 100:
        return 100.0
    elif words > 50:
        return 80.0
    elif words > 20:
        return 50.0
    else:
        return 30.0

def calculate_resume_score(candidate: models.Candidate) -> float:
    """Heuristic resume completeness score."""
    score = 40.0  # Base score for uploading profile
    if candidate.resume_path:
        score += 30.0  # Extra points for uploading a file
    if candidate.github_link:
        score += 15.0
    if candidate.linkedin_link:
        score += 15.0
    return min(score, 100.0)

def calculate_rule_based_score(candidate: models.Candidate, job: models.Job, assessment: models.Assessment) -> Dict[str, float]:
    """
    Computes rule-based candidate fit scores based on weights in jobs table.
    Normalizes weights to sum to 1.0.
    """
    # 1. Compute sub-scores
    skill_score = calculate_skill_match(candidate.skills, job.required_skills)
    experience_score = calculate_experience_match(candidate.experience_years, job.min_experience)
    education_score = calculate_education_match(candidate.degree, job.min_education)
    cert_score = calculate_certification_score(candidate.certifications, job.preferred_certifications)
    proj_score = calculate_project_score(candidate.projects)
    resume_score = calculate_resume_score(candidate)
    
    # Extract assessment scores
    coding = assessment.coding_score if assessment else 0.0
    technical = assessment.technical_score if assessment else 0.0
    hr = assessment.hr_score if assessment else 0.0
    
    # 2. Get recruiter defined weights
    w_resume = job.weight_resume or 0.1
    w_skills = job.weight_skills or 0.2
    w_coding = job.weight_coding or 0.2
    w_technical = job.weight_technical or 0.2
    w_hr = job.weight_hr or 0.1
    w_projects = job.weight_projects or 0.1
    w_certs = job.weight_certifications or 0.1
    
    # Ensure weights are normalized to sum to 1.0
    total_weight = w_resume + w_skills + w_coding + w_technical + w_hr + w_projects + w_certs
    if total_weight > 0:
        w_resume /= total_weight
        w_skills /= total_weight
        w_coding /= total_weight
        w_technical /= total_weight
        w_hr /= total_weight
        w_projects /= total_weight
        w_certs /= total_weight
    else:
        # Default even weights
        w_resume = w_skills = w_coding = w_technical = w_hr = w_projects = w_certs = 1.0 / 7.0
        
    # 3. Calculate weighted sum
    weighted_score = (
        (resume_score * w_resume) +
        (skill_score * w_skills) +
        (coding * w_coding) +
        (technical * w_technical) +
        (hr * w_hr) +
        (proj_score * w_projects) +
        (cert_score * w_certs)
    )
    
    return {
        "skill_match_score": round(skill_score, 2),
        "experience_score": round(experience_score, 2),
        "education_score": round(education_score, 2),
        "certification_score": round(cert_score, 2),
        "project_score": round(proj_score, 2),
        "weighted_score": round(weighted_score, 2)
    }

def get_final_recommendation(final_score: float) -> str:
    """Helper to determine recommendation category based on final AI score."""
    if final_score >= 75:
        return "Recommended"
    elif final_score >= 50:
        return "Consider"
    else:
        return "Not Recommended"
