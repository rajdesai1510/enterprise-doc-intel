from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env from the repository root so env vars are available when running from inside `backend`
# Note: parents[3] points to the project root (enterprise-doc-intel) for this file layout
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(_env_path)

class Settings(BaseSettings):
    gemini_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    pinecone_api_key: Optional[str] = None
    pinecone_env: Optional[str] = None
    pinecone_index_host: Optional[str] = None
    pinecone_sparse_index_host: Optional[str] = None
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    SUPABASE_BUCKET: str = "documents"
    database_url: Optional[str] = None
    jwt_secret: Optional[str] = None

    # Prefer an absolute env file path if it exists, otherwise fall back to default behavior
    model_config = {"env_file": str(_env_path) if _env_path.exists() else ".env"}

settings = Settings()
