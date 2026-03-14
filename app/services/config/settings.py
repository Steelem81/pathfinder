import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

env_path = find_dotenv()

load_dotenv(env_path)

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL")
    MAX_TOKENS: int = os.getenv("MAX_TOKENS")
    TEMPERATURE: float = os.getenv("TEMPERATURE")

settings = Settings()