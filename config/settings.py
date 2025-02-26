import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    embedding_model: str = "text-embedding-3-small"
    completion_model: str = "gpt-3.5-turbo"
    documents_dir: str = os.path.join(os.getcwd(), "data", "documents")
    vector_store_path: str = os.path.join(os.getcwd(), "data", "vector_store")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 