# HireAI – AI-Powered Multi-Model Recruitment Platform

## Overview

HireAI is a full-stack AI-powered recruitment platform designed to streamline the hiring process for recruiters, candidates, and administrators.

The platform combines traditional recruitment workflows with a Hybrid AI Fit Engine that evaluates candidates using both rule-based matching and machine learning predictions.

---

## Problem Statement

Recruiters often spend significant time reviewing resumes, comparing candidate profiles, conducting assessments, and shortlisting applicants.

Manual hiring processes can lead to:

* Delayed recruitment decisions
* Inconsistent candidate evaluation
* Difficulty comparing multiple applicants
* Increased recruiter workload

HireAI addresses these challenges by providing AI-assisted candidate ranking, evaluation, and comparison tools.

---

## Key Features

### Candidate Portal

* Candidate registration and login
* Profile management
* Resume upload
* Job browsing
* Job applications
* Application status tracking

### Recruiter Portal

* Job posting management
* Candidate evaluation panel
* Assessment score entry
* Candidate ranking
* Side-by-side candidate comparison
* Recruiter notes
* Printable evaluation reports
* Dashboard analytics

### Admin Portal

* Platform overview dashboard
* Candidate directory
* Recruiter directory
* Job directory
* Application monitoring

---

## Hybrid AI Fit Engine

The platform uses a hybrid scoring model:

Final AI Fit Score = (0.60 × Rule-Based Score) + (0.40 × Machine Learning Prediction)

### Rule-Based Scoring

Evaluates:

* Skill matching
* Education matching
* Experience matching
* Assessment performance
* Certifications
* Projects

### Machine Learning Prediction

Uses a Random Forest Classifier trained on candidate recruitment data.

### Recommendation Categories

* Recommended → Score ≥ 75
* Consider → Score 50–74
* Not Recommended → Score < 50

---

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

### Backend

* Python
* FastAPI

### Database

* SQLite (default)
* MySQL (optional)

### ORM

* SQLAlchemy

### Machine Learning

* Scikit-Learn
* Pandas
* NumPy
* Random Forest Classifier

### Visualization

* Chart.js

### Authentication & Security

* JWT
* bcrypt

---

## Project Structure

```text
HireAI/
│
├── app/
│   ├── routers/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── auth.py
│   ├── database.py
│   └── main.py
│
├── dataset/
├── sql/
├── requirements.txt
├── seed.py
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Vinay18-sng/HireAI.git
cd HireAI
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## Demo Workflow

### Candidate

1. Register/Login
2. Complete profile
3. Upload resume
4. Browse jobs
5. Apply for jobs

### Recruiter

1. Login
2. Create job
3. Review applicants
4. Enter assessment scores
5. View AI ranking
6. Compare candidates
7. Generate reports

### Administrator

1. Login
2. Monitor platform activity
3. View recruiters
4. View candidates
5. Manage job listings

---

## Future Enhancements

* NLP-based resume parsing
* Email notifications
* Interview scheduling
* Cloud deployment
* Job recommendation system
* Advanced machine learning models
* Bias detection and fairness analysis

---

## Author

**K Vinay**

AI & Machine Learning Engineering Student

---

## License

This project is developed for educational, internship, and demonstration purposes.
