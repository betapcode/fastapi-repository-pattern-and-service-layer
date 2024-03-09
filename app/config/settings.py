from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # FastAPI
    # Debug should be set to False on production
    DEBUG: bool = os.getenv("DEBUG") == "True"
    # Title is the name of application
    TITLE: str = os.getenv("TITLE")
    # SQLITE connection string
    SQLITE_CONNECTION_STRING: str = "sqlite:///database.db" #os.getenv("SQLITE_CONNECTION_STRING")


settings = Settings()
