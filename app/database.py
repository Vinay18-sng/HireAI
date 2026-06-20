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

DATABASE_URL = os.getenv("DATABASE_URL")

# Resolve a safe default absolute SQLite database path in the application root directory
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
default_sqlite_db_path = os.path.join(base_dir, "hireai.db")
default_sqlite_url = f"sqlite:///{default_sqlite_db_path}"

# Fallback mechanism for DB connection
engine = None
try:
    if DATABASE_URL:
        # Standardize PostgreSQL URLs for SQLAlchemy
        if DATABASE_URL.startswith("postgres://") or DATABASE_URL.startswith("postgresql://"):
            if DATABASE_URL.startswith("postgres://"):
                DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
            logger.info("Attempting to connect to PostgreSQL database...")
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            with engine.connect() as conn:
                pass
            logger.info("Successfully connected to PostgreSQL database.")
        
        # Standardize MySQL URLs
        elif DATABASE_URL.startswith("mysql"):
            # Ensure pymysql driver is used if not specified
            if DATABASE_URL.startswith("mysql://"):
                DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
            logger.info("Attempting to connect to MySQL database...")
            engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
            with engine.connect() as conn:
                pass
            logger.info("Successfully connected to MySQL database.")
            
        # Support configured SQLite
        elif DATABASE_URL.startswith("sqlite"):
            logger.info(f"Using configured SQLite database URL: {DATABASE_URL}")
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        
        else:
            logger.warning(f"Unsupported database scheme in URL. Falling back to default SQLite.")
            DATABASE_URL = default_sqlite_url
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        logger.info("No DATABASE_URL configured. Using SQLite fallback.")
        DATABASE_URL = default_sqlite_url
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info(f"Connected to local SQLite database at: {default_sqlite_db_path}")

except Exception as e:
    logger.warning(f"Failed to connect to configured Database: {e}")
    logger.warning(f"Falling back to default SQLite database at: {default_sqlite_db_path}")
    DATABASE_URL = default_sqlite_url
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
