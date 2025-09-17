from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return {"message": "Welcome Admin"}
