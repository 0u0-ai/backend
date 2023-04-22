from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    pinecone_api_key: str
    pinecone_environment: str
    pinecone_index: str
    port: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()