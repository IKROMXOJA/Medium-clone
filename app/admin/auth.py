from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models.user import User
from ..utils.security import verify_password, create_access_token

router = APIRouter(prefix="/admin-auth", tags=["admin-auth"])

ADMIN_COOKIE_NAME = "admin_token"

@router.post("/login")
def admin_login(resp: Response, db: Session = Depends(get_db)):
    # oddiy: env-dagi admini yaratib qo'yamiz (yo'q bo'lsa)
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        raise HTTPException(500, "Admin user not seeded")
    token = create_access_token(sub=admin.email, roles=["admin"])
    resp.set_cookie(ADMIN_COOKIE_NAME, token, httponly=True, samesite="lax")
    return {"ok": True}

@router.post("/logout")
def admin_logout(resp: Response):
    resp.delete_cookie(ADMIN_COOKIE_NAME)
    return {"ok": True}
