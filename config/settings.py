import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
CHROMA_COLLECTION_NAME: str = "codewatch_kb"

EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

SUPPORTED_LANGUAGES: list[str] = ["python", "javascript", "php", "java", "typescript", "go", "ruby"]

SEVERITY_ORDER: list[str] = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]

if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY is not set. Copy .env.example to .env and add your key.")
