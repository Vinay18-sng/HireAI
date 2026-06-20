import os
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from app import models, crud, auth

def seed_db():
    print("Initializing database tables...")
    # Drop and recreate tables to start fresh
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        print("Creating demo accounts...")
        
        # 1. Create Admin
        admin_user = models.User(
            name="Platform Admin",
            email="admin@hireai.com",
            password_hash=auth.get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin_user)
        
        # 2. Create Recruiters
        rec1_user = models.User(
            name="Sarah Jenkins",
            email="recruiter@hireai.com",
            password_hash=auth.get_password_hash("recruiter123"),
            role="recruiter"
        )
        rec2_user = models.User(
            name="Marcus Vance",
            email="recruiter2@hireai.com",
            password_hash=auth.get_password_hash("recruiter123"),
            role="recruiter"
        )
        db.add_all([rec1_user, rec2_user])
        db.commit()
        
        rec1_profile = models.Recruiter(
            user_id=rec1_user.id,
            company_name="Google",
            designation="Principal Tech Recruiter"
        )
        rec2_profile = models.Recruiter(
            user_id=rec2_user.id,
            company_name="Meta",
            designation="Lead Talent Architect"
        )
        db.add_all([rec1_profile, rec2_profile])
        
        # 3. Create Candidates (12 total for realistic distribution)
        candidates_data = [
            ("John Doe", "candidate@hireai.com", "candidate123", "+1-555-1001", "San Francisco, USA", "B.Tech in Computer Science", 8.8, "Python, SQL, FastAPI, Docker, Git", 3, "AWS Certified Developer", "Developed web APIs with FastAPI; configured CI/CD pipelines."),
            ("Jane Smith", "candidate2@hireai.com", "candidate123", "+1-555-1002", "New York, USA", "M.S. in Software Engineering", 9.1, "JavaScript, React, Node, CSS, HTML5, TypeScript", 4, "Certified React Developer", "Built single page apps using React/Redux and Node.js backend REST interfaces."),
            ("Alice Johnson", "candidate3@hireai.com", "candidate123", "+1-555-1003", "Boston, USA", "PhD in Data Science", 9.7, "Python, Machine Learning, PyTorch, Pandas, Scikit-Learn, SQL", 6, "Google Professional Data Engineer", "Published NLP research papers. Built and deployed deep learning text classifiers in production."),
            ("Bob Brown", "candidate4@hireai.com", "candidate123", "+1-555-1004", "Seattle, USA", "B.Tech in Information Technology", 7.2, "AWS, Docker, Kubernetes, Linux, Bash, Git, Python", 2, "AWS Solutions Architect Associate", "Maintained cloud infrastructure, built terraform configurations, and handled deployments."),
            ("Charlie Green", "candidate5@hireai.com", "candidate123", "+1-555-1005", "Austin, USA", "MBA in Tech Management", 8.2, "Agile, Scrum, Jira, Product Management, Analytics", 5, "Certified Scrum Master (CSM)", "Led cross-functional product sprints, defined roadmap scopes, and analyzed user retention."),
            ("Diana Prince", "candidate6@hireai.com", "candidate123", "+1-555-1006", "Chicago, USA", "Bachelor of Science", 8.5, "Python, Django, PostgreSQL, HTML, CSS", 1, "None", "Designed ecommerce platforms with Django; integrated Stripe payments."),
            ("Evan Wright", "candidate7@hireai.com", "candidate123", "+1-555-1007", "Denver, USA", "M.S. in Computer Science", 9.4, "Python, C++, SQL, Algorithms, Multithreading", 5, "None", "Optimized database index query execution times; built low-latency simulation engines."),
            ("Fiona Gallagher", "candidate8@hireai.com", "candidate123", "+1-555-1008", "Los Angeles, USA", "Diploma", 6.8, "JavaScript, HTML, CSS, jQuery, Bootstrap", 2, "None", "Created responsive web layouts for digital agency marketing campaigns."),
            ("George Costanza", "candidate9@hireai.com", "candidate123", "+1-555-1009", "New York, USA", "Bachelor of Arts", 7.0, "Product Management, Excel, Communication", 3, "None", "Managed stakeholder client relations and drafted feature specification proposals."),
            ("Helen Keller", "candidate10@hireai.com", "candidate123", "+1-555-1010", "Miami, USA", "Master of IT", 8.9, "SQL, Python, Tableau, Excel, BI Analytics", 4, "Tableau Desktop Specialist", "Created analytics business intelligence executive reporting dashboards."),
            ("Ian Malcolm", "candidate11@hireai.com", "candidate123", "+1-555-1011", "Dallas, USA", "PhD in Mathematics", 9.9, "Python, R, NumPy, Statistics, ML, MATLAB", 8, "None", "Modeled biological population algorithms and chaos theory structures."),
            ("Julia Roberts", "candidate12@hireai.com", "candidate123", "+1-555-1012", "Atlanta, USA", "B.Tech in CS", 8.6, "Java, Spring Boot, MySQL, Git", 3, "Oracle Certified Java Professional", "Maintained enterprise Java microservices and transactional relational APIs.")
        ]
        
        candidates = []
        for name, email, pwd, phone, loc, deg, cgpa, skills, exp, certs, proj in candidates_data:
            c_user = models.User(
                name=name,
                email=email,
                password_hash=auth.get_password_hash(pwd),
                role="candidate"
            )
            db.add(c_user)
            db.commit()
            
            c_profile = models.Candidate(
                user_id=c_user.id,
                full_name=name,
                email=email,
                phone=phone,
                location=loc,
                degree=deg,
                cgpa=cgpa,
                skills=skills,
                experience_years=exp,
                certifications=certs,
                projects=proj
            )
            db.add(c_profile)
            db.commit()
            candidates.append(c_profile)
            
        print(f"Created {len(candidates)} candidates.")
        
        # 4. Create Jobs
        print("Creating job openings...")
        jobs_data = [
            # Google Jobs (Sarah Jenkins - recruiter_id = 1)
            (1, "Python Backend Developer", "Engineering", "We are looking for a Python Software Engineer to build scalable APIs using FastAPI and SQLAlchemy.", "Python, FastAPI, SQL, Git", 2, "Bachelor", "AWS Certified Developer", 0.1, 0.2, 0.25, 0.20, 0.1, 0.1, 0.05),
            (1, "Machine Learning Engineer", "Engineering", "Build and deploy neural network models. Preprocess data streams and optimize random forest pipelines.", "Python, Machine Learning, Scikit-Learn, PyTorch, Pandas", 4, "Master", "None", 0.05, 0.25, 0.20, 0.25, 0.1, 0.1, 0.05),
            (1, "Frontend Engineer", "Design", "Design modern, responsive user interfaces. Implement interactive client logic.", "JavaScript, React, CSS, HTML5, TypeScript", 2, "Bachelor", "None", 0.1, 0.3, 0.1, 0.2, 0.1, 0.15, 0.05),
            
            # Meta Jobs (Marcus Vance - recruiter_id = 2)
            (2, "Product Manager II", "Product", "Oversee feature lifecycles, run sprint meetings, align tech roadmaps.", "Product Management, Agile, Jira, Analytics", 3, "Bachelor", "Certified Scrum Master", 0.1, 0.2, 0.1, 0.15, 0.2, 0.15, 0.1),
            (2, "DevOps / Infrastructure Engineer", "Operations", "Implement robust CI/CD, terraform scripting, and monitor containerized infrastructure.", "AWS, Docker, Kubernetes, Linux, Git", 3, "Bachelor", "AWS Solutions Architect", 0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.1)
        ]
        
        jobs = []
        for rec_id, title, dept, desc, skills, exp, edu, certs, w_res, w_sk, w_cod, w_tech, w_hr, w_proj, w_cert in jobs_data:
            job = models.Job(
                recruiter_id=rec_id,
                title=title,
                department=dept,
                description=desc,
                required_skills=skills,
                min_experience=exp,
                min_education=edu,
                preferred_certifications=certs,
                weight_resume=w_res,
                weight_skills=w_sk,
                weight_coding=w_cod,
                weight_technical=w_tech,
                weight_hr=w_hr,
                weight_projects=w_proj,
                weight_certifications=w_cert
            )
            db.add(job)
            db.commit()
            jobs.append(job)
            
        print(f"Created {len(jobs)} jobs.")
        
        # 5. Create Applications & Assessment Scores
        print("Submitting candidate applications & adding interview scores...")
        
        # Mapping: candidate index -> list of job indices they apply for
        applications_map = {
            0: [0, 4], # John Doe applies to Python Backend and DevOps
            1: [2],    # Jane Smith applies to Frontend
            2: [0, 1], # Alice Johnson applies to Python Backend and ML Engineer
            3: [4],    # Bob Brown applies to DevOps
            4: [3],    # Charlie Green applies to Product Manager
            5: [0],    # Diana Prince applies to Python Backend
            6: [0, 1], # Evan Wright applies to Python Backend and ML Engineer
            7: [2],    # Fiona Gallagher applies to Frontend
            8: [3],    # George Costanza applies to Product Manager
            9: [0],    # Helen Keller applies to Python Backend
            10: [1],   # Ian Malcolm applies to ML Engineer
            11: [0]    # Julia Roberts applies to Python Backend
        }
        
        # Predefined Assessment Scores for specific candidate-job pairs
        # Format: (candidate_index, job_index, coding, aptitude, technical, hr, project)
        scores_data = [
            (0, 0, 85.0, 78.0, 80.0, 75.0, 90.0), # John Doe @ Python Backend
            (1, 2, 88.0, 82.0, 85.0, 80.0, 85.0), # Jane Smith @ Frontend
            (2, 0, 95.0, 92.0, 98.0, 85.0, 95.0), # Alice Johnson @ Python Backend
            (2, 1, 98.0, 95.0, 98.0, 90.0, 98.0), # Alice Johnson @ ML Engineer
            (3, 4, 72.0, 78.0, 74.0, 80.0, 80.0), # Bob Brown @ DevOps
            (4, 3, 50.0, 88.0, 60.0, 85.0, 75.0), # Charlie Green @ Product Manager
            (6, 0, 90.0, 86.0, 88.0, 80.0, 90.0), # Evan Wright @ Python Backend
            (6, 1, 92.0, 88.0, 90.0, 82.0, 92.0), # Evan Wright @ ML Engineer
            (8, 3, 40.0, 70.0, 50.0, 75.0, 55.0)  # George Costanza @ Product Manager
        ]
        
        # First create all applications
        apps_created = []
        for c_idx, j_list in applications_map.items():
            candidate = candidates[c_idx]
            for j_idx in j_list:
                job = jobs[j_idx]
                app = models.Application(
                    candidate_id=candidate.candidate_id,
                    job_id=job.job_id,
                    status="Applied"
                )
                db.add(app)
                db.commit()
                apps_created.append(app)
                
        # Update assessments
        for c_idx, j_idx, cod, apt, tech, hr, proj in scores_data:
            candidate = candidates[c_idx]
            job = jobs[j_idx]
            assessment = models.Assessment(
                candidate_id=candidate.candidate_id,
                job_id=job.job_id,
                coding_score=cod,
                aptitude_score=apt,
                technical_score=tech,
                hr_score=hr,
                project_score=proj
            )
            db.add(assessment)
            db.commit()
            
            # Shortlist candidates who have good scores
            app = db.query(models.Application).filter(
                models.Application.candidate_id == candidate.candidate_id,
                models.Application.job_id == job.job_id
            ).first()
            if (cod + tech) / 2 >= 75:
                app.status = "Shortlisted"
            elif (cod + tech) / 2 < 60:
                app.status = "Rejected"
            db.commit()
            
        print("Calculating initial AI scores...")
        # 6. Recalculate AI scores and train ML model (on-the-fly)
        for app in apps_created:
            crud.calculate_and_save_ai_score(db, app.candidate_id, app.job_id)
            
        # Add a note for Alice Johnson
        alice = candidates[2] # Alice Johnson
        python_job = jobs[0] # Python Backend Job
        crud.create_note(
            db, 
            recruiter_id=1, 
            candidate_id=alice.candidate_id, 
            job_id=python_job.job_id, 
            note_text="Outstanding candidate. Perfect scores in coding and systems design. Highly recommended for immediate hiring."
        )
        
        print("Database seeded with demo accounts, jobs, and candidate applications successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
