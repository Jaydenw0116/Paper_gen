from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    temp_dir: str = "/tmp/paper_gen"
    max_file_size: int = 20 * 1024 * 1024
    max_questions: int = 100

    class Config:
        env_file = ".env"

settings = Settings()

os.makedirs(settings.temp_dir, exist_ok=True)