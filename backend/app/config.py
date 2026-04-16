from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq LLM
    GROQ_API_KEY: str = "your_groq_api_key_here"
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "llama-3.1-8b-instant"
    GROQ_EMBEDDING_MODEL: str = "nomic-embed-text-v1_5"

    # PostgreSQL
    DATABASE_URL: str = "postgresql://athena:athena@localhost:5432/athena"

    # ChromaDB
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001

    # Elasticsearch (optional)
    ELASTICSEARCH_HOST: str = "http://localhost:9200"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
