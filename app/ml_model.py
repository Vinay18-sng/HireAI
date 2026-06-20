import os
import pickle
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

logger = logging.getLogger(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml_model.pkl")
DATASET_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset", "candidates_sample.csv")

def train_and_save_model():
    """Trains a Random Forest classifier on the generated sample dataset and saves the pipeline."""
    logger.info("Training suitability classification model...")
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}. Please generate it first.")
        
    df = pd.read_csv(DATASET_PATH)
    
    # Features and target
    X = df.drop(columns=["selected_or_not"])
    y = df["selected_or_not"]
    
    # Categorical and numerical columns
    categorical_cols = ["role_applied", "degree"]
    numerical_cols = [
        "cgpa", "skill_match_percent", "experience_years", 
        "coding_score", "aptitude_score", "technical_score", 
        "hr_score", "certification_count", "project_score"
    ]
    
    # Define preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", StandardScaler(), numerical_cols)
        ]
    )
    
    # Combine preprocessing with model
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Split train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    logger.info(f"Model trained successfully! Test Accuracy: {accuracy:.4f}")
    logger.info("\n" + report)
    
    # Ensure directory exists and save
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)
        
    logger.info(f"Model serialized and saved to {MODEL_PATH}")
    return pipeline

def load_model():
    """Loads model from disk, training a new one if not found."""
    if not os.path.exists(MODEL_PATH):
        logger.info("Pickled model not found. Initiating on-the-fly training...")
        return train_and_save_model()
        
    try:
        with open(MODEL_PATH, "rb") as f:
            pipeline = pickle.load(f)
        return pipeline
    except Exception as e:
        logger.warning(f"Error loading model: {e}. Retraining...")
        return train_and_save_model()

def predict_suitability(
    role_applied: str,
    degree: str,
    cgpa: float,
    skill_match_percent: float,
    experience_years: int,
    coding_score: float,
    aptitude_score: float,
    technical_score: float,
    hr_score: float,
    certification_count: int,
    project_score: float
) -> float:
    """Predicts candidates selection suitability percentage (0.0 to 100.0) based on model decision boundary."""
    try:
        pipeline = load_model()
        
        # Format candidate row matching dataset structure
        input_data = pd.DataFrame([{
            "role_applied": role_applied,
            "degree": degree,
            "cgpa": cgpa,
            "skill_match_percent": skill_match_percent,
            "experience_years": experience_years,
            "coding_score": coding_score,
            "aptitude_score": aptitude_score,
            "technical_score": technical_score,
            "hr_score": hr_score,
            "certification_count": certification_count,
            "project_score": project_score
        }])
        
        # Predict class 1 (selected) probability
        prob = pipeline.predict_proba(input_data)[0][1]
        return round(float(prob) * 100.0, 2)
    except Exception as e:
        logger.error(f"Error during ML prediction: {e}")
        # Safe fallback (e.g. average coding & technical scores)
        fallback_score = (coding_score + technical_score) / 2.0 if (coding_score and technical_score) else 50.0
        return round(fallback_score, 2)
