from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = 'mongodb://localhost:27017'
    DB_NAME: str = 'finance_tracker'
settings = Settings()