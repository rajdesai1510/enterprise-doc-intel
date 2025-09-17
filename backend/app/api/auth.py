from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.auth import create_user, authenticate
from app.core.security import create_token

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(email: str, password: str, db: Session = Depends(get_db)):
    user = create_user(db, email, password)
    return {"id": user.id}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate(db, email, password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    return {"token": create_token(user.id, user.role)}
