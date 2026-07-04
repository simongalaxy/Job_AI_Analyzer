import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    
    # logger settings.
    log_path: str
    log_level: str
    
    # database settings.
    username: str
    password: str
    host: str
    port: str
    db_name: str
    
    # llm settings.
    ollama_extraction_model: str
    ollama_summarization_model: str
    ollama_insight_model: str
    ollama_report_model: str

    # folder paths for reports.
    report_path: str
        
    # pydantic settings config.
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    # batch size for processing job ads in batches.
    batch_size: int

# Singleton instance of the settings.
settings = Settings() # type: ignore
