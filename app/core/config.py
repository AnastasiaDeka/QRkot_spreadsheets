from typing import Optional
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    """
    Настройки приложения.
    """
    app_title: str = 'Благотворительный фонд поддержки котиков'
    app_description: str = 'Котики'
    database_url: str = 'sqlite+aiosqlite:///./qrkot_charity_fund.db'
    secret: str = 'secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    PASSWORD_MIN_LENGTH: int = 3
    MIN_INVESTED_AMOUNT: int = 0
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
