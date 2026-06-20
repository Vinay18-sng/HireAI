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

## Render Deployment

Prepare to deploy the HireAI platform onto **Render (free tier)**. The codebase is fully configured for zero-configuration setup using a Render Blueprint or manual settings.

### Option 1: Automated Deploy via Render Blueprint (Recommended)
1. Commit all your changes and push them to your GitHub repository.
2. Log in to your [Render Dashboard](https://dashboard.render.com).
3. Click **New +** and select **Blueprint**.
4. Connect your GitHub repository containing the HireAI codebase.
5. Render will automatically detect the `render.yaml` file, provisioning a free PostgreSQL database and a FastAPI Web Service connected to it.
6. The service will build and boot up, and auto-seeding will populate the database with demo accounts automatically.

### Option 2: Manual Deploy on Render
If you prefer not to use blueprints:
1. Create a new **Web Service** on Render and connect your repository.
2. Select **Python** as the runtime.
3. Configure the following service settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. In the **Environment** tab, add the following environment variables:
   - `SECRET_KEY`: A secure random JWT key (e.g., `your-random-secret-key-123!`).
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `120`
   - `AUTO_SEED`: `true` (enables automatic data seeding on first boot).
   - `DATABASE_URL`: (Optional) Connect your own MySQL/PostgreSQL connection string. If left blank, HireAI will fall back to SQLite automatically.

### Notes on SQLite Fallback and Ephemeral File Systems
* **SQLite Fallback:** If `DATABASE_URL` is omitted, the application uses an SQLite database (`hireai.db`) resolved at the root directory of the application.
* **Limitations on Render Free Tier:** Render free tier container disks are **ephemeral**. Any SQLite database changes or candidate resume uploads will be reset whenever the service restarts, redeploys, or spins down due to inactivity. For persistent storage, use Render PostgreSQL (Option 1) or hook up an external database in the `DATABASE_URL` variable.

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
