import os
from typing import Set
try:
    from pydantic_settings import BaseSettings
    USE_PYDANTIC_SETTINGS = True
except ImportError:
    from pydantic import BaseModel as BaseSettings
    USE_PYDANTIC_SETTINGS = False
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # App Info
    APP_TITLE: str = "Candidate Application Form"
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    UPLOAD_DIR: str = os.path.join(os.path.dirname(BASE_DIR), "uploads")
    
    # Database Configuration
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: str = "Rohith123"
    DB_NAME: str = "job_app"
    
    # File Upload Configuration
    ALLOWED_EXTENSIONS: Set[str] = {"pdf", "doc", "docx"}
    MAX_FILE_SIZE_BYTES: int = 5 * 1024 * 1024  # 5 MB

    if USE_PYDANTIC_SETTINGS:
        model_config = {"env_file": ".env", "extra": "ignore"}
    else:
        # Fallback for manual env loading
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            for field in self.__fields__:
                env_val = os.getenv(field.upper())
                if env_val:
                    setattr(self, field, env_val)

settings = Settings()
