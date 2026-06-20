import csv
import os
import random

def generate():
    os.makedirs("dataset", exist_ok=True)
    filepath = "dataset/candidates_sample.csv"
    
    roles = ["Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer", "Frontend Developer"]
    degrees = ["Bachelor", "Master", "PhD", "Diploma"]
    
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "role_applied", "degree", "cgpa", "skill_match_percent", 
            "experience_years", "coding_score", "aptitude_score", 
            "technical_score", "hr_score", "certification_count", 
            "project_score", "selected_or_not"
        ])
        
        # Seed for reproducibility
        random.seed(42)
        
        for _ in range(400):
            role = random.choice(roles)
            degree = random.choices(degrees, weights=[0.7, 0.2, 0.05, 0.05])[0]
            cgpa = round(random.uniform(6.0, 10.0), 2)
            experience = random.choices(
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15], 
                weights=[15, 15, 12, 12, 10, 8, 6, 5, 5, 4, 4, 2, 2]
            )[0]
            
            # Scores
            skill_match = round(random.uniform(20.0, 100.0), 2)
            coding = round(random.uniform(30.0, 100.0), 2)
            aptitude = round(random.uniform(40.0, 100.0), 2)
            technical = round(random.uniform(30.0, 100.0), 2)
            hr = round(random.uniform(45.0, 100.0), 2)
            certs = random.randint(0, 4)
            projects = round(random.uniform(20.0, 100.0), 2)
            
            # Simple heuristic for selection probability to make data realistic
            # Average score with weights
            avg_score = (
                (skill_match * 0.2) + 
                (coding * 0.25) + 
                (technical * 0.2) + 
                (hr * 0.1) + 
                (projects * 0.15) + 
                (experience * 4.0) + # 4 points per year
                (certs * 3.0)
            )
            
            # Define selection threshold
            if avg_score > 75:
                prob = 0.85
            elif avg_score > 60:
                prob = 0.45
            elif avg_score > 45:
                prob = 0.15
            else:
                prob = 0.02
                
            selected = 1 if random.random() < prob else 0
            
            writer.writerow([
                role, degree, cgpa, skill_match, experience, 
                coding, aptitude, technical, hr, certs, 
                projects, selected
            ])
            
    print(f"Generated 400 candidate rows successfully in {filepath}.")

if __name__ == "__main__":
    generate()
