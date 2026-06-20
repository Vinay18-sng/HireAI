import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./hireai.db")

# Fallback mechanism for DB connection
engine = None
try:
    if DATABASE_URL and DATABASE_URL.startswith("mysql"):
        logger.info(f"Attempting to connect to MySQL database...")
        # Create MySQL engine
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
        # Test connection
        with engine.connect() as conn:
            pass
        logger.info("Successfully connected to MySQL database.")
    else:
        logger.info("No MySQL configuration found. Using SQLite.")
        DATABASE_URL = "sqlite:///./hireai.db"
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info("Connected to local SQLite database.")
except Exception as e:
    logger.warning(f"Failed to connect to configured Database: {e}")
    logger.warning("Falling back to SQLite database at 'sqlite:///./hireai.db'")
    DATABASE_URL = "sqlite:///./hireai.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
