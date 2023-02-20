from pydantic import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    PROJECT_ID: int
    BASE_URL: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
