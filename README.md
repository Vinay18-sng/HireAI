# HireAI – AI-Powered Multi-Model Recruitment Platform

HireAI is a premium, full-stack HR-tech web application that automates candidate matching, interview assessments, and application tracking. It utilizes a hybrid AI scoring engine combining a rule-based weighted match (60%) with a trained Random Forest machine learning classifier (40%) to predict candidate suitability and rank them dynamically.

---

## Key Features

* **Multi-Model AI Scoring Engine:** Evaluates applicants based on skill alignment, experience years, education rankings, and assessment test scores.
* **Random Forest ML Classification:** Trained on-the-fly using a realistic candidate dataset of 400 records to calculate suitability probability scores.
* **Dynamic Recruiter Dashboard:** Displays total jobs, applicants, shortlisted statistics, average AI scores, and interactive Chart.js visualizations (applicants per job, funnel breakdown, score distributions).
* **Ranked Applicant Pool & Side-by-Side Comparison:** Instantly ranks candidates for each job. Recruiters can select multiple candidates to compare them side-by-side.
* **Resume Document Uploads:** Candidates can upload PDF/Word resumes which are securely stored on the server and accessible to recruiters.
* **Assessment Scoring Panel:** Recruiters can input and update scores for coding, aptitude, technical interview, HR interview, and projects, triggering instant AI score recalculations.
* **Recruiter Notes & Printable Reports:** Evaluators can log notes for candidates and download print-friendly HTML candidate summaries.
* **Cookie-Based Session Auth & Role-Based Access Control:** Secure JWT authentication stored in HTTP-Only cookies. Automatic dashboards routing based on role (Admin, Recruiter, Candidate).

---

## Tech Stack

* **Frontend:** Semantic HTML5, Custom Styled Premium White/Slate/Blue Light Theme SaaS CSS, Vanilla JavaScript
* **Backend:** Python + FastAPI
* **Database:** MySQL (Primary) with SQLAlchemy ORM
* **Automatic Fallback:** Local SQLite (`sqlite:///./hireai.db`) for immediate zero-config runnability if MySQL is not running or credentials are not configured.
* **Validation:** Pydantic v2
* **Templating:** Jinja2
* **Machine Learning:** Scikit-Learn, Pandas, NumPy

---

##  Project Structure

```bash
HireAI/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI initialization & global handlers
│   ├── database.py          # SQLAlchemy connection with SQLite fallback
│   ├── models.py            # SQLAlchemy database tables
│   ├── schemas.py           # Pydantic v2 request/response validation
│   ├── crud.py              # DB queries, updates & AI scoring pipeline
│   ├── auth.py              # direct bcrypt hashing & JWT token validation
│   ├── utils.py             # Rule-based fit scores & education ranking maps
│   ├── ml_model.py          # Random Forest Classifier training & prediction
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth_routes.py   # Login, registration, and logout routes
│   │   ├── admin.py         # Admin console metrics & list directories
│   │   ├── recruiter.py     # Job posting, applicant lists, scores & comparison
│   │   ├── candidate.py     # Profile editing, dashboard & resume downloads
│   │   ├── jobs.py          # Candidate job search & application submission
│   │   └── analytics.py     # JSON data endpoints for Chart.js
│   │
│   ├── templates/
│   │   ├── base.html        # Main responsive layout grid & navbar/sidebar
│   │   ├── home.html        # Landing page
│   │   ├── login.html       # Login portal with quick-login autofills
│   │   ├── register.html    # Signup with recruiter dynamic inputs toggle
│   │   ├── admin/           # Skeletons for admin directories
│   │   ├── recruiter/       # Dashboards, job forms, rankings, and compare
│   │   ├── candidate/       # Dashboards and profile editing
│   │   └── jobs/            # Job browsing and detail specifications
│   │
│   ├── static/
│   │   └── css/
│   │       └── styles.css   # Premium White/Slate/Blue light SaaS theme
│   │
│   └── uploads/             # Secure folder holding candidate resumes
│
├── dataset/
│   ├── generate_dataset.py  # Self-contained CSV generator
│   └── candidates_sample.csv# 400 candidate dataset rows for ML training
│
├── requirements.txt         # Required Python packages
├── seed.py                  # Full database seeding & ML pre-training script
├── .env                     # Local configuration parameters
└── .env.example             # Configuration templates
```

---

##  Demo Access Credentials

The database comes pre-seeded with these credentials. Click the autofill buttons on the login page to sign in instantly:

* **Administrator Console:**
  * **Email:** `admin@hireai.com`
  * **Password:** `admin123`
* **Recruiter Portal (Google):**
  * **Email:** `recruiter@hireai.com`
  * **Password:** `recruiter123`
* **Candidate Portal (John Doe):**
  * **Email:** `candidate@hireai.com`
  * **Password:** `candidate123`

---

## ⚙️ Installation & Running Guide

### 1. Prerequisite Checks
Ensure you have Python 3.10+ installed.

### 2. Configure Environment (`.env`)
By default, the `.env` file is pre-configured to use **SQLite** so the application runs immediately without database configuration:
```env
DATABASE_URL=sqlite:///./hireai.db
SECRET_KEY=supersecretjwtkeyforhireaiplatformdevelopment123!
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

To switch to a **MySQL** backend, uncomment and edit the line:
```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/hireai
```
*(Make sure to create the database `hireai` in MySQL first, e.g., `CREATE DATABASE hireai;`)*

### 3. Setup Virtual Environment & Install Packages
```bash
# Create venv
python -m venv venv

# Activate venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 4. Seed Database & Train ML Model
Run the seed script to initialize tables, create accounts, generate the candidate dataset, and train the Random Forest Classifier:
```bash
python seed.py
```

### 5. Launch the Application Server
Run the FastAPI development server:
```bash
uvicorn app.main:app --reload
```

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

##  How the AI Score Works

Each time a candidate applies or their assessment scores are updated, a composite score (0-100) is calculated:

$$\text{Final Fit Score} = (0.60 \times \text{Rule-Based Score}) + (0.40 \times \text{ML Suitability Score})$$

1. **Rule-Based Score (60%):** Sums candidate attributes using recruiter-configured job weights:
   * **Skill Match:** Percentage of job's required skills found in candidate profile.
   * **Experience Match:** Degree of alignment with required minimum years.
   * **Education Match:** Rank index check (PhD > Master > Bachelor > Diploma).
   * **Certifications:** Match against preferred certifications.
   * **Assessments:** Weighted scores from Coding, Technical, Aptitude, HR, and Project tests.
2. **ML Suitability Score (40%):** The Random Forest model processes candidate traits and returns the class probability (0% to 100%) of the candidate being "Selected" based on historical data patterns.
3. **Recommendation Categories:**
   * **Recommended:** Score $\ge 75\%$
   * **Consider:** Score $50\% - 74\%$
   * **Not Recommended:** Score $< 50\%$
