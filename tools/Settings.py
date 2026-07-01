import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    
    # logger settings.
    log_path: str
    log_level: str
    
    # PostgreSQL database settings.
    username: str
    password: str
    host: str
    port: int
    db_name: str
    
    # Ollama LLM settings.
    ollama_extraction_model: str
    ollama_embedding_model: str
    ollama_summarization_model: str
    
    # report settings.
    report_path: str
    
    # crawl4ai settings.
    playwright_skip_browser_download: int
    
    
    # pydantic settings config.
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Singleton instance of the settings.
settings = Settings() # type: ignore
