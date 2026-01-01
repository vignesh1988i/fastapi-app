from pydantic import BaseModel
from functools import lru_cache
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseModel):
    # MQ Web REST API Configuration
    mq_rest_base_url: str
    mq_rest_base_mqsc_url: str
    mq_username: str
    mq_password: str
    
    # JWT Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # FastAPI User Authentication
    api_username: str
    api_password: str
    
    class Config:
        # Allow extra fields and case insensitive
        extra = "ignore"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Load settings from environment variables."""
    return Settings(
        mq_rest_base_url=os.getenv("MQ_REST_BASE_URL", "http://localhost:9443/ibmmq/rest/v1/admin"),
        mq_rest_base_mqsc_url=os.getenv("MQ_REST_BASE_MQSC_URL", "http://localhost:9443/ibmmq/rest/v1/admin/action"),
        mq_username=os.getenv("MQ_USERNAME", ""),
        mq_password=os.getenv("MQ_PASSWORD", ""),
        secret_key=os.getenv("SECRET_KEY", ""),
        algorithm=os.getenv("ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
        api_username=os.getenv("API_USERNAME", "admin"),
        api_password=os.getenv("API_PASSWORD", "admin123")
    )