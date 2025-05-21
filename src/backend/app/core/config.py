import os
import secrets
from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, validator

class Settings(BaseSettings):
    # 基本配置
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 数据目录
    DATA_DIR: str = os.getenv("DATA_DIR", "/app/data")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "/app/logs")
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{DATA_DIR}/app.db"
    )
    
    # 美股数据API配置
    ALPHA_VANTAGE_API_KEY: str = os.getenv("ALPHA_VANTAGE_API_KEY", "")
    FINNHUB_API_KEY: str = os.getenv("FINNHUB_API_KEY", "")
    
    # 登录密码
    LOGIN_PASSWORD: str = os.getenv("LOGIN_PASSWORD", "admin")
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # 系统配置
    PROJECT_NAME: str = "US Stock Scanner"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
