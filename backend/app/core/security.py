from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from hashlib import sha256
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"])
ALGO = "HS256"

# Bcrypt has a 72-byte input limit; to safely support arbitrary-length passwords
# we pre-hash the password with SHA-256 and pass the hex digest (64 bytes) to bcrypt.
# This preserves entropy while avoiding truncation errors.

def _pre_hash(password: str) -> str:
    if password is None:
        raise ValueError("password must be a non-empty string")
    return sha256(password.encode("utf-8")).hexdigest()

def _bcrypt_hash_direct(pre_hashed_hex: str) -> str:
    # bcrypt.hashpw expects bytes
    hashed = bcrypt.hashpw(pre_hashed_hex.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def _bcrypt_verify_direct(pre_hashed_hex: str, hashed: str) -> bool:
    return bcrypt.checkpw(pre_hashed_hex.encode("utf-8"), hashed.encode("utf-8"))

def hash_password(password: str) -> str:
    """Hash a password (pre-hashes with SHA-256 to avoid bcrypt length limits).

    Tries to use passlib first; on unexpected backend errors falls back to using
    the `bcrypt` library directly to avoid initialization issues that can occur
    in some environments.
    """
    pre = _pre_hash(password)
    try:
        return pwd_context.hash(pre)
    except Exception:
        # fallback to direct bcrypt use
        return _bcrypt_hash_direct(pre)

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a bcrypt hash (using the same pre-hash).

    Uses passlib where possible and falls back to `bcrypt.checkpw` on error.
    """
    pre = _pre_hash(password)
    try:
        return pwd_context.verify(pre, hashed)
    except Exception:
        return _bcrypt_verify_direct(pre, hashed)

def create_token(user_id, role):
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGO)
