from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Azure Storage settings
    azure_storage_connection_string: str = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    blob_container_name: str = "client-data"
    
    # Azure Document Intelligence settings
    document_intelligence_endpoint: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "")
    document_intelligence_key: str = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    
    # Azure AI Foundry settings
    ai_foundry_endpoint: str = os.getenv("AZURE_AI_FOUNDRY_ENDPOINT", "")
    ai_foundry_key: str = os.getenv("AZURE_AI_FOUNDRY_KEY", "")
    
    # Application settings
    max_file_size: int = 52428800  # 50MB in bytes
    allowed_extensions: set = {".pdf", ".docx", ".xlsx"}
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings() 