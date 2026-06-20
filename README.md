# HireAI – AI-Powered Multi-Model Recruitment Platform

<p align="center">
  <b>AI-assisted recruitment platform for candidate evaluation, ranking, comparison, and hiring workflow management</b>
</p>

---

## Table of Contents

* [Overview](#overview)
* [Problem Statement](#problem-statement)
* [Objectives](#objectives)
* [Key Features](#key-features)
* [System Modules](#system-modules)
* [Hybrid AI Fit Engine](#hybrid-ai-fit-engine)
* [Technology Stack](#technology-stack)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Run the Application](#run-the-application)
* [Render Deployment](#render-deployment)
* [Demo Workflow](#demo-workflow)
* [Application Screenshots](#application-screenshots)
* [Future Enhancements](#future-enhancements)
* [Author](#author)
* [License](#license)

---

# Overview

**HireAI** is a full-stack **AI-powered recruitment platform** designed to simplify and modernize the hiring process for **candidates, recruiters, and administrators**. It combines traditional recruitment workflows with an intelligent **Hybrid AI Fit Engine** that evaluates candidates using both **rule-based heuristics** and **machine learning predictions**.

The platform is built to reduce manual effort in candidate screening, improve evaluation consistency, and support faster, data-driven hiring decisions.

---

# Problem Statement

Recruitment is often a time-consuming process in which recruiters must manually review resumes, compare candidate profiles, track assessment performance, and shortlist applicants. These traditional workflows can create several challenges, including:

* delayed hiring decisions
* inconsistent evaluation of candidates
* difficulty in comparing multiple applicants effectively
* increased recruiter workload
* limited use of candidate performance data during final selection

HireAI addresses these issues by providing a unified recruitment platform that automates candidate evaluation, ranking, comparison, and reporting while still allowing recruiters to apply human judgment where needed.

---

# Objectives

The main objectives of HireAI are:

* to streamline the recruitment lifecycle for candidates, recruiters, and administrators
* to reduce manual effort in resume screening and applicant comparison
* to assist recruiters with AI-based candidate ranking and fit analysis
* to provide structured assessment and reporting workflows
* to improve the consistency and speed of hiring decisions
* to create a practical AI-driven recruitment system suitable for academic, internship, and demo use cases

---

# Key Features

## Candidate Portal

* Candidate registration and login
* Profile management and profile completeness tracking
* Resume upload support
* Job browsing and job application submission
* Application status tracking
* Candidate-side dashboard for monitoring active applications

## Recruiter Portal

* Recruiter login and personalized dashboard
* Job posting and job management
* Candidate evaluation and assessment score entry
* AI-based applicant ranking
* Side-by-side candidate comparison matrix
* Recruiter notes and decision support
* Printable candidate evaluation reports
* Visual dashboard analytics

## Admin Portal

* Platform overview dashboard
* Candidate directory
* Recruiter directory
* Job listing directory
* Application monitoring and administrative visibility

---

# System Modules

## 1. Candidate Module

The candidate module allows applicants to register, log in, maintain their profile, upload resumes, browse available jobs, and apply for suitable openings. It also helps candidates track the status of submitted applications.

## 2. Recruiter Module

The recruiter module provides tools for posting jobs, reviewing applicants, entering assessment scores, viewing AI-generated candidate rankings, comparing shortlisted applicants, and generating evaluation reports.

## 3. Admin Module

The admin module provides a centralized view of the platform, including users, recruiters, candidates, jobs, and applications, enabling better system monitoring and management.

## 4. AI Scoring Module

The AI scoring module combines rule-based matching with machine learning predictions to generate a final candidate fit score for each application.

---

# Hybrid AI Fit Engine

HireAI uses a **hybrid candidate evaluation model** that combines **rule-based scoring** with **machine learning prediction** to generate a final candidate suitability score.

## Final AI Fit Score

```text
Final AI Fit Score = (0.60 × Rule-Based Score) + (0.40 × Machine Learning Prediction)
```

---

## Rule-Based Scoring

The rule-based component evaluates candidates using recruiter-defined job requirements and candidate profile data.

### Factors considered

* skill matching
* education matching
* experience matching
* assessment performance
* certifications
* project work

### Example rule-based evaluation logic

* overlap between candidate skills and required job skills
* verification of minimum education level
* comparison of candidate experience against required experience
* scoring based on coding, aptitude, technical, HR, and project assessments

---

## Machine Learning Prediction

The machine learning component uses a **Random Forest Classifier** trained on recruitment-related candidate data to estimate the likelihood of a candidate being selected.

### Model input examples

* CGPA
* skill match percentage
* years of experience
* coding score
* aptitude score
* technical interview score
* HR interview score
* project score

---

## Recommendation Categories

* **Recommended** → Final score **≥ 75**
* **Consider** → Final score **50–74**
* **Not Recommended** → Final score **< 50**

---

# Technology Stack

## Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

## Backend

* Python
* FastAPI

## Database

* SQLite *(local/demo fallback)*
* PostgreSQL *(supported and recommended for deployment)*
* MySQL *(optional)*

## ORM

* SQLAlchemy

## Machine Learning

* Scikit-Learn
* Pandas
* NumPy
* Random Forest Classifier

## Data Visualization

* Chart.js

## Authentication & Security

* bcrypt
* session/JWT-based authentication

---

# Project Structure

```text
HireAI/
│
├── app/
│   ├── routers/
│   │   ├── admin.py
│   │   ├── analytics.py
│   │   ├── auth_routes.py
│   │   ├── candidate.py
│   │   ├── jobs.py
│   │   └── recruiter.py
│   │
│   ├── static/
│   │   └── css/
│   │
│   ├── templates/
│   │   ├── admin/
│   │   ├── candidate/
│   │   ├── jobs/
│   │   └── recruiter/
│   │
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── ml_model.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
│
├── dataset/
│   ├── candidates_sample.csv
│   └── generate_dataset.py
│
├── screenshots/
│   ├── home-page.png
│   ├── candidate-dashboard.png
│   ├── recruiter-dashboard.png
│   ├── ranked-applicants.png
│   ├── candidate-comparison.png
│   ├── candidate-report.png
│   └── admin-dashboard.png
│
├── sql/
│   └── hireai_schema.sql
│
├── requirements.txt
├── seed.py
├── render.yaml
├── runtime.txt
└── README.md
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Vinay18-sng/HireAI.git
cd HireAI
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

## 3. Activate the Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

## Local Development

```bash
uvicorn app.main:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000
```

---

## Production / Deployment Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

# Render Deployment

HireAI is configured for deployment on **Render** and supports both **Blueprint deployment** and **manual Web Service deployment**.

## Option 1: Deploy with Render Blueprint (Recommended)

1. Push the latest HireAI code to GitHub.
2. Sign in to the Render dashboard.
3. Click **New +** → **Blueprint**.
4. Select the GitHub repository containing HireAI.
5. Render will automatically detect the `render.yaml` file and create the required services.
6. Review the generated service settings and deploy.

This is the recommended deployment method because the repository already includes deployment-ready configuration.

---

## Option 2: Manual Render Deployment

If you want to configure the service manually:

### Create a Web Service

* **Environment:** Python

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## Required Environment Variables

Set the following environment variables in Render:

```env
APP_ENV=production
AUTO_SEED=true
SECRET_KEY=your_long_random_secret_key
```

### Optional Environment Variables

* `DATABASE_URL` → PostgreSQL or MySQL connection string
* `ALGORITHM`
* `ACCESS_TOKEN_EXPIRE_MINUTES`

---

## Database Behavior

HireAI supports:

* **PostgreSQL**
* **MySQL**
* **SQLite fallback**

If `DATABASE_URL` is not provided, the application falls back to a local SQLite database for demo and development use.

---

## Auto-Seeding

If `AUTO_SEED=true`, HireAI automatically inserts demo data on first startup **only when the database is empty**.

This makes the platform easier to test in:

* internship demonstrations
* project showcases
* local development environments

---

## Important Note About SQLite on Render Free Tier

If the application is deployed using SQLite fallback on Render free tier:

* the database is stored on an **ephemeral filesystem**
* uploaded resumes and SQLite data may be lost when the service restarts, redeploys, or sleeps

For a more stable hosted deployment, **PostgreSQL** is recommended.

---

## Recommended Render Setup

* **Service Name:** `hireai-web`
* **Build Command:** `pip install -r requirements.txt`
* **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

# Demo Workflow

## Candidate Workflow

1. Register or log in
2. Complete profile information
3. Upload resume
4. Browse available jobs
5. Apply for jobs
6. Track application status

## Recruiter Workflow

1. Log in
2. Create and manage jobs
3. Review applicants
4. Enter assessment scores
5. View AI-based candidate ranking
6. Compare candidates side by side
7. Generate candidate evaluation reports

## Administrator Workflow

1. Log in
2. Monitor platform activity
3. View recruiter directory
4. View candidate directory
5. Manage jobs and applications

---

# Application Screenshots

## Home Page

Landing page of HireAI showing the platform overview, authentication entry points, and feature highlights.

![Home Page](screenshots/home-page.png)

## Candidate Dashboard

Displays candidate profile status, application tracking, and job-related activities.

![Candidate Dashboard](screenshots/candidate-dashboard.png)

## Recruiter Dashboard

Provides recruiter analytics, job management, and applicant overview.

![Recruiter Dashboard](screenshots/recruiter-dashboard.png)

## Ranked Applicants Page

Shows AI-based candidate ranking for a selected job using the hybrid scoring engine.

![Ranked Applicants](screenshots/ranked-applicants.png)

## Candidate Comparison Matrix

Allows recruiters to compare multiple candidates side by side across skills, experience, and assessment scores.

![Candidate Comparison Matrix](screenshots/candidate-comparison.png)

## Candidate Report Page

Displays a print-friendly candidate evaluation report with AI fit score, assessment breakdown, and recruiter notes.

![Candidate Report](screenshots/candidate-report.png)

## Admin Dashboard

Provides system-wide visibility into recruiters, candidates, jobs, and applications.

![Admin Dashboard](screenshots/admin-dashboard.png)

---

# Future Enhancements

* NLP-based resume parsing
* Email notifications
* Interview scheduling
* Job recommendation system
* advanced resume-job matching
* improved machine learning pipeline
* bias detection and fairness analysis
* resume semantic matching using embeddings
* cloud object storage for resume uploads

---

# Author

**K Vinay**
AI & Machine Learning Engineering Student

---

# License

This project is developed for **educational, internship, and demonstration purposes**.
