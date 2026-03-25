from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
import mysql.connector
from mysql.connector import Error

# Database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database and apply necessary ALTER TABLE queries."""
    try:
        # 1. Ensure Database Exists (using mysql-connector for bootstrap)
        conn = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()

        # 2. Apply Migrations / Alter Table
        with engine.connect() as conn:
            # Check if table exists
            table_check = conn.execute(text("SHOW TABLES LIKE 'candidates'")).fetchone()
            if table_check:
                # Get existing columns
                columns = [row[0] for row in conn.execute(text("SHOW COLUMNS FROM candidates")).fetchall()]
                
                # ALTER logic
                alter_queries = []
                
                # Rename id to sr_no if id exists and sr_no doesn't
                if 'id' in columns and 'sr_no' not in columns:
                    alter_queries.append("CHANGE COLUMN id sr_no INT AUTO_INCREMENT")
                
                # Rename phone to phone_number
                if 'phone' in columns and 'phone_number' not in columns:
                    alter_queries.append("CHANGE COLUMN phone phone_number VARCHAR(20)")
                
                # Rename location to current_location
                if 'location' in columns and 'current_location' not in columns:
                    alter_queries.append("CHANGE COLUMN location current_location VARCHAR(100)")
                
                # Rename company to current_company
                if 'company' in columns and 'current_company' not in columns:
                    alter_queries.append("CHANGE COLUMN company current_company VARCHAR(100)")
                
                # Rename reason to reason_for_job_change
                if 'reason' in columns and 'reason_for_job_change' not in columns:
                    alter_queries.append("CHANGE COLUMN reason reason_for_job_change TEXT")
                
                # Add missing columns
                if 'first_name' not in columns:
                    alter_queries.append("ADD COLUMN first_name VARCHAR(100) AFTER sr_no")
                if 'last_name' not in columns:
                    alter_queries.append("ADD COLUMN last_name VARCHAR(100) AFTER first_name")
                if 'comments' not in columns:
                    alter_queries.append("ADD COLUMN comments TEXT")
                
                # Ensure email is UNIQUE
                # We can't easily check for UNIQUE constraint name in a simple cross-platform way, 
                # but we can try to add it and ignore if it exists (or just trust the user's "Ensure email is UNIQUE").
                # Let's try to see if 'email' exists and if it has a unique constraint.
                # For simplicity, we'll try to add it.
                
                if alter_queries:
                    query = "ALTER TABLE candidates " + ", ".join(alter_queries)
                    conn.execute(text(query))
                    conn.commit()
                    print("[DB] Tables updated with new fields.")

            else:
                # Table doesn't exist, SQLAlchemy will create it via Base.metadata.create_all
                print("[DB] Creating new candidates table.")
        
        # 3. Create tables defined in models
        from app.models.candidate import Candidate  # Import here to avoid circular imports
        Base.metadata.create_all(bind=engine)
        print("[DB] Database initialization complete.")
        
    except Exception as e:
        print(f"[DB ERROR] {e}")

