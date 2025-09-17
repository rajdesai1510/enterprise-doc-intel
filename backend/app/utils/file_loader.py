from supabase import create_client
from app.core.config import settings
import uuid
import os
from pypdf import PdfReader
import io

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)


def upload_file(file_bytes: bytes, filename: str) -> str:
    """
    Upload file to Supabase Storage and return storage path
    """
    ext = os.path.splitext(filename)[1]
    storage_path = f"{uuid.uuid4()}{ext}"

    supabase.storage \
        .from_(settings.SUPABASE_BUCKET) \
        .upload(storage_path, file_bytes)

    return storage_path


def download_file(storage_path: str) -> bytes:
    """
    Download file from Supabase Storage
    """
    response = supabase.storage \
        .from_(settings.SUPABASE_BUCKET) \
        .download(storage_path)

    return response


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text

def delete_file(storage_path: str):
    supabase.storage \
        .from_(settings.SUPABASE_BUCKET) \
        .remove([storage_path])
